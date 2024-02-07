(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Initiate the wowjs
    new WOW().init();


    // parallax video
    document.addEventListener('scroll', function() {
        const image = document.getElementById('parallaxVideo');
        const scrolled = window.scrollY;
        
        const scaleFactor = 1 + (scrolled * 0.0005);
        const top = -50 - scaleFactor;
        
        image.style.transform = `translate3d(0, ${scrolled * -0.6}px, 0) scale(${scaleFactor * 1.25})`;
        image.style.transform = `tranlateY(${top}px)`;
      });
      


    // Sticky Navbar
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.sticky-top').addClass('bg-white shadow-sm py-1').css('top', '0px');
            $('.nav-link').removeClass('text-light').css('top', '0px');
            $('.nav-link').addClass('text-primary').css('top', '0px');
            $('.account').removeClass('text-light').css('top', '0px');
            $('.account').addClass('text-primary').css('top', '0px');
            $('.login-button').addClass('text-primary border-primary').css('top', '0px');
            $('.register-button').addClass('text-white bg-primary border-primary').css('top', '0px');
            $('.navbar-toggler-icon').removeClass('navbar-toggler-icon-light').css('top', '0px');
            $('.navbar-toggler-icon').addClass('navbar-toggler-icon-dark').css('top', '0px');
        } else {
            // only appears when user scrolls up
            $('.sticky-top').removeClass('bg-white shadow-sm py-1').css('top', '-150px');
            $('.nav-link').removeClass('text-primary').css('top', '-150px');
            $('.nav-link').addClass('text-light').css('top', '0px');
            $('.account').removeClass('text-primary').css('top', '-150px');
            $('.account').addClass('text-light').css('top', '0px');
            $('.login-button').removeClass('text-primary border-primary').css('top', '-150px');
            $('.register-button').removeClass('text-white bg-primary border-primary').css('top', '-1500px');
            $('.navbar-toggler-icon').removeClass('navbar-toggler-icon-dark').css('top', '-150px');  
            $('.navbar-toggler-icon').addClass('navbar-toggler-icon-light').css('top', '-150px');  
        }
    });
    $(window).scroll(function () {
        if ($(this).scrollTop() == 0) {
            $('.home-link').removeClass('bi-house').css('top', '0px');
            $('.home-link').addClass('bi-arrow-down').css('top', '0px');
        } else {
            $('.home-link').removeClass('bi-arrow-down').css('top', '1px');  
            $('.home-link').addClass('bi-house').css('top', '1px');
        }

    });
    

    // Facts counter
    $('[data-toggle="counter-up"]').counterUp({
        delay: 10,
        time: 2000
    });
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 150) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        items: 1,
        autoplay: true,
        smartSpeed: 2000,
        dots: false,
        loop: true,
        nav: false,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

     // Testimonials carousel
     $(".recommended-carousel").owlCarousel({
        items: 3,
        autoplay: true,
        smartSpeed: 2000,
        dots: false,
        loop: true,
        nav: false,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });

    // Testimonials carousel
    $(".testimonial-carousel-long").owlCarousel({
        items: 1,
        autoplay: true,
        smartSpeed: 1500,
        duration: 6000,
        dots: true,
        loop: true,
        nav: true,
        navText : [
            '<i class="bi bi-chevron-left"></i>',
            '<i class="bi bi-chevron-right"></i>'
        ]
    });
    
})(jQuery);

