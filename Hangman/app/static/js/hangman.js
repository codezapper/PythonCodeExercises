var mainCanvas = document.getElementById("gameCanvas");
var mainContext = mainCanvas.getContext("2d");
var gameIsRunning = true;
var animationId;
var currentMistakeIndex = 0;

var SCREEN_WIDTH = 800;
var SCREEN_HEIGHT = 480;
var X_MARGIN = 150;
var Y_MARGIN = 60;

var field = new Field();
var player = new Player(80, 50);
var maskedWord;

function startGame() {
    // fetch('http://localhost:5000/new_word')
    //     .then(response => response.json())
    //     .then(data => {
    //         maskedWord = new MaskedWord(Array(data.word_size).join("_"), 500, 50);
    //         document.addEventListener("keypress", keyPressHandler, false);
    //         drawAll();
    //     });
    drawAll();
}

function Score(value, initialX, initialY, initialDx, initialDy) {
    var thisScore = this;
    thisScore.value = value;
    thisScore.x = initialX;
    thisScore.y = initialY;

    thisScore.decrease = function() {
        thisScore.value--;
    }

    thisScore.draw = function() {
        mainContext.font = "50px Courier";
        mainContext.lineWidth = "1";
        mainContext.fillStyle = "#FFFFFF";
        mainContext.fillText(thisScore.value.toString(), thisScore.x, thisScore.y);
    }

    return thisScore;
}

function Field() {
    var theField = this;

    theField.draw = function() {
        mainContext.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        mainContext.fillStyle = "#8599d5";
        mainContext.strokeStyle = "#000000";
        mainContext.moveTo(0, 60);
        mainContext.lineTo(SCREEN_WIDTH, 60);
        mainContext.moveTo(0, SCREEN_HEIGHT - Y_MARGIN);
        mainContext.lineTo(SCREEN_WIDTH, SCREEN_HEIGHT - Y_MARGIN);
        mainContext.rect(X_MARGIN, SCREEN_HEIGHT - 90, X_MARGIN + 50, 30);
        mainContext.rect(X_MARGIN, Y_MARGIN + 60, X_MARGIN + 250, 30);
        mainContext.rect(X_MARGIN, Y_MARGIN + 90, 30, 240);
        mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 90);
        mainContext.lineTo(X_MARGIN + 360, Y_MARGIN + 120);
        mainContext.strokeStyle = "#FFFFFF";
        mainContext.fill();
        mainContext.stroke();
    }

    return theField;
}

function drawMistake() {
    mainContext.lineWidth = 2;
    switch (currentMistakeIndex) {
        case 0:
            // Head
            mainContext.moveTo(X_MARGIN + 370, Y_MARGIN + 130);
            mainContext.arc(X_MARGIN + 360, Y_MARGIN + 130, 10, 0, 2 * Math.PI);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
        case 1:
            // Body
            mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 140);
            mainContext.lineTo(X_MARGIN + 360, Y_MARGIN + 180);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
        case 2:
            // Left arm
            mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 150);
            mainContext.lineTo(X_MARGIN + 340, Y_MARGIN + 170);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
        case 3:
            // Right arm
            mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 150);
            mainContext.lineTo(X_MARGIN + 380, Y_MARGIN + 170);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
        case 4:
            // Left leg
            mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 180);
            mainContext.lineTo(X_MARGIN + 340, Y_MARGIN + 200);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
        case 5:
            // Right leg
            mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 180);
            mainContext.lineTo(X_MARGIN + 380, Y_MARGIN + 200);
            mainContext.strokeStyle = "#FFFFFF";
            mainContext.stroke();
            break;
    
        default:
            // The game is lost, this should not be reachable
            break;
    }
    currentMistakeIndex++;
}

function MaskedWord(word, x, y) {
    var thisMaskedWord = this;
    thisMaskedWord.x = x;
    thisMaskedWord.y = y;
    thisMaskedWord.word = word;

    thisMaskedWord.draw = function () {
        mainContext.font = "50px Courier";
        mainContext.lineWidth = "1";
        mainContext.strokeStyle = "#FFFFFF";
        mainContext.fillStyle = "#FFFFFF";
        mainContext.fillText(thisMaskedWord.word, thisMaskedWord.x, thisMaskedWord.y);
    }

    return thisMaskedWord;
}

function Player(scoreX, scoreY) {
    this.score = new Score(0, scoreX, scoreY, 0, 0);
}

function keyPressHandler(event) {
    console.log(event);

    if ("abcdefghijklmnopqrstuvwxyz0123456789".indexOf(event.key) > -1) {
        var updatedWord = "";
        var found = false;
        // fetch('http://localhost:5000/character?c=' + event.key)
        //     .then(response => response.json())
        //     .then(data => {
        //         console.log("request");
        //         maskedWord = new MaskedWord(data.word, 500, 50);
        //         drawAll();
        //     });
        // console.log(updatedWord);
        // maskedWord = new MaskedWord(updatedWord, 500, 50);
        // if (!found) {
        //     drawMistake(currentMistakeIndex);
        // }
    } else {
        // Handle invalid input
    }
    drawAll();
}

function clearScreen() {
    mainContext.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
}

function drawAll() {
    [field, player.score, maskedWord].forEach(function(gameObject, index) {
        gameObject.draw();
    });
}

document.addEventListener("DOMContentLoaded", function (event) {
    startGame();
});
