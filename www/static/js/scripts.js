function toggleDarkMode() {
    let element = document.body;
    element.classList.toggle("dark");

    let contactBox = document.querySelector(".contact-us-box");
    contactBox.classList.toggle("dark");


    let contactBoxButton = contactBox.querySelector("button");
    contactBoxButton.classList.toggle("dark");

    let closeButton = contactBox.querySelector(".contact-us-box button.cancel");
    closeButton.classList.toggle("dark");
  }

function hamburger() {
      var x = document.getElementById("myTopnav");
      if (x.className === "topnav") {
          x.className += " responsive";
      } else {
          x.className = "topnav";
      }
  }

  function openPop() {             /* popup https://www.geeksforgeeks.org/how-to-open-a-popup-on-click-using-javascript/-->> */

    const popupDialogue =
        document.getElementById(
            "popupDialogue"
        );
    popupDialogue.style.visibility =
        popupDialogue.style.visibility ===
            "visible"
            ? "hidden"
            : "visible"

}

let slideIndex = 1;
window.onload = function(){
    showSlides(slideIndex);
}

//gotten fromhttps://www.w3schools.com/howto/howto_js_slideshow.asp

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].className += " active";
}