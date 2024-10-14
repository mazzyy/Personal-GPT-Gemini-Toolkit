# Stage 1: Build the frontend (if it's more than simple HTML, e.g., if you use any build tools like npm)
# For simple static HTML, this step can be skipped, but I'll include it here for clarity
FROM nginx:alpine as frontend

# Copy the HTML files to nginx's default location
COPY ./chat-frontend /usr/share/nginx/html

# Stage 2: Backend setup
FROM python:3.10-slim as backend

# Set the working directory for backend
WORKDIR /app

# Copy the FastAPI app to the container
COPY ./backend /app

# Copy the chat_histories folder (important for the backend)
COPY ./chat_histories /app/chat_histories

# Copy the requirements and install them
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# Stage 3: Final setup combining both backend and frontend services
FROM nginx:alpine

# Copy the frontend files from the build stage
COPY --from=frontend /usr/share/nginx/html /usr/share/nginx/html

# Copy backend and chat_histories from the backend stage
COPY --from=backend /app /app

# Expose ports for nginx (frontend) and FastAPI (backend)
EXPOSE 80 8000

# Start both backend and nginx frontend services
CMD ["/bin/sh", "-c", "nginx && uvicorn /app/main:app --host 0.0.0.0 --port 8000"]
