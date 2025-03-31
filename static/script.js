document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('message-form');
    const errorDiv = document.getElementById('error-alert');

    if (window.location.hash) {
        const messageElement = document.querySelector(window.location.hash);
        if (messageElement) {
            messageElement.scrollIntoView();
            messageElement.classList.add('highlight');
        }
    }

    document.querySelectorAll('.copy-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const messageId = this.getAttribute('data-message-id');
            const messageUrl = `${window.location.origin}/message/${messageId}`;
            
            navigator.clipboard.writeText(messageUrl).then(() => {
                const tooltip = document.createElement('div');
                tooltip.textContent = 'Link copied!';
                tooltip.style.position = 'absolute';
                tooltip.style.background = '#333';
                tooltip.style.color = '#fff';
                tooltip.style.padding = '5px 10px';
                tooltip.style.borderRadius = '4px';
                tooltip.style.fontSize = '12px';
                tooltip.style.top = `${this.getBoundingClientRect().top - 30}px`;
                tooltip.style.left = `${this.getBoundingClientRect().left}px`;
                document.body.appendChild(tooltip);
                
                setTimeout(() => {
                    document.body.removeChild(tooltip);
                }, 2000);
            });
        });
    });

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const response = await fetch('/', {
                method: 'POST',
                body: new FormData(form)
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const data = await response.json();
                if (data.error) {
                    showError(data.error);
                }
            }
        });
    }

    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

function scrollToBottom() {
    const messagesBox = document.getElementById('messages-box');
    messagesBox.scrollTop = messagesBox.scrollHeight;
}

function updateMessages() {
    fetch('/get_messages')
        .then(response => response.json())
        .then(data => {
            const messagesBox = document.getElementById('messages-box');
            const currentMessages = Array.from(messagesBox.children).map(el => el.id);
            const newMessages = data.messages.filter(msg => 
                !currentMessages.includes(`message-${msg.id}`)
            );

            if (newMessages.length > 0) {
                newMessages.reverse().forEach(message => {
                    const html = `
                    <div class="message" id="message-${message.id}">
                        <div class="message-header">
                            <small class="nickname">${message.nickname}</small>
                            <div class="message-actions">
                                <a href="/message/${message.id}" class="copy-link" 
                                   title="Copy message link" 
                                   data-message-id="${message.id}">
                                    <i class="fas fa-paperclip"></i>
                                </a>
                            </div>
                        </div>
                        <p class="text">${message.message}</p>
                    </div>`;
                    messagesBox.insertAdjacentHTML('afterbegin', html);
                });
                scrollToBottom();
            }
        })
        .catch(error => console.error('Error fetching messages:', error));
}
document.getElementById('message-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const form = this;
    const submitButton = form.querySelector('button[type="submit"]');
    const errorDiv = document.getElementById('error-alert');

    submitButton.disabled = true;
    submitButton.innerHTML = 'Sending... <i class="fas fa-spinner fa-spin"></i>';

    try {
        const response = await fetch('/', {
            method: 'POST',
            body: new FormData(form)
        });

        if (response.ok) {
            window.location.reload();
        } else {
            const data = await response.json();
            showError(data.error || 'Unknown error occurred');
        }
    } catch (error) {
        showError('Network error. Please try again.');
    } finally {
        setTimeout(() => {
            submitButton.disabled = false;
            submitButton.innerHTML = 'Send <i class="fas fa-paper-plane"></i>';
        }, 2000);
    }
});

function showError(message) {
    const errorDiv = document.getElementById('error-alert');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    
    setTimeout(() => {
        errorDiv.style.display = 'none';
    }, 5000);
}
