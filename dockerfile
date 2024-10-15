
# Stage 1: Backend setup (no frontend stage needed)
FROM python:3.10-slim 

# Set the working directory for backend
WORKDIR /app


# Copy the FastAPI app to the container
COPY ./backend /app

# Copy the chat_histories folder
COPY ./chat_histories /app/chat_histories

ARG gemini_key
ARG PERSONAL_ACCESS_TOKEN_GITHUB
# Copy the requirements and install them
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
