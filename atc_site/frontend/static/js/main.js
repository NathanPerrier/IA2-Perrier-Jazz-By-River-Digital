
$(document).ready(function(){
    $(window).scroll(function(){
        var scroll = $(window).scrollTop();
        if (scroll > 100) {
          $(".netflix-navbar").css("background" , "#0C0C0C");
        }
  
        else{
            $(".netflix-navbar").css("background" , "transparent");  	
        }
    });

  })


function position(id){
  var card = document.getElementsByClassName('weather-card')[id];
  // card.style.transform = 'scale(1.5)';
  console.log(id)
}

// Get all nav links
var navLinks = document.querySelectorAll('#sidebar .navbar-item .nav-link');

// Get current URL
var currentUrl = window.location.href;

navLinks.forEach(function(link) {
    // Check if the nav link's href matches the current URL
    if (link.href === currentUrl) {
        // Add the 'active' class
        link.classList.add('active');
    } else {
        // Remove the 'active' class
        link.classList.remove('active');
    }
});