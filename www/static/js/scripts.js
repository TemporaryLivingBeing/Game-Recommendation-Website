function toggleDarkMode() {
    let element = document.body;
    element.classList.toggle("dark");

    let contactBox = document.querySelector(".contact-us-box");
    contactBox.classList.toggle("dark");
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