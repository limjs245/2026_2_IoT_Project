const speechText = document.getElementById('speechText');
const happiness = document.getElementById('happinessStatusValue');
const fullness = document.getElementById('fullnessStatusValue');

let happinessValue = 50;
let fullnessValue = 50;

fullness.style.width = fullnessValue + "%";
happiness.style.width = happinessValue + "%";

setInterval(function() {
    fetch('/get_input')
        .then(res => res.json())
        .then(data => {
            if (data.feedBtn) {
                fullnessValue += 10;
                if (fullnessValue > 100) fullnessValue = 100;
            }
            if (data.touchBtn) {
                happinessValue += 10;
                if (happinessValue > 100) happinessValue = 100;
            }
            if (data.isNear) {
                speechText.textContent = "Hello!";
            } else {
                speechText.textContent = "";
            }
            
            fullness.style.width = fullnessValue + "%";
            happiness.style.width = happinessValue + "%";
        })
        .catch(e => console.error("error:", e));
}, 1000);


setInterval(function() {
    if (fullnessValue > 0) fullnessValue -= 1;
    if (happinessValue > 0) happinessValue -= 1;
    
    fullness.style.width = fullnessValue + "%";
    happiness.style.width = happinessValue + "%";
}, 1000);