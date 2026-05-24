cli_gpt() {
    local initial_input="$BUFFER"
    local venv_python="$CLI_GPT_PATH/bin/python3"
    [[ -x "$venv_python" ]] || venv_python="$CLI_GPT_PATH/bin/python"
    local selected

    selected=$($venv_python "$CLI_GPT_PATH/cli_gpt_ui.py" "$initial_input") || return

    if [[ -n "$selected" ]]; then
        BUFFER="$selected"
        CURSOR=$#BUFFER
    fi

    zle redisplay
}

zle -N cli_gpt_widget cli_gpt

bindkey '^G' cli_gpt_widget
