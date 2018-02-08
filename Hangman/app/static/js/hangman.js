var mainCanvas = document.getElementById("gameCanvas");
var mainContext = mainCanvas.getContext("2d");
var gameIsRunning = true;
var animationId;
var currentMistakeIndex = 0;
var isGameOver = false;

var SCREEN_WIDTH = 800;
var SCREEN_HEIGHT = 480;
var X_MARGIN = 150;
var Y_MARGIN = 60;

var field = new Field();
var score;
var maskedWord;

function startGame() {
    mainContext.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
    fetch('http://localhost:5000/new_word', { credentials: 'include'  })
        .then(response => response.json())
        .then(data => {
            maskedWord = new MaskedWord(Array(data.word_size + 1).join("_"), 500, 50);
            score = new Score(data.score, 80, 50, 0, 0);
            document.addEventListener("keypress", keyPressHandler, false);
            [field, score, maskedWord].forEach(function (gameObject, index) {
                gameObject.draw();
            });
        });
}

function Score(value, x, y) {
    var thisScore = this;
    thisScore.value = value;
    thisScore.x = x;
    thisScore.y = y;

    thisScore.decrease = function() {
        thisScore.value--;
    }

    thisScore.draw = function() {
        mainContext.beginPath();
        mainContext.rect(5, 5, 200, 50);
        mainContext.fillStyle = "#456";
        mainContext.fill();
        mainContext.closePath();
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
        mainContext.beginPath();
        mainContext.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        mainContext.fillStyle = "#456";
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
        mainContext.closePath();
    }

    return theField;
}

function drawHead() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 370, Y_MARGIN + 130);
    mainContext.arc(X_MARGIN + 360, Y_MARGIN + 130, 10, 0, 2 * Math.PI);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

function drawBody() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 140);
    mainContext.lineTo(X_MARGIN + 360, Y_MARGIN + 180);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

function drawLeftArm() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 150);
    mainContext.lineTo(X_MARGIN + 340, Y_MARGIN + 170);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

function drawRightArm() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 150);
    mainContext.lineTo(X_MARGIN + 380, Y_MARGIN + 170);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

function drawLeftLeg() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 180);
    mainContext.lineTo(X_MARGIN + 340, Y_MARGIN + 200);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

function drawRightLeg() {
    mainContext.lineWidth = 2;
    mainContext.moveTo(X_MARGIN + 360, Y_MARGIN + 180);
    mainContext.lineTo(X_MARGIN + 380, Y_MARGIN + 200);
    mainContext.strokeStyle = "#FFFFFF";
    mainContext.stroke();
}

var drawMistake = [
    drawHead,
    drawBody,
    drawLeftArm,
    drawRightArm,
    drawLeftLeg,
    drawRightLeg
]

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

function keyPressHandler(event) {
    if (isGameOver) {
        if (event.key == 'n') {
            isGameOver = false;
            startGame();
        }
    } else {
        if ("abcdefghijklmnopqrstuvwxyz0123456789".indexOf(event.key) > -1) {
            var updatedWord = "";
            var found = false;
            fetch('http://localhost:5000/character?c=' + event.key, { credentials: 'include'  })
                .then(response => response.json())
                .then(data => {
                    if (data.error === 0 ) {
                        maskedWord = new MaskedWord(data.word, 500, 50);
                        maskedWord.draw();
                        if (data.winner) {
                            gameOver(true);
                        } else {
                            found = data.found;
                            score.value = data.score;
                            score.draw();
                            if (!found) {
                                mainContext.beginPath();
                                drawMistake[currentMistakeIndex]();
                                mainContext.closePath();

                                currentMistakeIndex++;
                                if (currentMistakeIndex >= drawMistake.length) {
                                    gameOver(false);
                                }
                            }
                        }
                    }
                });
        } else {
            // Handle invalid input
        }
    }
}

function win() {
}

function gameOver(isWinner) {
    mainContext.font = "50px Courier";
    mainContext.lineWidth = "1";
    mainContext.fillStyle = "#FFFFFF";
    if (isWinner) {
        mainContext.fillText("YOU WIN!", 300, 100);
    } else {
        mainContext.fillText("YOU LOSE!", 300, 100);
    }
    mainContext.fillText("GAME OVER", 300, 300);
    isGameOver = true;
    currentMistakeIndex = 0;
}

document.addEventListener("DOMContentLoaded", function (event) {
    startGame();
});
