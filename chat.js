const socket = new WebSocket("ws://localhost:8080/ws");

socket.onopen = function(e) {
    console.log("Connection established!");
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.action === "message") {
        const chatMessages = document.getElementById("chat-messages");
        if (chatMessages) {
            chatMessages.innerHTML += `<div>${data.message}</div>`;
        }
    } else if (data.action === "register" && data.success) {
        alert("Registration successful. Please log in.");
        showLoginForm();
    } else if (data.action === "login") {
        if (data.success) {
            window.location.href = 'chat.html';
        } else {
            alert("Login failed. Please try again.");
        }
    }
};

function showLoginForm() {
    document.getElementById("register-form").style.display = "none";
    document.getElementById("login-form").style.display = "block";
}

function showRegisterForm() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
}

function register() {
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;
    socket.send(JSON.stringify({ action: "register", user: { username, password } }));
    sessionStorage.setItem("username", username);
}

function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    socket.send(JSON.stringify({ action: "login", user: { username, password } }));
    sessionStorage.setItem("username", username);
}

function sendChatMessage() {
    const messageInput = document.getElementById("chat-message");
    const message = messageInput.value;
    if (message) {
        // Получение имени пользователя из sessionStorage
        const username = sessionStorage.getItem("username");
        const fullMessage = username + ": " + message;
        socket.send(JSON.stringify({ action: "message", message: fullMessage }));
        messageInput.value = "";
    }
}

