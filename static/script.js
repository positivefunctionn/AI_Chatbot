
const chatBox = document.getElementById("chatBox");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const typing = document.getElementById("typing");
const clearBtn = document.getElementById("clearBtn");

function addMessage(message, sender) {
    const div = document.createElement("div");

    div.className = "message " + sender;
    div.textContent = message;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const message = userInput.value.trim();

    if (!message) return;

    addMessage(message, "user");
    userInput.value = "";

    sendBtn.disabled = true;
    typing.classList.remove("hidden");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Request failed");
        }

        addMessage(data.response, "bot");

    } catch (error) {
        addMessage("Error: " + error.message, "bot");

    } finally {
        typing.classList.add("hidden");
        sendBtn.disabled = false;
        userInput.focus();
    }
}

sendBtn.addEventListener("click", sendMessage);

userInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

clearBtn.addEventListener("click", async function() {
    try {
        const response = await fetch("/clear", {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Could not clear chat");
        }

        chatBox.innerHTML = "";

        addMessage("New conversation started!", "bot");

    } catch (error) {
        addMessage("Error: " + error.message, "bot");
    }
});
