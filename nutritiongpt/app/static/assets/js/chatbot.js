function getCurrentTimeString() {
    var now = new Date();
    var hours = now.getHours();
    var minutes = now.getMinutes();

    if (minutes < 10) {
        minutes = '0' + minutes;
    }

    return hours + ':' + minutes;
}

function createUserMessageElement(message, timestamp) {
    return `
        <div class="media flex-row-reverse chat-right">
            <div class="main-img-user online"><img alt="avatar" src="{% static '/assets/images/users/21.jpg' %}"></div>
            <div class="media-body">
                <div class="main-msg-wrapper">${message}</div>
                <div>
                    <span>${timestamp}</span> <a href="{% static 'javascript:void(0)' %}"><i class="icon ion-android-more-horizontal"></i></a>
                </div>
            </div>
        </div>`;
}

function createBotResponseElement(response, timestamp) {
    return `
        <div class="media chat-left">
            <div class="main-img-user online"><img alt="avatar" src="{% static '/images/users/1.jpg' %}"></div>
            <div class="media-body">
                <div class="main-msg-wrapper">${response}</div>
                <div>
                    <span>${timestamp}</span> <a href="{% static 'javascript:void(0)' %}"><i class="icon ion-android-more-horizontal"></i></a>
                </div>
            </div>
        </div>`;
}

function displayInitialBotMessage() {
    const botInitialMessage = `
        <div class="media chat-left">
            <div class="main-img-user online"><img alt="avatar" src="{% static '/assets/images/users/1.jpg' %}"></div>
            <div class="media-body">
                <div class="main-msg-wrapper" id="bot-response">
                    I am a bot. I am here to help you. How may I help you?
                </div>
                <div>
                    <span>${getCurrentTimeString()}</span> <a href="{% static 'javascript:void(0)' %}"><i class="icon ion-android-more-horizontal"></i></a>
                </div>
            </div>
        </div>`;
    $('#ChatBody .content-inner').append(botInitialMessage);
}

function createTypingIndicatorElement() {
    return `
        <div class="media chat-left typing-indicator-wrapper">
            <div class="main-img-user online"><img alt="avatar" src="{% static '/assets/images/users/1.jpg' %}"></div>
            <div class="media-body">
                <div class="main-msg-wrapper">
                    <div class="typing-indicator"></div>
                </div>
            </div>
        </div>`;
}

$(document).ready(function() {
    displayInitialBotMessage();

    $("#send-message").click(function() {
        var message = $("#user-message").val();
        $("#user-message").val(""); // Clear the input field
        var timestamp = getCurrentTimeString();

        // Append the user message to the chat body
        var userMessageElement = createUserMessageElement(message, timestamp);
        $("#ChatBody .content-inner").append(userMessageElement);

        // Show the typing indicator
        var typingIndicatorElement = createTypingIndicatorElement();
        $("#ChatBody .content-inner").append(typingIndicatorElement);

        // Disable the send button and input field while waiting for a response
        $("#send-message").prop("disabled", true);
        $("#user-message").prop("disabled", true);

        $.ajax({
            url: '{% url "chatbot_response" %}',
            method: 'POST',
            data: {
                'message': message,
                'csrfmiddlewaretoken': '{{ csrf_token }}',
            },
            success: function(response) {
                // Remove the typing indicator
                $(".typing-indicator-wrapper").remove();

                // Append the bot response to the chat body
                var botResponseElement = createBotResponseElement(response.response, timestamp);
                $("#ChatBody .content-inner").append(botResponseElement);

                // Re-enable the send button and input field
                $("#send-message").prop("disabled", false);
                $("#user-message").prop("disabled", false);
            },
            error: function() {
                // Remove the typing indicator
                $(".typing-indicator-wrapper").remove();

                alert("An error occurred. Please try again.");

                // Re-enable the send button and input field
                $("#send-message").prop("disabled", false);
                $("#user-message").prop("disabled", false);
            }
        })
    });
    
});