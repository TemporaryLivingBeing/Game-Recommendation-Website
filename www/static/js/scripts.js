function toggleDarkMode() {
    let element = document.body;
    element.classList.toggle("dark");
}

document.addEventListener("DOMContentLoaded", autoSwitchMode);

