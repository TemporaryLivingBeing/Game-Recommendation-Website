function toggleDarkMode() {
    let element = document.body;
    element.classList.toggle("dark");
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