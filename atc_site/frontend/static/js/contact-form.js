$(function () {

    $("#contactForm input, #contactForm textarea").jqBootstrapValidation({
        preventSubmit: true,
        submitError: function ($form, event, errors) {},
        submitSuccess: function ($form, event) {
            event.preventDefault();
            var name = $("input#name").val();
            var email = $("input#email").val();
            var subject = $("input#subject").val();
            var message = $("textarea#message").val();


            $("#sendMessageButton").prop("disabled", true);
            $("#sendMessageButton span").text("SENDING...");
            $("#sendMessageButton div").removeClass("d-none");

            fetch('/handle-contact-request', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    subject: subject,
                    message: message
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response from the server
                $('#alertMessage').html("<div class='alert alert-success alert-dismissible'>");
                $('#alertMessage > .alert-success').html("<button type='button' class='btn-close' data-bs-dismiss='alert' aria-hidden='true'>").append("</button>");
                $('#alertMessage > .alert-success').append("<strong>" + name + ", your message has been sent. </strong>");
                $('#alertMessage > .alert-success').append('</div>');
                $('#contactForm').trigger("reset");
            })
            .catch((error) => {
                console.error('Error:', error);
                // Display error message
                $('#alertMessage').html("<div class='alert alert-danger alert-dismissible'>");
                $('#alertMessage > .alert-danger').html("<button type='button' class='btn-close' data-bs-dismiss='alert' aria-hidden='true'>").append("</button>");
                $('#alertMessage > .alert-danger').append($("<strong>").text("Sorry " + name + ", it seems that our mail server is not responding. Please try again later!"));
                $('#alertMessage > .alert-danger').append('</div>');
            })
            .finally(() => {
                $("#sendMessageButton").prop("disabled", false);
                $("#sendMessageButton span").text("SEND");
                $("#sendMessageButton div").addClass("d-none");
            });            
        },
    });
});

$('#name, #email, #subject, #message').focus(function () {
    $('#alertMessage').html('');
});