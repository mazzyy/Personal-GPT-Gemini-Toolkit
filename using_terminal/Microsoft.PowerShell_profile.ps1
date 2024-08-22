# Path to the virtual environment's activate script
$env:VIRTUAL_ENV_PATH = "C:\Users\z004wezy\chatgpt_4\.venv\Scripts\Activate.ps1"

# Path to your Python script
$env:PYTHON_SCRIPT_PATH = "C:\Users\z004wezy\chatgpt_4\using_terminal\index.py"

# Define the function to activate the virtual environment and run the script
function Start-MyScript {
  
    . $env:VIRTUAL_ENV_PATH

    python $env:PYTHON_SCRIPT_PATH
}


Set-Alias gpt Start-MyScript
