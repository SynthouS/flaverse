
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