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

document.addEventListener("DOMContentLoaded", autoSwitchMode);

function hamburger() {
      var x = document.getElementById("myTopnav");
      if (x.className === "topnav") {
          x.className += " responsive";
      } else {
          x.className = "topnav";
      }
  }

function openPop() {
    const popDialogue =
        document.getElementById(
            "popupDialogue"
        );
    popDialogue.style.visibility =
        popDialogue.style.visibility ===
            "visible"
            ? "hidden"
            : "visible";
}