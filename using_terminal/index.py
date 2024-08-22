# from langchain.chat_models import ChatOpenAI
from langchain.schema import AIMessage, SystemMessage, HumanMessage
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os
load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


# Initialize the model with your API key
model = ChatOpenAI(model="gpt-4", api_key=openai_api_key)

# Directory to store chat histories
chat_dir = os.path.join(os.path.dirname(__file__), '..', 'chat_histories')
os.makedirs(chat_dir, exist_ok=True)

current_topic = None
chat_history = []

system_message = SystemMessage(content="You are a helpful AI Assistant")

def save_chat_history(topic, chat_history):
    with open(os.path.join(chat_dir, f"{topic}.txt"), "w") as f:
        for message in chat_history:
            if isinstance(message, HumanMessage):
                f.write(f"user: {message.content}\n")
            elif isinstance(message, AIMessage):
                f.write(f"AI: {message.content}\n")
            # Optionally include the SystemMessage if desired:
            # elif isinstance(message, SystemMessage):
            #     f.write(f"system: {message.content}\n")


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

while True:
    query = input("==================\nYou: ")
    print("==================")
    
    if query.lower() == "exit":
        if current_topic:
            save_chat_history(current_topic, chat_history)
        break
    
    if query.lower() == "topic" or query.lower()=="topics":
        topics = list_topics()
        if not topics:
            print("No topics available.")
            continue
        
        print("Available topics:")
        for idx, topic in enumerate(topics, start=1):
            print(f"{idx}. {topic}")
        
        topic_choice = input("Which topic would you like to continue? (Enter the number or type a new topic name): ")
        if topic_choice == "exit":
            break
        elif topic_choice.isdigit() and 1 <= int(topic_choice) <= len(topics):
         
            current_topic = topics[int(topic_choice) - 1]
        else:
            current_topic = topic_choice.strip()
        
        chat_history = load_chat_history(current_topic)
        chat_history.insert(0, system_message)
        continue
    
    if current_topic is None:
        current_topic = input("Enter a topic for this conversation: ").strip()
        chat_history = load_chat_history(current_topic)
        chat_history.insert(0, system_message)
    
    chat_history.append(HumanMessage(content=query))  # Appending user's message
    
    # Generate response from the model using invoke
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))  # Appending AI's message

    print("++++++++++++++++\nAI:", response)
    print("++++++++++++++++")

    # Save chat history after each interaction
    save_chat_history(current_topic, chat_history)

print("-------Chat History ---------")
print(chat_history)