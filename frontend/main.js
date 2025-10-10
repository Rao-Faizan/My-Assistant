$(document).ready(function () {
    console.log("AI Assistant Frontend Initialized");

    // Welcome message on startup
    setTimeout(() => {
        eel.send_welcome_message()(function(message) {
            if (message) {
                addMessage(message, false, "System");
            }
        });
    }, 1000);

    // 🎙️ Mic button clicked
    $("#mic-btn").click(function () {
        console.log("Mic button clicked");
        eel.playAssistantSound();
        eel.allCommands();  // Voice input mode
    });

    // 🧠 Handle text input message
    function PlayAssistant(message) {
        if (message !== "") {
            console.log("Sending message:", message);
            addMessage(message, true); // Show user message
            
            try {
                eel.allCommands(message);  // Send to Python backend
            } catch (error) {
                console.error("Error calling allCommands():", error);
                addMessage("Error: " + error.message, false, "Error");
            }
            $("#chatbox").val("");
        }
    }

    // 🔁 Toggle mic/send button
    function ShowHideButton(message) {
        if (message.length === 0) {
            $("#mic-btn").show();
            $("#SendBtn").hide();
        } else {
            $("#mic-btn").hide();
            $("#SendBtn").show();
        }
    }

    // Detect typing in chatbox
    $("#chatbox").keyup(function () {
        const message = $("#chatbox").val();
        ShowHideButton(message);
    });

    // 📤 Send button clicked
    $("#SendBtn").click(function () {
        const msg = $("#chatbox").val();
        if (msg.trim() !== "") {
            PlayAssistant(msg);
        }
    });

    // ⏎ Enter key pressed
    $("#chatbox").keypress(function (e) {
        if (e.which === 13) {
            $("#SendBtn").click();
        }
    });

    // =============================
    // 🟢 Functions exposed by Python
    // =============================

    // User message show in frontend
    eel.expose(senderText);
    function senderText(message) {
        console.log("User message:", message);
        addMessage(message, true);
    }

    // AI response show in frontend
    eel.expose(receiverText);
    function receiverText(message) {
        console.log("AI response:", message);
        addMessage(message, false, "AI Assistant");
    }

    // Add message to chat with proper formatting
    function addMessage(content, isUser = false, agentName = null) {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) {
            console.error("Chat messages container not found");
            return;
        }

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'assistant'} fade-in`;
        
        if (agentName && !isUser) {
            messageDiv.innerHTML = `<div class="agent-tag">${agentName}</div>${content}`;
        } else {
            messageDiv.textContent = content;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        if (!messagesContainer) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'message assistant typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="agent-tag">AI Assistant</div>
            <div class="typing-indicator">
                <span>Thinking</span>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Override the global DisplayMessage function
    window.DisplayMessage = function(message, isUser = false, agentName = null) {
        addMessage(message, isUser, agentName);
    };

    // Add some interactive effects
    $('.quick-action').hover(
        function() {
            $(this).css('transform', 'translateX(5px) scale(1.02)');
        },
        function() {
            $(this).css('transform', 'translateX(0) scale(1)');
        }
    );

    // Add click effect to buttons
    $('.btn').click(function() {
        $(this).css('transform', 'scale(0.95)');
        setTimeout(() => {
            $(this).css('transform', 'scale(1)');
        }, 150);
    });

    console.log("Frontend setup complete");
});