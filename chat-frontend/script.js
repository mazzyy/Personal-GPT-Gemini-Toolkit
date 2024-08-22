document.addEventListener('DOMContentLoaded', function() {
    const topicsDropdown = document.getElementById('topics');
    const chatHistoryDiv = document.getElementById('chat-history');
    const userInput = document.getElementById('message-input');
    const sendMessageButton = document.getElementById('send-button');
    const loadTopicButton = document.getElementById('load-topic');
    const newTopicButton = document.getElementById('new-topic');

    // const topicsList = document.getElementById("topics-list");
    // const chatHistory = document.querySelector("#chat-history .card-body");
    // const currentTopicTitle = document.getElementById("current-topic");
    // const messageInput = document.getElementById("message-input");
    // const sendButton = document.getElementById("send-button");

    let currentTopic = null;

    // Load topics from the server
    fetch('http://127.0.0.1:8000/topics/')
        .then(response => response.json())
        .then(data => {
            data.topics.forEach(topic => {
                const option = document.createElement('option');
                option.value = topic;
                option.textContent = topic;
                topicsDropdown.appendChild(option);
            });
        });

    // Load chat history for the selected topic
    loadTopicButton.addEventListener('click', function() {
        currentTopic = topicsDropdown.value;
        if (currentTopic) {
            fetch('http://127.0.0.1:8000/load/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ topic: currentTopic })
            })
            .then(response => response.json())
            .then(data => {
                chatHistoryDiv.innerHTML = '';
                data.messages.forEach(msg => {
                    const messageDiv = document.createElement('div');
                    messageDiv.classList.add('chat-message', msg.role === 'user' ? 'user-message' : 'ai-message');
                    messageDiv.textContent = msg.content;
                    chatHistoryDiv.appendChild(messageDiv);
                });
            });
        } else {
            alert('Please select a topic first!');
        }
    });

    // Start a new chat
    newTopicButton.addEventListener('click', function() {
        currentTopic = prompt('Enter a new topic name:');
        if (currentTopic) {
            chatHistoryDiv.innerHTML = '';
            topicsDropdown.value = currentTopic;
        } else {
            alert('Topic name cannot be empty!');
        }
    });

    sendMessageButton.addEventListener('click', function() {
    const message = userInput.value; 
    console.log(message); 

    if (message && currentTopic) { 
        fetch('http://127.0.0.1:8000/chat/', { 
            method: 'POST', 
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ topic: currentTopic, message: message })
        })
        .then(response => response.json())
        .then(data => {

            // User Message (Preserving formatting)
            const userMessageDiv = document.createElement('pre'); // Use <pre> for preformatted text
            userMessageDiv.classList.add('chat-message', 'user-message');
            userMessageDiv.textContent = message;
            chatHistoryDiv.appendChild(userMessageDiv);

            // AI Message (Preserving formatting)
            const aiMessageDiv = document.createElement('pre'); // Use <pre> for preformatted text
            aiMessageDiv.classList.add('chat-message', 'ai-message');
            aiMessageDiv.textContent = data.response;
            chatHistoryDiv.appendChild(aiMessageDiv);

            userInput.value = '';
            chatHistoryDiv.scrollTop = chatHistoryDiv.scrollHeight;
        });
    } else {
        alert('Please enter a message and select a topic!'); 
    }
});
});
