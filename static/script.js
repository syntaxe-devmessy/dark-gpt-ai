// Configuration
const API_URL = window.location.origin;

// État global
let modelLoaded = false;
let loadingStarted = false;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    checkStatus();
    setInterval(checkStatus, 10000);
    initEventListeners();
});

function initEventListeners() {
    // Bouton d'envoi
    const sendBtn = document.getElementById('send-btn');
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    // Entrée clavier
    const input = document.getElementById('user-input');
    if (input) {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
    }

    // Bouton effacer
    const clearBtn = document.getElementById('clear-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearChat);
    }

    // Suggestions
    document.querySelectorAll('.suggestion').forEach(btn => {
        btn.addEventListener('click', () => {
            const input = document.getElementById('user-input');
            input.value = btn.textContent;
            sendMessage();
        });
    });

    // Slider température
    const tempSlider = document.getElementById('temp');
    if (tempSlider) {
        tempSlider.addEventListener('input', () => {
            document.getElementById('temp-value').textContent = tempSlider.value;
        });
    }
}

async function checkStatus() {
    const statusEl = document.getElementById('status');
    if (!statusEl) return;

    try {
        const response = await fetch(`${API_URL}/api/status`);
        const data = await response.json();
        
        modelLoaded = data.loaded;
        loadingStarted = data.loading;
        
        if (modelLoaded) {
            statusEl.style.color = '#00ff00';
            statusEl.innerHTML = '● Prêt';
            statusEl.title = 'Modèle chargé';
        } else if (loadingStarted) {
            statusEl.style.color = '#ffaa00';
            statusEl.innerHTML = '● Chargement...';
            statusEl.title = 'Modèle en cours de chargement';
        } else {
            statusEl.style.color = '#ff4444';
            statusEl.innerHTML = '● Hors ligne';
            statusEl.title = 'Modèle non disponible';
        }
    } catch (error) {
        console.error('Erreur status:', error);
        statusEl.style.color = '#ff4444';
        statusEl.innerHTML = '● Erreur';
    }
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;

    // Afficher le message utilisateur
    addMessage(message, 'user');
    input.value = '';

    // Vérifier si le modèle est prêt
    if (!modelLoaded) {
        addMessage('⏳ Modèle en cours de chargement... Patientez quelques instants.', 'ai');
        return;
    }

    // Indicateur de chargement
    const loadingId = showLoading();

    try {
        const mode = document.getElementById('mode')?.value || 'general';
        const temperature = parseFloat(document.getElementById('temp')?.value || '0.7');
        const maxTokens = parseInt(document.getElementById('max-tokens')?.value || '500');

        const response = await fetch(`${API_URL}/api/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: message,
                mode: mode,
                temperature: temperature,
                max_tokens: maxTokens,
                top_p: 0.95
            })
        });

        const data = await response.json();
        
        removeLoading(loadingId);

        if (response.status === 202) {
            addMessage('⏳ Modèle en cours de chargement... Réessaie dans une minute.', 'ai');
        } else if (data.success) {
            addMessage(data.response, 'ai');
        } else {
            addMessage(`❌ Erreur: ${data.error || 'Erreur inconnue'}`, 'ai');
        }

    } catch (error) {
        removeLoading(loadingId);
        addMessage(`❌ Erreur de connexion: ${error.message}`, 'ai');
    }
}

function addMessage(text, sender) {
    const container = document.getElementById('messages');
    if (!container) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = sender === 'user' ? '👤' : '🤖';
    
    const content = document.createElement('div');
    content.className = 'content';
    
    // Formater le texte (urls, code, etc.)
    content.innerHTML = formatMessage(text);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
    
    container.appendChild(messageDiv);
    
    // Scroll vers le bas
    container.scrollTop = container.scrollHeight;
}

function formatMessage(text) {
    // Échapper le HTML
    text = escapeHtml(text);
    
    // Remplacer les URLs par des liens
    text = text.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
    
    // Remplacer les sauts de ligne
    text = text.replace(/\n/g, '<br>');
    
    return text;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading() {
    const container = document.getElementById('messages');
    if (!container) return '';

    const id = 'loading-' + Date.now();
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai';
    loadingDiv.id = id;
    
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = '🤖';
    
    const content = document.createElement('div');
    content.className = 'content';
    content.innerHTML = '<span class="loading"></span> Réflexion en cours...';
    
    loadingDiv.appendChild(avatar);
    loadingDiv.appendChild(content);
    
    container.appendChild(loadingDiv);
    container.scrollTop = container.scrollHeight;
    
    return id;
}

function removeLoading(id) {
    const loadingEl = document.getElementById(id);
    if (loadingEl) {
        loadingEl.remove();
    }
}

function clearChat() {
    const container = document.getElementById('messages');
    if (!container) return;

    container.innerHTML = `
        <div class="message ai">
            <div class="avatar">🤖</div>
            <div class="content">
                Bonjour ! Je suis Dark Gpt Ai, ton assistant sans censure basé sur Dolphin 2.9.1.
                Pose-moi des questions sur le code ou tout autre sujet !
            </div>
        </div>
    `;
}