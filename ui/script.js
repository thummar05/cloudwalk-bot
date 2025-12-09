const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Auto-focus input
userInput.focus();

// Handle "Enter" key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

sendBtn.addEventListener('click', handleSend);

async function handleSend() {
    const text = userInput.value.trim();
    if (!text) return;

    // 1. Add User Message
    addMessage(text, 'user');
    userInput.value = '';
    sendBtn.disabled = true;

    // 2. Add "Thinking..." placeholder
    const loadingId = addMessage('Thinking...', 'bot', true);

    try {
        // 3. Call the Backend API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question: text })
        });

        const data = await response.json();

        // 4. Remove loader and show actual response
        removeMessage(loadingId);

        if (response.ok) {
            addMessage(data.answer, 'bot', false, data.sources);
        } else {
            addMessage(`Error: ${data.detail || 'Something went wrong'}`, 'bot');
        }

    } catch (error) {
        removeMessage(loadingId);
        addMessage(`Network Error: ${error.message}`, 'bot');
    } finally {
        sendBtn.disabled = false;
        userInput.focus();
    }
}

function addMessage(text, sender, isLoading = false, sources = null) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${sender} ${isLoading ? 'loading' : ''}`;

    // Convert newlines to <br> for display
    const formattedText = text.replace(/\n/g, '<br>');

    let html = `<div class="content">${formattedText}</div>`;

    if (sources && sources.length > 0) {
        html += `<div class="sources">Sources: ${sources.join(', ')}</div>`;
    }

    msgDiv.innerHTML = html;

    // ID for removing loading messages
    const id = Date.now().toString();
    msgDiv.dataset.id = id;

    chatHistory.appendChild(msgDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;

    return id;
}

function removeMessage(id) {
    const el = document.querySelector(`.message[data-id="${id}"]`);
    if (el) el.remove();
}