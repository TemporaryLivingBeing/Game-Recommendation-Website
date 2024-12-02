function toggleDarkMode() {
    let i = document.getElementById("sunMoon");
    
    if (i.classList.contains('fa-sun')) {
        i.classList.replace('fa-sun', 'fa-moon');
    } else {
        i.classList.replace('fa-moon', 'fa-sun');
    }

    let element = document.body;
    element.classList.toggle("dark");

    if (localStorage.getItem('dark') === 'TRUE') {
      localStorage.setItem('dark', 'FALSE');
    } else {
      localStorage.setItem('dark', 'TRUE');
    }   
    console.log(localStorage.getItem('dark')); 
  }

function hamburger() {
      var x = document.getElementById("myTopnav");
      if (x.className === "topnav") {
          x.className += " responsive";
      } else {
          x.className = "topnav";
      }
}

function searchGames() {
  var searchText = document.getElementById('gameSearch').value.toLowerCase();
  filteredGames = [];
  
  for (var i = 0; i < allGames.length; i++) {
      if (allGames[i].toLowerCase().includes(searchText)) {
          filteredGames.push(allGames[i]);
      }
  }
  updateGameSelect();
}  

function updateGameSelect() {
  var select = document.getElementById('gameSelect');
  
  var startIndex = (currentPage - 1) * gamesPerPage;
  var endIndex = Math.min(startIndex + gamesPerPage, filteredGames.length);
  
  select.innerHTML = '';
  for (var i = startIndex; i < endIndex; i++) {
      var option = document.createElement('option');
      option.value = filteredGames[i];
      option.textContent = filteredGames[i];
      select.appendChild(option);
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