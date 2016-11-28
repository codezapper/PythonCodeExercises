// Adapted from http://codepen.io/katzkode/pen/Kfgix

var playlist = $('#playlist');
var player = $('#audioplayer')[0];
var playButton = $('#play-button')[0];
var playHead = $('#play-head')[0];
var currentTrackText = $('div#current-track-title');
var currentTrackCover = $('img#current-track-cover');
var onPlayHead = false;
var timeline = document.getElementById('timeline');
var timelineWidth = timeline.offsetWidth - playHead.offsetWidth;
var trackList = [];
var currentTrack = 0;
var duration;

player.addEventListener("timeupdate", timeUpdate, false);

player.addEventListener('ended',function(e){
    nextTrack();
});

player.addEventListener("canplaythrough", function () {
    duration = player.duration;  
}, false);

function timeUpdate() {
    var playPercent = timelineWidth * (player.currentTime / duration);
    playHead.style.marginLeft = playPercent + "px";
    if (player.currentTime == duration) {
        playButton.className = "";
        playButton.className = "play";
    }
}

timeline.addEventListener("click", function (event) {
    movePlayHead(event);
    player.currentTime = duration * clickPercent(event);
}, false);

function clickPercent(e) {
    return (e.pageX - timeline.offsetLeft) / timelineWidth;
}

playHead.addEventListener('mousedown', mouseDownOnPlayHead, false);

function mouseDownOnPlayHead() {
    onPlayHead = true;
    window.addEventListener('mousemove', movePlayHead, true);
    player.removeEventListener('timeupdate', timeUpdate, false);
}

function mouseUp(e) {
    if (onPlayHead == true) {
        movePlayHead(e);
        window.removeEventListener('mousemove', movePlayHead, true);
        player.currentTime = duration * clickPercent(e);
        player.addEventListener('timeupdate', timeUpdate, false);
    }
    onPlayHead = false;
}

function movePlayHead(e) {
    var newMarginLeft = e.pageX - timeline.offsetLeft;
    if (newMarginLeft >= 0 && newMarginLeft <= timelineWidth) {
        playHead.style.marginLeft = newMarginLeft + "px";
    }
    if (newMarginLeft < 0) {
        playHead.style.marginLeft = "0px";
    }
    if (newMarginLeft > timelineWidth) {
        playHead.style.marginLeft = timelineWidth + "px";
    }
}

function getCurrentTrack() {
    if (trackList.length === 0) {
        player.load();
        trackList = playlist.find('li a');
        currentTrack = 0;
    }

    $(trackList[currentTrack].closest('ul')).addClass('active-track');
    currentTrackText[0].innerHTML = trackList[currentTrack].text;
    return trackList[currentTrack].getAttribute('href');
}

function play() {
    if (player.paused) {
        if (player.src === "") {
            currentTrack = getCurrentTrack();
            setCoverImage(currentTrack);
            player.src = currentTrack;
        }
        player.play();
        playButton.className = "pause";
    } else {
        player.pause();
        playButton.className = "play";
    }
}

function setCoverImage(songPath) {
    console.log(currentTrackCover);
    currentTrackCover.attr('src', getCoverPathFromSongPath(songPath));
}

function getCoverPathFromSongPath(songPath) {
    return songPath.substring(0, songPath.lastIndexOf('/')) + '/Folder.jpg';
}

function getNextTrack() {
    var trackPath = '';
    $(trackList[currentTrack].closest('ul')).removeClass('active-track');
    if(currentTrack == (trackList.length - 1)){
        currentTrack = 0;
        trackPath = playlist.find('a')[0];
    } else {
        currentTrack++;
        trackPath = playlist.find('a')[currentTrack];    
    }
    $(trackList[currentTrack].closest('ul')).addClass('active-track');
    currentTrackText[0].innerHTML = trackList[currentTrack].text;
    setCoverImage(trackPath);
    return trackPath;
}

function getPrevTrack() {
    var trackPath = '';
    $(trackList[currentTrack].closest('ul')).removeClass('active-track');
    if(currentTrack == 0){
        currentTrack = trackList.length - 1;
        trackPath = playlist.find('a')[currentTrack];
    } else {
        currentTrack--;
        trackPath = playlist.find('a')[currentTrack];    
    }
    $(trackList[currentTrack].closest('ul')).addClass('active-track');
    currentTrackText[0].innerHTML = trackList[currentTrack].text;
    setCoverImage(trackPath);
    return trackPath;
}

function nextTrack() {
    player.src = getNextTrack();
    player.play();
}

function prevTrack() {
    player.src = getPrevTrack();
    player.play();
}

window.addEventListener('mouseup', mouseUp, false);
