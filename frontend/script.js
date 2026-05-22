// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const themeToggle = document.getElementById('themeToggle');
const attachBtn = document.getElementById('attachBtn');
const welcomeMessage = document.getElementById('welcomeMessage');
const typingIndicator = document.getElementById('typingIndicator');
const statusIndicator = document.getElementById('statusIndicator');
const suggestionBtns = document.querySelectorAll('.suggestion-btn');

// Configuration
const API_URL = 'http://localhost:5000/api/chat';
const CLEAR_URL = 'http://localhost:5000/api/clear';

// Generate unique session ID
const SESSION_ID = 'user_' + Math.random().toString(36).substring(7);

// Event Listeners
sendBtn.addEventListener('click', handleSend);
clearBtn.addEventListener('click', handleClear);
attachBtn.addEventListener('click', () => {
    showNotification('File upload coming soon! 📎', 'info');
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
});

// Suggestion buttons
suggestionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const message = btn.getAttribute('data-msg');
        userInput.value = message;
        handleSend();
    });
});

// Auto-focus input
userInput.focus();

// Functions
async function handleSend() {
    const message = userInput.value.trim();
    
    if (!message) {
        showNotification('Please enter a message!', 'warning');
        return;
    }
    
    // Clear input
    userInput.value = '';
    
    // Remove welcome message
    if (welcomeMessage) {
        welcomeMessage.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
            welcomeMessage.style.display = 'none';
        }, 300);
    }
    
    // Display user message
    addMessage(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: message,
                session_id: SESSION_ID 
            }),
        });
        
        const data = await response.json();
        
        // Hide typing indicator
        hideTypingIndicator();
        
        if (response.ok) {
            if (data.type === 'image' && data.image_data) {
                addImageMessage(data.response, data.image_data);
            } else {
                addMessage(data.response, 'bot');
            }
            updateStatus('connected');
        } else {
            addMessage('Gomen! Something went wrong. Please try again! 🙏', 'bot');
            updateStatus('error');
        }
    } catch (error) {
        hideTypingIndicator();
        addMessage('⚠️ Connection error! Make sure the backend server is running.', 'bot');
        updateStatus('disconnected');
        console.error('Error:', error);
    }
    
    userInput.focus();
}

async function handleClear() {
    if (!confirm('🗑️ Clear all conversation history? This cannot be undone!')) return;
    
    try {
        await fetch(CLEAR_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ session_id: SESSION_ID }),
        });
        
        // Clear chat with animation
        chatContainer.style.opacity = '0';
        setTimeout(() => {
            chatContainer.innerHTML = '';
            const newWelcome = createWelcomeMessage();
            chatContainer.appendChild(newWelcome);
            chatContainer.style.opacity = '1';
        }, 300);
        
        showNotification('✨ Conversation cleared!', 'success');
        updateStatus('connected');
    } catch (error) {
        showNotification('Failed to clear history!', 'error');
        console.error('Error:', error);
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    
    if (sender === 'user') {
        avatar.textContent = '👤';
    } else {
        const img = document.createElement('img');
        img.src = 'assets/logo.png';
        img.alt = 'Animexia';
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';
        avatar.appendChild(img);
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = text;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function addImageMessage(text, imageData) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    const avatarImg = document.createElement('img');
    avatarImg.src = 'assets/logo.png';
    avatarImg.style.width = '100%';
    avatarImg.style.height = '100%';
    avatarImg.style.objectFit = 'cover';
    avatar.appendChild(avatarImg);
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const textP = document.createElement('p');
    textP.textContent = text;
    textP.style.marginBottom = '12px';
    
    const img = document.createElement('img');
    img.src = imageData;
    img.style.maxWidth = '100%';
    img.style.borderRadius = '12px';
    img.style.marginTop = '8px';
    img.style.border = '2px solid rgba(139, 92, 246, 0.5)';
    
    contentDiv.appendChild(textP);
    contentDiv.appendChild(img);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
    
    scrollToBottom();
}

function showTypingIndicator() {
    typingIndicator.style.display = 'block';
    scrollToBottom();
}

function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

function scrollToBottom() {
    setTimeout(() => {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }, 100);
}

function updateStatus(status) {
    const statusMap = {
        'connected': { text: '● Connected', color: '#10b981' },
        'disconnected': { text: '● Disconnected', color: '#ef4444' },
        'error': { text: '● Error', color: '#f59e0b' }
    };
    
    const config = statusMap[status] || statusMap.connected;
    statusIndicator.textContent = config.text;
    statusIndicator.style.color = config.color;
}

function createWelcomeMessage() {
    const welcomeDiv = document.createElement('div');
    welcomeDiv.className = 'welcome-message';
    welcomeDiv.id = 'welcomeMessage';
    welcomeDiv.innerHTML = `
        <div class="welcome-avatar-container">
            <div class="avatar-glow"></div>
            <img src="assets/logo.png" alt="Animexia" class="welcome-avatar-img">
        </div>
        <h2 class="glitch-text" data-text="Konnichiwa!">Konnichiwa!</h2>
        <h3>Welcome back to Animexia AI! 🌸</h3>
        <p class="welcome-description">Ready to explore the anime universe together!</p>
        <div class="suggestions">
            <button class="suggestion-btn glow-btn" onclick="quickSend('Recommend me an epic action anime')">
                <span class="btn-icon">⚔️</span>
                <span>Action Anime</span>
            </button>
            <button class="suggestion-btn glow-btn" onclick="quickSend('What are the best romance manga?')">
                <span class="btn-icon">💕</span>
                <span>Romance Manga</span>
            </button>
        </div>
    `;
    return welcomeDiv;
}

function quickSend(message) {
    userInput.value = message;
    handleSend();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'rgba(16, 185, 129, 0.9)' : 
                      type === 'error' ? 'rgba(239, 68, 68, 0.9)' :
                      type === 'warning' ? 'rgba(245, 158, 11, 0.9)' : 
                      'rgba(139, 92, 246, 0.9)'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        z-index: 9999;
        font-weight: 500;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Check backend on load
async function checkBackend() {
    try {
        const response = await fetch('http://localhost:5000/health');
        if (response.ok) {
            updateStatus('connected');
        } else {
            updateStatus('disconnected');
        }
    } catch (error) {
        updateStatus('disconnected');
    }
}

checkBackend();

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeOut {
        from { opacity: 1; transform: translateY(0); }
        to { opacity: 0; transform: translateY(-20px); }
    }
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
`;
document.head.appendChild(style);
