from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.schema import AIMessage, SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os

# Initialize the FastAPI app
app = FastAPI()
load_dotenv()
# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai_api_key = os.getenv('OPENAI_API_KEY')
# Initialize the OpenAI model
model = ChatOpenAI(model="gpt-4", api_key=openai_api_key)

# Directory to store chat histories
chat_dir = os.path.join(os.path.dirname(__file__), '..', 'chat_histories')
os.makedirs(chat_dir, exist_ok=True)

system_message = SystemMessage(content="You are a helpful AI Assistant")

class MessageRequest(BaseModel):
    topic: str
    message: str

class TopicRequest(BaseModel):
    topic: str

@app.post("/chat/")
async def chat(request: MessageRequest):
    topic = request.topic
    user_message = request.message

    chat_history = load_chat_history(topic)
    if not chat_history:
        chat_history = [system_message]

    chat_history.append(HumanMessage(content=user_message))

    # Generate AI response
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    save_chat_history(topic, chat_history)

    return {"response": response}

@app.get("/topics/")
async def get_topics():
    topics = list_topics()
    return {"topics": topics}

@app.post("/load/")
async def load_topic(request: TopicRequest):
    chat_history = load_chat_history(request.topic)
    messages = [
        {"role": "system" if isinstance(msg, SystemMessage) else ("user" if isinstance(msg, HumanMessage) else "ai"),
         "content": msg.content}
        for msg in chat_history
    ]
    print(messages)
    return {"messages": messages}

def save_chat_history(topic, chat_history):
    with open(os.path.join(chat_dir, f"{topic}.txt"), "w") as f:
        for message in chat_history:
            if isinstance(message, HumanMessage):
                f.write(f"user: {message.content}\n")
            elif isinstance(message, AIMessage):
                f.write(f"AI: {message.content}\n")


def load_chat_history(topic):
    history = []
    file_path = os.path.join(chat_dir, f"{topic}.txt")
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            # Read the entire file content
            content = f.read()
            
            # Use regex to find all instances of "User:" and "AI:" and split the content accordingly
            # This also captures the code blocks by including `(?:```.*?```)?`
            messages = re.split(r"(user:|AI:)", content, flags=re.DOTALL)
            
            current_role = None
            for message in messages:
                message = message.strip()
                
                if message == "user:":
                    current_role = "user"
                elif message == "AI:":
                    current_role = "AI"
                elif current_role and message:
                    # Preserve the message exactly as it is, including newlines and spaces
                    if current_role == "user":
                        history.append(HumanMessage(content=message))
                    elif current_role == "AI":
                        history.append(AIMessage(content=message))
                    current_role = None
    
    return history


def list_topics():
   
    return [f.split(".")[0] for f in os.listdir(chat_dir) if f.endswith(".txt")]

