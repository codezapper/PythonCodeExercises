// Adapted from http://codepen.io/katzkode/pen/Kfgix

var duration;
var player = document.getElementById('audioplayer');
var pButton = document.getElementById('pButton');
var playhead = document.getElementById('playhead');
var timeline = document.getElementById('timeline');
var timelineWidth = timeline.offsetWidth - playhead.offsetWidth;

player.addEventListener("timeupdate", timeUpdate, false);

timeline.addEventListener("click", function (event) {
    moveplayhead(event);
    player.currentTime = duration * clickPercent(event);
}, false);

function clickPercent(e) {
    return (e.pageX - timeline.offsetLeft) / timelineWidth;
}

playhead.addEventListener('mousedown', mouseDown, false);
window.addEventListener('mouseup', mouseUp, false);

var onplayhead = false;
function mouseDown() {
    onplayhead = true;
    window.addEventListener('mousemove', moveplayhead, true);
    player.removeEventListener('timeupdate', timeUpdate, false);
}
function mouseUp(e) {
    if (onplayhead == true) {
        moveplayhead(e);
        window.removeEventListener('mousemove', moveplayhead, true);
        player.currentTime = duration * clickPercent(e);
        player.addEventListener('timeupdate', timeUpdate, false);
    }
    onplayhead = false;
}

function moveplayhead(e) {
    var newMargLeft = e.pageX - timeline.offsetLeft;
    if (newMargLeft >= 0 && newMargLeft <= timelineWidth) {
        playhead.style.marginLeft = newMargLeft + "px";
    }
    if (newMargLeft < 0) {
        playhead.style.marginLeft = "0px";
    }
    if (newMargLeft > timelineWidth) {
        playhead.style.marginLeft = timelineWidth + "px";
    }
}

function timeUpdate() {
    var playPercent = timelineWidth * (player.currentTime / duration);
    playhead.style.marginLeft = playPercent + "px";
    if (player.currentTime == duration) {
        pButton.className = "";
        pButton.className = "play";
    }
}

var currentTrack = 0;
var audio = $('#audioplayer');
var playlist = $('#playlist');
var trackList = [];

player.addEventListener('ended',function(e){
    if(currentTrack == (trackList.length - 1)){
        currentTrack = 0;
        player.src = playlist.find('a')[0];
    }else{
        currentTrack++;
        player.src = playlist.find('a')[currentTrack];    
    }
    player.play();
});

function getCurrentTrack() {
    if (trackList.length === 0) {
        player.load();
        trackList = playlist.find('li a');
        currentTrack = 0;
    }

    return trackList[currentTrack].getAttribute('href');
}

function play() {
    if (player.paused) {
        if (player.src === "") {
            player.src = getCurrentTrack();
        }
        player.play();
        pButton.className = "";
        pButton.className = "pause";
    } else {
        player.pause();
        pButton.className = "";
        pButton.className = "play";
    }
}

player.addEventListener("canplaythrough", function () {
    duration = player.duration;  
}, false);
