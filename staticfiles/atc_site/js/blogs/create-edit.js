

function submitStepOne() {
    var title = document.querySelector('input[name="title"]').value;
    var description = document.getElementById('textbox').value;


    if (!title || !description) {
        alert('Inputs cannot be empty');
    } else {
        nextPrev(1);
    }
}

function submitStepTwo() {
    var content = document.getElementById('textbox').value;

    if (!content) {
        alert('Input cannot be empty');
    } else {
        nextPrev(1);
    }
}

function submitStepThree() {
    document.getElementById("title-confirm").value = document.querySelector('input[name="title"]').value;
    document.getElementById("description-confirm").value = document.getElementById('textbox').value;
    document.getElementById("content-confirm").value = document.getElementById('textbox-2').value;
    if (document.querySelector('input[name="image"]').files[0] == undefined) {
        if (document.getElementById("image-current") == undefined) {
            alert("No image uploaded. Using AI generated image.");
            document.getElementById("image-confirm").value = "No image uploaded. Using AI generated image.";
        } else {
            document.getElementById("image-confirm").value = document.getElementById("image-current").value;
        }
    } else {
        document.getElementById("image-confirm").value = document.querySelector('input[name="image"]').files[0].name;
    }
    nextPrev(1);
}





var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

function showTab(n) {
    // This function will display the specified tab of the form...
    var x = document.getElementsByClassName("tab");
    x[n].style.display = "block";
    //... and fix the Previous/Next buttons:
    if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
    } else {
    document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    } else {
    document.getElementById("nextBtn").innerHTML = "Next";
    }

    //... and run a function that will display the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tab");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    x[currentTab].style.display = "none";
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form...
    if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
    }
    if (currentTab > 1) {
        $("#progressbar li").eq(currentTab).addClass("active"); //works?
    } else {
        if (n>= 1) {
            if (currentTab == 1) {
                $("#progressbar li").eq(n).addClass("active"); //works?
            }
        }
        else {
            $("#progressbar li").eq(currentTab+1).removeClass("active");
        }
    }
    showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, y, i, valid = true;
    x = document.getElementsByClassName("tab");
    y = x[currentTab].getElementsByTagName("input");
    // A loop that checks every input field in the current tab:
    for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
        if (currentTab == 0) {
        // add an "invalid" class to the field:
        y[i].className += " invalid";
        // and set the current valid status to false
        valid = false;
        }
        else {
        // add an "invalid" class to the field:
        y[i].className += " valid";
        // and set the current valid status to false
        valid = true;
        }
    }
    }
    // If the valid status is true, mark the step as finished and valid:
    if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

// function fixStepIndicator(n) {
//     // This function removes the "active" class of all steps...
//     var i, x = document.getElementsByClassName("step");
//     for (i = 0; i < x.length; i++) {
//     x[i].className = x[i].className.replace(" active", "");
//     }
//     //... and adds the "active" class on the current step:
//     x[n].className += " active";
// }
$('#nextBtn').click(function(){
    $('form').animate({height: "toggle", opacity: "toggle"}, 100000);
}); 

const textbox = document.getElementById("textbox");
const charCount = document.getElementById("char_count");

textbox.addEventListener("input", () => {
  let remainingChars = 100 - textbox.value.length;
  if (remainingChars < 0) {
    remainingChars = 0;
  }
  charCount.textContent = `${remainingChars}/100`;
});

