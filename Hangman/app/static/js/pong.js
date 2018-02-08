var mainCanvas = document.getElementById("gameCanvas");
var mainContext = mainCanvas.getContext("2d");
var gameIsRunning = true;
var animationId;

var SCREEN_WIDTH = 800;
var SCREEN_HEIGHT = 480;
var X_MARGIN = 15;
var Y_MARGIN = 60;
var PADDLE_X_SIZE = 15;
var PADDLE_Y_SIZE = 60;

var PADDLE_Y_SPEED = 5;

function Score(value, initialX, initialY) {
    var thisScore = this;
    thisScore.value = value;
    thisScore.x = initialX;
    thisScore.y = initialY;

    thisScore.increase = function() {
        thisScore.value++;
    }

    thisScore.update = function() {
        return 0;
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

    theField.update = function() {
        return 0;
    }

    theField.draw = function() {
        mainContext.beginPath();
        mainContext.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
        mainContext.fillStyle = "#456";
        mainContext.strokeStyle = "#FFFFFF";
        mainContext.fill();
        mainContext.stroke();
        mainContext.closePath();
        mainContext.beginPath();
        mainContext.strokeStyle = "#FFFFFF";
        mainContext.moveTo(0, 60);
        mainContext.lineTo(SCREEN_WIDTH, 60);
        mainContext.stroke();
        mainContext.closePath();
        mainContext.beginPath();
        mainContext.strokeStyle = "#FFFFFF";
        mainContext.moveTo(SCREEN_WIDTH / 2, 0);
        mainContext.lineTo(SCREEN_WIDTH / 2, SCREEN_HEIGHT);
        mainContext.stroke();
        mainContext.closePath();
        mainContext.beginPath();
        mainContext.arc(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + 20, 80, 0, 2 * Math.PI);
        mainContext.stroke();
        mainContext.closePath();
    }

    return theField;
}

function Ball(radius, initialX, initialY, initialDx, initialDy) {
    var theBall = this;
    theBall.radius = radius;
    theBall.initialX = initialX;
    theBall.initialY = initialY;
    theBall.x = initialX;
    theBall.y = initialY;
    theBall.dx = initialDx;
    theBall.dy = initialDy;
    theBall.currentSpeed = 1;
    theBall.maxSpeed = 10;

    theBall.draw = function() {
        mainContext.beginPath();
        // mainContext.fillStyle = "#456";
        mainContext.fillStyle = "#FFFFFF";
        mainContext.arc(theBall.x, theBall.y, theBall.radius, 0, Math.PI * 2);
        mainContext.strokeStyle = "#000000";
        mainContext.fill();
        mainContext.stroke();
        mainContext.closePath();
    }

    theBall.respawn = function() {
        theBall.x = theBall.initialX
        theBall.y = theBall.initialY
        theBall.dx = (theBall.dx > 0) ? -2 : 2;
        theBall.dy = (theBall.dy > 0) ? -2 : 2;
        theBall.currentSpeed = 1;
    }

    theBall.bounceFaster = function() {
        if (theBall.currentSpeed < theBall.maxSpeed) {
            theBall.dx = (1.1 * theBall.dx)
            theBall.dy = (1.1 * theBall.dy)
            theBall.currentSpeed++;
        }
        theBall.dx = -theBall.dx;
    }

    theBall.update = function() {
        theBall.x += theBall.dx;
        theBall.y += theBall.dy;

        if (theBall.y >= (SCREEN_HEIGHT - theBall.radius)) {
            theBall.y = (SCREEN_HEIGHT - theBall.radius);
            theBall.dy = -theBall.dy;
        }
        if (theBall.y < Y_MARGIN + theBall.radius) {
            theBall.y = Y_MARGIN + theBall.radius;
            theBall.dy = -theBall.dy;
        }

        if (theBall.x >= (players[1].paddle.x - theBall.radius)) {
            if ((theBall.y >= players[1].paddle.y) && (theBall.y <= (players[1].paddle.y + players[1].paddle.height))) {
                theBall.bounceFaster();
            } else {
                players[0].score.increase();
                theBall.respawn();
            }
        }

        if (theBall.x <= (players[0].paddle.x + theBall.radius + players[0].paddle.width)) {
            if ((theBall.y >= players[0].paddle.y) && (theBall.y <= (players[0].paddle.y + players[0].paddle.height))) {
                theBall.bounceFaster();
            } else {
                players[1].score.increase();
                theBall.respawn();
            }
        }
    }

    return theBall;
}

function Paddle(width, height, initialX, initialY, initialDx, initialDy) {
    var thisPaddle = this;
    thisPaddle.width = width;
    thisPaddle.height = height;
    thisPaddle.x = initialX;
    thisPaddle.y = initialY;
    thisPaddle.dx = initialDx;
    thisPaddle.dy = initialDy;
    thisPaddle.isMovingUp = false;
    thisPaddle.isMovingDown = false;

    thisPaddle.draw = function() {
        mainContext.beginPath();
        mainContext.rect(thisPaddle.x, thisPaddle.y, thisPaddle.width, thisPaddle.height);
        // mainContext.fillStyle = "#456";
        mainContext.fillStyle = "#FFFFFF";
        mainContext.strokeStyle = "#000000";
        mainContext.fill();
        mainContext.stroke();
        mainContext.closePath();
    }

    thisPaddle.moveUp = function() {
        thisPaddle.dy = -PADDLE_Y_SPEED;
    }

    thisPaddle.moveDown = function() {
        thisPaddle.dy = PADDLE_Y_SPEED;
    }

    thisPaddle.stopMoving = function() {
        thisPaddle.dy = 0;
    }

    thisPaddle.update = function() {
        thisPaddle.x += thisPaddle.dx;
        thisPaddle.y += thisPaddle.dy;

        if (thisPaddle.y >= (SCREEN_HEIGHT - thisPaddle.height)) {
            thisPaddle.y = (SCREEN_HEIGHT - thisPaddle.height);
        }
        if (thisPaddle.y < Y_MARGIN) {
            thisPaddle.y = Y_MARGIN;
        }
    }
    return thisPaddle;
}

function Player(paddleWidth, paddleHeight, paddleX, paddleY, scoreX, scoreY) {
    var thisPlayer = this;
    thisPlayer.paddle = new Paddle(paddleWidth, paddleHeight, paddleX, paddleY, 0, 0);
    thisPlayer.score = new Score(0, scoreX, scoreY, 0, 0);
}

function keyDownHandler(event) {
    if (event.key in keyDownMapping) {
        keyDownMapping[event.key]();
    }
}

function keyUpHandler(event) {
    if (event.key in keyUpMapping) {
        keyUpMapping[event.key]();
    }
}

function clearScreen() {
    mainContext.clearRect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT);
}

function pauseOrResumeGame() {
    if (gameIsRunning) {
        cancelAnimationFrame(animationId);
    } else {
        animationId = requestAnimationFrame(drawAll);
    }
    gameIsRunning = !gameIsRunning;
}

function drawAll() {
    gameObjects.forEach(function(gameObject, index) {
        gameObject.update();
    });
    clearScreen();
    gameObjects.forEach(function(gameObject, index) {
        gameObject.draw();
    });
    animationId = requestAnimationFrame(drawAll);
}

var ball = new Ball(10, 398, 260, 2, 2);

var players = [new Player(PADDLE_X_SIZE, PADDLE_Y_SIZE, X_MARGIN, (SCREEN_HEIGHT / 2) - (PADDLE_Y_SIZE / 2), 80, 50),
    new Player(PADDLE_X_SIZE, PADDLE_Y_SIZE, SCREEN_WIDTH - X_MARGIN - PADDLE_X_SIZE, (SCREEN_HEIGHT / 2) - (PADDLE_Y_SIZE / 2), 700, 50)
];
var gameObjects = [new Field(), ball, players[0].paddle, players[1].paddle, players[0].score, players[1].score];

var keyDownMapping = {
    p: pauseOrResumeGame,
    w: players[0].paddle.moveUp,
    s: players[0].paddle.moveDown,
    ArrowUp: players[1].paddle.moveUp,
    ArrowDown: players[1].paddle.moveDown
};
var keyUpMapping = {
    w: players[0].paddle.stopMoving,
    s: players[0].paddle.stopMoving,
    ArrowUp: players[1].paddle.stopMoving,
    ArrowDown: players[1].paddle.stopMoving
};

document.addEventListener("keydown", keyDownHandler, false);
document.addEventListener("keyup", keyUpHandler, false);

var cancelAnimationFrame = window.cancelAnimationFrame || window.mozCancelAnimationFrame || window.webkitCancelAnimationFrame || window.msCancelAnimationFrame;
var requestAnimationFrame = window.requestAnimationFrame || window.mozRequestAnimationFrame || window.webkitRequestAnimationFrame || window.msRequestAnimationFrame;
animationId = requestAnimationFrame(drawAll);