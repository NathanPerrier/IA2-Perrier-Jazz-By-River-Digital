
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function resetMessages() {
    fetch('/chat/reset/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'), 
        },
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); 
    })
};

window.addEventListener('load', function() {
    resetMessages();
});

$(document).ready(function(){
    $(".chat_on").click(function(){
        $(".Layout").toggle();
        $(".chat_on").hide(300);
    });
    
        $(".chat_close_icon").click(function(){
        console.log("clicked");
        $(".Layout").hide();
            $(".chat_on").show(300);
    });
    
});

$(document).click(function(event) {
    // Check if the clicked target is not the chatbox, not a descendant of the chatbox, and not the .chat_on button
    if (!$(event.target).closest('.Layout').length && !$(event.target).closest('.chat_on').length) {
        // Hide the chatbox
        $(".Layout").hide();
        $(".chat_on").show(300);
    }
});

var requestInProgress = false;

$('.Input_button-send').click(function() {
    if (requestInProgress) {
    $('.Input_field').val('');
    return;
    }

    var userMessage = $('.Input_field').val();

    // Check if the input field is not empty
    if(userMessage.trim() === '') {
        alert('Please enter a message.');
        return;
    }

    $('.Input_field').val(''); // Clear the input field
    $('.Messages_list').append('<div class="d-flex flex-row p-1 py-2"><div class="bg-white message ml-2 p-3"><small>You</small><br>' + userMessage + '</div></div>');

    requestInProgress = true;

    $.ajax({
        url: '/chat/',  // The URL to chat endpoint
        method: 'POST',
        data: {
            message: userMessage,
        },
        success: function(response) {
            // Add chatbot Message
            $('.Messages_list').append('<div class="d-flex flex-row p-1"><div class="chat message mr-2 p-3"><small>Genie</small><br>' + response.message + '</div></div>');
        },
        complete: function() {
        requestInProgress = false;
        }
    });
});

$('.Input_field').keypress(function(e) {
if(e.which == 13) { // Enter key pressed
    $('.Input_button-send').click(); // Trigger the button click event
}
});

function SelectModel() {
requestInProgress = true;

var model = document.getElementById('modelSelect').value;
var model_user = document.getElementById(model).innerHTML;

$.ajax({
    url: '/chat/change_model/',  // The URL to your chat endpoint
    method: 'POST',
    data: {
        model: model,
    },
    success: function(response) {
        // This is where you handle the chatbot's response
        $('.Messages_list').append('<div class="d-flex flex-row p-1"><div class="chat message mr-2 p-3"><small>Genie</small><br>You are now using the ' + model_user + ' model</div></div>');
    },
    complete: function() {
    // Set the flag back to false to indicate that the request is complete
    requestInProgress = false;
    }
});
}
