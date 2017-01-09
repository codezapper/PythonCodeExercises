var playlist = $('#playlist');
var player = $('#audioplayer')[0];
var playButton = $('#play-pause-button');
var timeLineHead = $('#timeline-head');
var currentTime = $('li#song-time');
var timeline = document.getElementById('timeline');
var timelineWidth = $('#timeline')[0].offsetWidth;
var finderBox = $('.flexsearch')[0];
var inputBox = $('.flexsearch--input')[0];
var trackList = {};
var shuffledList = [];
var currentTrack = 0;
var currentTrackIndex = 0;
var useShuffled = false;
var useCycled = true;
var duration;

Number.prototype.toMMSS = function() {
    var roundedTime = Math.round(this);
    var minutes = Math.floor(roundedTime / 60);
    var seconds = roundedTime - (minutes * 60);

    minutes = minutes < 10 ? '0' + minutes : minutes;
    seconds = seconds < 10 ? '0' + seconds : seconds;

    return minutes + ':' + seconds;
}

$('#timeline-head').draggable({
    appendTo: $('#timeline'),
    axis: "x",
    containment: $('#timeline'),
    stop: function( event, ui ) {
        console.log((ui.position.left * 100) / timelineWidth);
    }
});

playButton[0].addEventListener('click', function() {
    playButton.toggleClass('play-button');
    playButton.toggleClass('pause-button');
});


// player.addEventListener('ended', function(e) {
//     goToNextTrack();
// });

// player.addEventListener('canplaythrough', function() {
//     duration = player.duration;
// }, false);

// timeline.addEventListener('click', function(event) {
//     moveTimeLineHead(event);
//     player.currentTime = duration * clickPercent(event);
// }, false);

function clickPercent(e) {
    return (e.pageX - timeline.offsetLeft) / timelineWidth;
}

function showSongs(searchTerm) {
    songs = [];
    $.get('/lister/songs/', function(template) {
        $.getJSON('/lister/search/' + searchTerm, function(songs) {
            var html = Mustache.render(template, songs);
            $('#container-frame').html(html);
            trackList = songs.songs_list;
        });
    });
}

function playSongs() {
    player.src = trackList[0].path;
    player.play();
    playButton.className = 'pause-button';
}

finderBox.addEventListener('keyup', function(event) {
    showSongs(inputBox.value);
});


player.addEventListener('timeupdate', function() {
    var playPercent = timelineWidth * (player.currentTime / player.duration);
    console.log(playPercent);
    // currentTime[0].innerHTML = player.currentTime.toMMSS();
    timeLineHead.css('left', playPercent + 'px');

    // if (player.currentTime == duration) {
    //     playButton.className = 'play';
    // }
}, false);

window.addEventListener('load', showSongs, false);
window.addEventListener('resize', function() {
    timelineWidth = $('#timeline')[0].offsetWidth;
});

window.addEventListener('submit', function(event) {
    event.preventDefault();
    playSongs();
});
