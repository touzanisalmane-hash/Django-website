// Logic for the floating NOVA Assistant chat widget.
document.addEventListener('DOMContentLoaded', function () {
    const widget = document.getElementById('chatbot-widget');
    const toggleBtn = document.getElementById('chatbot-toggle');
    const iconChat = document.getElementById('chatbot-icon-chat');
    const iconClose = document.getElementById('chatbot-icon-close');
    const panel = document.getElementById('chatbot-panel');
    const messagesBox = document.getElementById('chatbot-messages');
    const form = document.getElementById('chatbot-form');
    const input = document.getElementById('chatbot-input');
    const clearBtn = document.getElementById('chatbot-clear');
    const statusLine = document.getElementById('chatbot-status');

    function getCsrfToken() {
        const field = form.querySelector('input[name="csrfmiddlewaretoken"]');
        return field ? field.value : '';
    }

    function addMessage(text, sender) {
        const msg = document.createElement('div');
        msg.className = 'chatbot-msg chatbot-msg-' + sender;
        msg.textContent = text;
        messagesBox.appendChild(msg);
        messagesBox.scrollTop = messagesBox.scrollHeight;
        return msg;
    }

    toggleBtn.addEventListener('click', function () {
        const isOpen = widget.classList.toggle('chatbot-open');
        iconChat.style.display = isOpen ? 'none' : 'block';
        iconClose.style.display = isOpen ? 'block' : 'none';
        if (isOpen) {
            input.focus();
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const text = input.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        input.value = '';
        input.disabled = true;
        statusLine.textContent = 'Thinking...';
        const typingMsg = addMessage('...', 'bot');

        fetch('/chatbot/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
            },
            body: JSON.stringify({ message: text }),
        })
            .then(function (response) { return response.json(); })
            .then(function (data) {
                typingMsg.textContent = data.reply || data.error || 'Something went wrong.';
            })
            .catch(function () {
                typingMsg.textContent = 'Connection error. Please try again.';
            })
            .finally(function () {
                input.disabled = false;
                statusLine.textContent = 'Ask me about our products';
                input.focus();
            });
    });

    clearBtn.addEventListener('click', function () {
        fetch('/chatbot/api/reset/', {
            method: 'POST',
            headers: { 'X-CSRFToken': getCsrfToken() },
        }).finally(function () {
            messagesBox.innerHTML = '';
            addMessage("Hi! I'm the NOVA STORE assistant. Ask me about our products, stock, or prices.", 'bot');
        });
    });
});
