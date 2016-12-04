// Adapted from http://codepen.io/katzkode/pen/Kfgix

var playlist = $('#playlist');
var player = $('#audioplayer')[0];
var playButton = $('#play-button')[0];
var playHead = $('#play-head')[0];
var currentTime = $('li#song-time');
var currentTrackText = $('div#current-track-title');
var currentTrackCover = $('img#current-track-cover');
var onPlayHead = false;
var timeline = document.getElementById('timeline');
var timelineWidth = timeline.offsetWidth - playHead.offsetWidth;
var trackList = {};
var currentTrack = 0;
var duration;

Number.prototype.toMMSS = function () {
    var roundedTime = Math.round(this);
    var minutes = Math.floor(roundedTime / 60);
    var seconds = roundedTime - (minutes * 60);

    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;

    return minutes + ':' + seconds;
}

player.addEventListener("timeupdate", timeUpdate, false);

player.addEventListener('ended',function(e){
    nextTrack();
});

player.addEventListener("canplaythrough", function () {
    duration = player.duration;  
}, false);

function timeUpdate() {
    var playPercent = timelineWidth * (player.currentTime / duration);
    currentTime[0].innerHTML = player.currentTime.toMMSS();
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
        player.addEventListener("timeupdate", timeUpdate, false);
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

function getCurrentTrackPath() {
    if (Object.keys(trackList).length === 0) {
        player.load();
        playlist.find('li a').each(function(index, item) {
            trackList[item.getAttribute('data-index')] = {}
            trackList[item.getAttribute('data-index')]["path"] = item.getAttribute('data-path');
            trackList[item.getAttribute('data-index')]["title"] = item.text;
        });
        currentTrack = 1;
    }

    return trackList[getCurrentTrack()].path;
}

function getCurrentTrack() {
    if (Object.keys(trackList).length === 0) {
        player.load();
        playlist.find('li a').each(function(index, item) {
            trackList[item.getAttribute('data-index')] = {}
            trackList[item.getAttribute('data-index')]["path"] = item.getAttribute('data-path');
            trackList[item.getAttribute('data-index')]["title"] = item.text;
        });
        currentTrack = 1;
    }

    currentTrackText[0].innerHTML = trackList[currentTrack].title;
    $('[data-index="' + currentTrack + '"').closest('ul').addClass('active-track');
    return currentTrack;
}

function play() {
    setCoverImage(getCurrentTrackPath());
    if (player.src === "") {
        player.src = getCurrentTrackPath();
    }
    player.play();
    playButton.className = "pause";
}

function pause() {
    player.pause();
    playButton.className = "play";
}

function playOrPause() {
    if (player.paused) {
        play();
    } else {
        pause();
    }
}

function setCoverImage(songPath) {
    currentTrackCover.attr('src', getCoverPathFromSongPath(songPath));
}

function getCoverPathFromSongPath(songPath) {
    return songPath.substring(0, songPath.lastIndexOf('/')) + '/Folder.jpg';
}

function getNextTrack() {
    $('[data-index="' + currentTrack + '"').closest('ul').removeClass('active-track');
    currentTrack++;
    if (currentTrack > Object.keys(trackList).length) {
        currentTrack = 1;
    }
    $('[data-index="' + currentTrack + '"').closest('ul').addClass('active-track');

    setCoverImage(getCurrentTrackPath());
    return trackList[currentTrack].path;
}

function getPrevTrack() {
    $('[data-index="' + currentTrack + '"').closest('ul').removeClass('active-track');
    currentTrack--;
    if (currentTrack <= 0) {
        currentTrack = Object.keys(trackList).length;
    }
    $('[data-index="' + currentTrack + '"').closest('ul').addClass('active-track');

    setCoverImage(getCurrentTrackPath());
    return trackList[currentTrack].path;
}

function nextTrack() {
    player.src = getNextTrack();
    play();
}

function prevTrack() {
    player.src = getPrevTrack();
    play();
}

function playTrack(trackIndex) {
    if (Object.keys(trackList).length === 0) {
        player.load();
        playlist.find('li a').each(function(index, item) {
            trackList[item.getAttribute('data-index')] = {}
            trackList[item.getAttribute('data-index')]["path"] = item.getAttribute('data-path');
            trackList[item.getAttribute('data-index')]["title"] = item.text;
        });
        currentTrack = 1;
    }

    $('[data-index="' + currentTrack + '"').closest('ul').removeClass('active-track');
    currentTrack = trackIndex;
    $('[data-index="' + currentTrack + '"').closest('ul').addClass('active-track');
    player.src = getCurrentTrackPath();
    play();
}

window.addEventListener('mouseup', mouseUp, false);
