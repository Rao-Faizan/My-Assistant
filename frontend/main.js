$(document).ready(function () {

    // Text animation for static welcome text
    $('.text').textillate({
        loop: true,
        sync: true,
        in: { effect: "bounceIn" },
        out: { effect: "bounceOut" }
    });

    // SiriWave animation setup
    var siriWave = new SiriWave({
        container: document.getElementById("siri-container"),
        width: 800,
        height: 200,
        style: "ios9",
        amplitude: "2",
        speed: "0.10",
        autostart: true
    });

    // Siri message animation
    $('.siri-message').textillate({
        loop: true,
        sync: true,
        in: { effect: "fadeInUp", sync: true },
        out: { effect: "fadeOutUp", sync: true },
    });

    // 🎙️ Mic button clicked
    $("#mic-btn").click(function () {
        eel.playAssistantSound();
        $("#oval").attr("hidden", true);
        $("#SiriWave").attr("hidden", false);
        eel.allCommands();  // Voice input mode
    });

    // ⌨️ Shortcut: Windows + J / CMD + J
    function keyUp(e) {
        if (e.key === 'j' && e.metaKey) {
            eel.playAssistantSound();
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);
            eel.allCommands();  // Voice input
        }
    }
    document.addEventListener('keyup', keyUp, false);

    // 🧠 Handle text input message
    function PlayAssistant(message) {
        if (message !== "") {
            $("#oval").attr("hidden", true);
            $("#SiriWave").attr("hidden", false);

            try {
                eel.allCommands(message);  // Pass message to Python
            } catch (error) {
                console.error("Error calling allCommands():", error);
            }

            $("#chatbox").val("");
            $("#mic-btn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        }
    }

    // 🔁 Toggle mic/send button
    function ShowHideButton(message) {
        if (message.length === 0) {
            $("#mic-btn").attr('hidden', false);
            $("#SendBtn").attr('hidden', true);
        } else {
            $("#mic-btn").attr('hidden', true);
            $("#SendBtn").attr('hidden', false);
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
        eel.processUserMessage(msg);  // <-- Send to Python
        $("#chatbox").val(""); // Clear after sending
    }
});


    // ⏎ Enter key pressed
  $("#chatbox").keypress(function (e) {
    if (e.which === 13) {
        $("#SendBtn").click();
    }
    
});

});
