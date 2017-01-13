var playlist = $('#playlist');
var player = $('#audioplayer')[0];
var playButton = $('#play-pause-button');
var prevButton = $('#prev-button');
var nextButton = $('#next-button');
var timeLineHead = $('#timeline-head');
var currentTime = $('#song-time');
var timeline = document.getElementById('timeline');
var timelineWidth = $('#timeline-container')[0].offsetWidth - 20; //Need to compensate for head size
var finderBox = $('.flexsearch')[0];
var inputBox = $('.flexsearch--input')[0];
var trackList = [];
var searchResults = [];
var shuffledList = [];
var currentTrack = 0;
var currentTrackIndex = 0;
var useShuffled = false;
var useCycled = true;
var duration = -1;
var playListTemplate;
var prevSearchTerm;
var currentSearchTerm;
var hasSubmitted = false;

var trackListOperations = {
    REPLACE: 1,
    APPEND: 2,
    PREPEND: 3
}

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
    start: function(event, ui) {
        player.removeEventListener('timeupdate', timeUpdate);
    },
    stop: function(event, ui) {
        if (duration > 0) {
            player.currentTime = parseInt(player.duration * clickPercent(event));
        }
        player.addEventListener('timeupdate', timeUpdate, false);
    }
});

player.addEventListener('canplaythrough', function() {
    duration = player.duration;
});

playButton[0].addEventListener('click', function() {
    if (player.paused || !player.currentTime) {
        player.play();
        playButton[0].className = 'pause-button';
    } else {
        player.pause();
        playButton[0].className = 'play-button';
    }
});

prevButton[0].addEventListener('click', function() {
    playTrack(currentTrack - 1);
});

nextButton[0].addEventListener('click', function() {
    playTrack(currentTrack + 1);
});

player.addEventListener('ended', function(e) {
    playTrack(currentTrack + 1);
});

timeline.addEventListener('click', function(event) {
    if (duration > 0) {
        player.currentTime = parseInt(player.duration * clickPercent(event));
    }
}, false);

function clickPercent(e) {
    return (e.pageX - timeline.offsetLeft) / timelineWidth;
}

function showSongs(searchTerm) {
    songs = [];
    if (currentSearchTerm !== searchTerm) {
        currentSearchTerm = searchTerm;
        $.get('/lister/songs/', function(template) {
            playListTemplate = template;
            $.getJSON('/lister/search/' + searchTerm, function(songs) {
                var html = Mustache.render(template, songs);
                $('#container-frame').html(html);
                searchResults = songs.songs_list;
            });
        });
    }
}

function playTrack(track) {
    if (!hasSubmitted) {
        setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.PREPEND);
    }

    if (track < 0) {
        track = trackList.length - 1;
    } else if (track > trackList.length - 1) {
        track = 0;
    }
    $('[data-index=' + currentTrack + ']').closest('ul').removeClass('active-track');
    currentTrack = track; // Needed when clicking directly on the track

    duration = -1;
    player.src = trackList[track].path;
    player.load();
    player.play();
    playButton[0].className = 'pause-button';
    $('[data-index=' + currentTrack + ']').closest('ul').addClass('active-track');
}

finderBox.addEventListener('keyup', function(event) {
    if (event.key != "Enter") {
        hasSubmitted = false;
        showSongs(inputBox.value);
    } else {
        if (prevSearchTerm !== currentSearchTerm) {
            hasSubmitted = true;
            if (event.ctrlKey) {
                setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.REPLACE);
            } else if (event.shiftKey) {
                setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.PREPEND);
            } else {
                setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.APPEND);
            }
            //TODO: This can be optimized to only render the new data and append it
            var html = Mustache.render(playListTemplate, {"songs_list": trackList});
            $('#container-frame').html(html);
        }
        if (player.paused || !player.currentTime) {
            playTrack(currentTrack);
        }
    }
});

function setCurrentTrackList(searchTerm, searchResults, operation = trackListOperations.APPEND ) {
    prevSearchTerm = searchTerm;
    if (operation === trackListOperations.REPLACE) {
        trackList = searchResults;
    } else if (operation === trackListOperations.PREPEND) {
        trackList = searchResults.concat(trackList);
    } else {
        trackList = trackList.concat(searchResults);
    }
    //TODO: This can be optimized to only render the new data and append it
    var html = Mustache.render(playListTemplate, {"songs_list": trackList});
    $('#container-frame').html(html);
}

function timeUpdate() {
    var playPercent = timelineWidth * (player.currentTime / player.duration);
    currentTime[0].innerHTML = player.currentTime.toMMSS();
    timeLineHead.css('left', playPercent + 'px');
}

player.addEventListener('timeupdate', timeUpdate, false);

window.addEventListener('load', showSongs, false);
window.addEventListener('resize', function() {
    timelineWidth = $('#timeline')[0].offsetWidth;
});

window.addEventListener('submit', function(event) {
    event.preventDefault();
});
