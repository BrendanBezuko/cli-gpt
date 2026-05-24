# cli-gpt

![demo gif](/screenshots/gpt-bash-demo.gif)

**2026 update:** Looking back at this tool I made in early 2023, I was ahead of the curve! It's interesting to see major companies like Google integrate similar features into their cloud products. This tool should stay useful for casual system admins. This update cleaned up the repo and replaced the fine-tuned model with a prompt, since GPT-5.5 no longer needs or supports fine-tuning (for this use case). A prompt with structured output is more efficient, faster, and better in every way.

## Brief Description

Generate commands faster than ever before. **cli-gpt** integrates Natural Language Processing (NLP) services, like OpenAI's ChatGPT, with the Zsh command line. Type what you want in plain English and get runnable command-line suggestions.

## Disclaimer

Use at your own risk. This tool is provided without guarantees or warranty. It sends data from the command line buffer to OpenAI or other NLP services. Note that the commands generated may not always work as expected and could potentially cause harm to your system, resulting in data loss. Please proceed with caution. I highly recommend trying it in a virtual machine or sandbox first.

## What it Does and How to Use

Type what you want to do in plain English and press `Ctrl+G`. A curses UI opens with GPT suggestions. Pick one with Enter, or press `e` to edit your prompt and retry if the results miss the mark.

## Supported Systems

cli-gpt is developed and tested primarily for GNU/Linux systems. macOS users might experience certain limitations.

## Setup and Installation

1.  **Install Dependencies:** Ensure `zsh` and `python` are installed on your system (using either `brew` or `pacman`).
2.  **Python Requirements:** Install the Python dependencies. On macOS, I use a venv because I did not want to install globally and risk unintended side effects. Run `python3 -m venv ./` in the project directory, then `source bin/activate` and `pip install -r requirements.txt`. On Arch Linux, you can also run `sudo pacman -S python-openai` to install the dependency globally. Check older commits in this repo, or modify `cli-gpt.zsh` to use your system Python.
3.  **Script Installation:** Run `chmod +x ask_gpt.py cli_gpt_ui.py`. For both macOS and Arch Linux, run `cp cli-gpt.zsh /usr/local/bin/ && chmod +x /usr/local/bin/cli-gpt.zsh`. You may need `sudo` for elevated permissions. Keep `system_prompt.txt`, `ask_gpt.py`, and `cli_gpt_ui.py` together in the project directory (or set `CLI_GPT_PATH` to that directory).
4.  **OpenAI Setup:** Create an API key at [OpenAI](https://platform.openai.com/). This project uses **GPT-5.5** with a structured JSON response (no fine-tuning or `linux-guru.jsonl` required). The system prompt in `system_prompt.txt` encodes the same behavior as the old fine-tuned assistant: natural language in, runnable shell commands out.

5.  **Shell Integration:** Append to `~/.zshrc`:

```
source /usr/local/bin/cli-gpt.zsh
export OPENAI_API_KEY='your_key_here'
export CLI_GPT_PATH='path/to/project/directory'
# Optional override (default: gpt-5.5):
# export OPENAI_MODEL_NAME='gpt-5.5'
```

6.  **Open new shell:** Open a new `zsh` session, or run `source ~/.zshrc`.

## Inspiration

When I first began using Linux and learning the command line, I was often sifting through Stack Overflow posts, man pages, and blog posts. I remember dreaming I could use natural language to quickly reference commands or write simple scripts. Modern NLP technology makes that feasible. I hope this project helps you learn the command line quickly and effectively, and speeds up your workflow.
