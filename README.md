# nlp-to-zsh

![demo gif](/screenshots/gpt-bash-demo.gif)

**2026 update:** Looking back at this tool I made in early 2023, I was ahead of the curve! It's interesting to see major companies like Google integrate similar features into their cloud products. This tool should stay useful for casual system admins. This update cleaned up the repo and replaced the fine-tuned model with a prompt, since GPT-5.5 no longer needs or supports fine-tuning (for this use case). A prompt with structured output is more efficient, faster, and better in every way.

## Brief Description

Generate commands faster than ever before. Nlp-to-zsh is a cutting-edge tool that seamlessly integrates Natural Language Processing (NLP) services, like OpenAI's ChatGPT, with the Zsh command line. It allows users to type commands in plain English and receive command-line suggestions, enhancing the user experience and efficiency.

## Disclaimer

Use at your own risk. This tool is provided without guarantees or warranty. It sends data from the command line buffer to OpenAI or other NLP services. Note that the commands generated may not always work as expected and could potentially cause harm to your system, resulting in data loss. Please proceed with caution. I highly recommend trying it in a virtual machine or sandbox first.

## What it Does and How to Use

Type what you want to do in plain English and press `Ctrl+G`. Choose from the listed options, and the command will appear in your command-line buffer.

## Supported Systems

Nlp-to-zsh is developed and tested primarily for GNU/Linux systems. macOS users might experience certain limitations.

## Setup and Installation

1.  **Install Dependencies:** Ensure `zsh`, `python`, and `fzf` are installed on your system (using either `brew` or `pacman`).
2.  **Python Requirements:** Install the Python dependencies. On macOS, I use a venv because I did not want to install globally and risk unintended side effects. Run `python3 -m venv ./` in the project directory, then `source bin/activate` and `pip install -r requirements.txt`. On Arch Linux, you can also run `sudo pacman -S python-openai` to install the dependency globally. Check older commits in this repo, or modify `nlp-to.zsh` to use your system Python.
3.  **Script Installation:** `cp ask_gpt.py /usr/local/bin/ && chmod +x /usr/local/bin/ask_gpt.py` (only if you are using the Arch Linux method; otherwise, run `chmod +x ask_gpt.py`). For both macOS and Arch Linux, run `cp nlp-to.zsh /usr/local/bin/ && chmod +x /usr/local/bin/nlp-to.zsh`. You may need `sudo` for elevated permissions. Keep `system_prompt.txt` next to `ask_gpt.py` (or set `NLP_TO_ZSH_PATH` to the project directory and run from there).
4.  **OpenAI Setup:** Create an API key at [OpenAI](https://platform.openai.com/). This project uses **GPT-5.5** with a structured JSON response (no fine-tuning or `linux-guru.jsonl` required). The system prompt in `system_prompt.txt` encodes the same behavior as the old fine-tuned assistant: natural language in, runnable shell commands out.

5.  **Shell Integration:** Append to `~/.zshrc`:

```
source /usr/local/bin/nlp-to.zsh
export OPENAI_API_KEY='your_key_here'
export NLP_TO_ZSH_PATH='path/to/project/directory'
# Optional override (default: gpt-5.5):
# export OPENAI_MODEL_NAME='gpt-5.5'
```

6.  **Open new shell:** Open a new `zsh` session, or run `source ~/.zshrc`.

## Future Plans and Features

- Built-in automated testing environment allowing users to quickly sandbox commands. (I had chroot or LVM snapshots in mind for this.)
- Support for multiple APIs for quickly accessing various models.
- Support for locally hosted models.

## Inspiration

When I first began using Linux and learning the command line, I was often sifting through Stack Overflow posts, man pages, and blog posts. I remember dreaming I could use natural language to quickly reference commands or write simple scripts. Modern NLP technology makes that feasible. I hope this project helps you learn the command line quickly and effectively, and speeds up your workflow.

## Credits

Developed by myself. All contributions are deeply appreciated.

**Enjoy using nlp-to-zsh!**
