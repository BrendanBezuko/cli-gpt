#!/usr/bin/env python3
import json
import os
import sys
from functools import lru_cache
from pathlib import Path

from openai import BadRequestError, OpenAI

DEFAULT_MODEL = "gpt-5.5"
MAX_SUGGESTIONS = 6
PROMPT_FILE = Path(__file__).with_name("system_prompt.txt")


@lru_cache(maxsize=1)
def _load_system_prompt() -> str:
    if not PROMPT_FILE.is_file():
        raise FileNotFoundError(f"System prompt not found: {PROMPT_FILE}")
    return PROMPT_FILE.read_text(encoding="utf-8").strip()


RESPONSE_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "shell_suggestions",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "suggestions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": MAX_SUGGESTIONS,
                }
            },
            "required": ["suggestions"],
            "additionalProperties": False,
        },
    },
}


def _format_suggestions(suggestions: list[str]) -> str:
    lines = [s.strip() for s in suggestions if s and s.strip()]
    return "\n".join(lines)


def _parse_suggestions(content: str) -> str:
    try:
        data = json.loads(content)
        suggestions = data.get("suggestions", [])
        if isinstance(suggestions, list) and suggestions:
            return _format_suggestions(suggestions)
    except json.JSONDecodeError:
        pass

    # Fallback: treat each non-empty line as one suggestion.
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    return "\n".join(lines)


def _drop_unsupported_param(kwargs: dict, key: str) -> bool:
    if key not in kwargs:
        return False
    if key == "max_completion_tokens":
        kwargs["max_tokens"] = kwargs.pop(key)
    else:
        kwargs.pop(key)
    return True


def _create_completion(client: OpenAI, **kwargs):
    """Call Chat Completions, dropping params unsupported by the SDK or API."""
    while True:
        try:
            return client.chat.completions.create(**kwargs)
        except TypeError:
            if not any(
                _drop_unsupported_param(kwargs, k)
                for k in ("reasoning_effort", "max_completion_tokens")
            ):
                raise
        except BadRequestError as e:
            msg = str(e).lower()
            if "reasoning_effort" in msg and _drop_unsupported_param(
                kwargs, "reasoning_effort"
            ):
                continue
            if "max_completion_tokens" in msg and _drop_unsupported_param(
                kwargs, "max_completion_tokens"
            ):
                continue
            raise


def ask_gpt_completions(prompt: str, max_tokens: int = 500) -> str:
    """
    Returns shell command suggestions (one per line) using the OpenAI API.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL_NAME", DEFAULT_MODEL)

    if not api_key:
        return "API key not found. Please set the OPENAI_API_KEY environment variable."

    try:
        client = OpenAI(api_key=api_key)
        response = _create_completion(
            client,
            model=model,
            messages=[
                {"role": "system", "content": _load_system_prompt()},
                {"role": "user", "content": prompt},
            ],
            response_format=RESPONSE_SCHEMA,
            max_completion_tokens=max_tokens,
        )
        if not response.choices:
            return "No response"

        content = response.choices[0].message.content or ""
        formatted = _parse_suggestions(content)
        return formatted or "No suggestions returned"
    except FileNotFoundError as e:
        return str(e)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ask_gpt.py 'describe what you want to do'", file=sys.stderr)
        sys.exit(1)

    prompt = sys.argv[1]
    print(ask_gpt_completions(prompt))
