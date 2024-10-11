#!/bin/bash

# Activate the virtual environment
if [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    .venv/Scripts/activate
    if [ $? -eq 0 ]; then
        echo "Virtual environment activated successfully (Windows)."
    else
        echo "Failed to activate virtual environment (Windows)."
        exit 1
    fi
else
    # Linux/macOS
    source .venv/Scripts/activate
    if [ $? -eq 0 ]; then
        echo "Virtual environment activated successfully (Linux/macOS)."
    else
        echo "Failed to activate virtual environment (Linux/macOS)."
        exit 1
    fi
fi

# Open the index.html in the default web browser
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open ./chat-frontend/index.html
    if [ $? -eq 0 ]; then
        echo "Opened index.html in browser (Linux)."
    else
        echo "Failed to open index.html in browser (Linux)."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open ./chat-frontend/index.html
    if [ $? -eq 0 ]; then
        echo "Opened index.html in browser (macOS)."
    else
        echo "Failed to open index.html in browser (macOS)."
    fi
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start ./chat-frontend/index.html
    if [ $? -eq 0 ]; then
        echo "Opened index.html in browser (Windows)."
    else
        echo "Failed to open index.html in browser (Windows)."
    fi

    # Navigate to the backend folder and run uvicorn in the background
    cd backend
    uvicorn main:app --reload &
    if [ $? -eq 0 ]; then
        echo "FastAPI server started successfully."
    else
        echo "Failed to start FastAPI server."
    fi
else
    echo "Unsupported OS"
fi

# Keep the terminal open after execution
# Infinite loop to keep the terminal open
echo "Script completed. Press Ctrl+C to exit or close the terminal manually."

# Loop to prevent closure
while true; do
    sleep 60
done
