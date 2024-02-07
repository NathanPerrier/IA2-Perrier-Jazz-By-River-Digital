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

    // timedate
    var timedate = function () {
        setTimeout(function () {
            var timedateElement = $('#timedate');
            if (timedateElement.text() > 0) {
                timedateElement.addClass('wow slideInLeft');
            }
        }, 1000); // Delay of 1 second
    };
    timedate();

    // Initiate the wowjs
    new WOW().init();

})(jQuery);