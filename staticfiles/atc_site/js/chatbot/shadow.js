// Import the tinycolor2 library
import tinycolor from "tinycolor2";

// Get the background color of the header
let bgColor = $('.Messenger_header').css('background-color');

// Use tinycolor to determine if the color is dark or light
if (tinycolor(bgColor).isDark()) {
    // If the color is dark, add a light shadow
    $('.Messenger_header').css('box-shadow', '0px 0px 10px #fff');
} else {
    // If the color is light, add a dark shadow
    $('.Messenger_header').css('box-shadow', '0px 0px 10px #000');
}