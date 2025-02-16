const home_button = document.getElementById("logo");
home_button.addEventListener("click", function() {
    window.location.href = "index.html";
});

const restart = document.getElementById("restart");
restart.addEventListener("click", function(){
    window.location.href = "default.html";
});


const closeModalButton = document.getElementById("closeModalButton");
const cancelExitButton = document.getElementById("cancelExitButton");
const confirmExitButton = document.getElementById("confirmExitButton");
const change = document.getElementById("switch");
change.addEventListener("click", function (){
    modal.style.display = "block";
});

closeModalButton.addEventListener("click", function() {
    modal.style.display = "none"; 
});

cancelExitButton.addEventListener("click", function() {
    modal.style.display = "none"; 
});


confirmExitButton.addEventListener("click", function() {
    window.location.href = "index.html";
    modal.style.display = "none"; 
});

window.addEventListener("click", function(event) {
    if (event.target === modal) {
        modal.style.display = "none"; 
    }
});