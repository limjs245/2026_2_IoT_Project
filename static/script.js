const speechText = document.getElementById('speechText');
const happiness = document.getElementById('happinessStatusValue');
const fullness = document.getElementById('fullnessStatusValue');
const cleanliness = document.getElementById('cleanlinessStatusValue');
const condition = document.getElementById('condition');
const happinessText = document.getElementById('happinessStatusValueText');
const fullnessText = document.getElementById('fullnessStatusValueText');
const cleanlinessText = document.getElementById('cleanlinessStatusValueText');

let happinessValue = 50;
let fullnessValue = 50;
let cleanlinessValue = 50;
let isEating = false;
let isTouching = false;
let isWashing = false;
let currentIsNear = false;
let eatTimeout = null;
let heartTimeout = null;
let washTimeout = null;

function updateCondition() {
    if (isEating) {
        condition.className = "eat";
    } else if (isTouching) {
        condition.className = "heart";
    } else if (isWashing) {
        condition.className = "wash";
    } else if (currentIsNear) {
        condition.className = "speak";
    } else {
        condition.className = "default";
    }
}

function updateStatus() {
    fullness.style.width = fullnessValue + "%";
    fullnessText.textContent = fullnessValue + "%";
    happiness.style.width = happinessValue + "%";
    happinessText.textContent = happinessValue + "%";
    cleanliness.style.width = cleanlinessValue + "%";
    cleanlinessText.textContent = cleanlinessValue + "%";
}
updateStatus();
updateCondition();

setInterval(function() {
    fetch('/get_input/h')
        .then(res => res.json())
        .then(data => {
            currentIsNear = data.isNear;
            if (data.feedBtn) {
                fullnessValue += 10;
                if (fullnessValue > 100) fullnessValue = 100;
                isEating = true;

                clearTimeout(eatTimeout);
                eatTimeout = setTimeout(() => {
                    isEating = false;
                    updateCondition();
                }, 3000);
            }
            if (data.touchBtn) {
                happinessValue += 10;
                if (happinessValue > 100) happinessValue = 100;
                isTouching = true;

                clearTimeout(heartTimeout);
                heartTimeout = setTimeout(() => {
                    isTouching = false;
                    updateCondition();
                }, 3000);
            }
            if (data.washBtn) {
                cleanlinessValue += 10;
                if (cleanlinessValue > 100) cleanlinessValue = 100;
                isWashing = true;

                clearTimeout(washTimeout);
                washTimeout = setTimeout(() => {
                    isWashing = false;
                    updateCondition();
                }, 3000);
            }
            if (currentIsNear) {
                speechText.textContent = "Hello!";
            } else {
                speechText.textContent = "";
            }
            
            updateCondition();
            updateStatus();
        })
        .catch(e => console.error("error:", e));
}, 1000);


setInterval(function() {
    if (fullnessValue > 0) fullnessValue -= 1;
    
    updateStatus();
}, 3000);

setInterval(function() {
    if (happinessValue > 0) happinessValue -= 1;
    
    updateStatus();
}, 5000);

setInterval(function() {
    if (cleanlinessValue > 0) cleanlinessValue -= 1;
    
    updateStatus();
}, 4000);