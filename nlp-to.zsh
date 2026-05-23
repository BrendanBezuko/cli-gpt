
nlp_to_zsh() { 
    # Capture the initial input
    local initial_input="$BUFFER"

    local venv_python="$NLP_TO_ZSH_PATH/bin/python"
    
    # Call the Python script and get suggestions 
    local suggestions=$($venv_python $NLP_TO_ZSH_PATH/ask_gpt.py "$initial_input")
    
    # Use fzf to let the user select a suggestion 
    local selected=$(echo "$suggestions" | fzf --height 10 --layout=reverse)
    
    # Replace the current command line with the selected suggestion
    BUFFER="$selected"

    # Move the cursor to the end of the line
    CURSOR=$#BUFFER
    
    # Redraw the command line
    zle redisplay
}

# Bind the function to a ZLE widget for interactive use
zle -N nlp_widget nlp_to_zsh

# Bind the widget to a key combination, e.g., Ctrl+G
bindkey '^G' nlp_widget