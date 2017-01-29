var player = $('#audioplayer');
var playerElement = $('#audioplayer')[0];
var playButton = $('#play-pause-button');
var currentTime = $('#song-time');
var timeline = $('#timeline');
var timeLineHead = $('#timeline-head');
var timelineWidth = $('#timeline-container').outerWidth() - 20; //Need to compensate for head size
var currentTrackCover = $('#current-track-cover');
var currentTitle = $('#current-title');
var currentArtist = $('#current-artist');
var finderBox = $('.mainsearch');
var inputBox = $('.mainsearch-input');
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
var displayedSongIDs = {};

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

function clickPercent(e) {
    return (e.pageX - timeline.offset().left) / timelineWidth;
}

function showSongs(searchTerm) {
    songs = [];
    if (currentSearchTerm !== searchTerm) {
        currentSearchTerm = searchTerm;
        $.get('/lister/songs/', function(template) {
            playListTemplate = template;
            if (searchTerm === '') {
                var html = Mustache.render(playListTemplate, {"search_results": [], "playlist": trackList});
                $('#container-frame').html(html);
                $('#search-results').css({display: 'block'});
                $('#playlist').css({display: 'none'});
                return;
            }
            $.getJSON('/lister/search/' + searchTerm, function(songs) {
                searchResults = songs.songs_list;
                var html = Mustache.render(playListTemplate, {"search_results": searchResults, "playlist": trackList});
                $('#container-frame').html(html);
                $('#search-results').css({display: 'block'});
                $('#playlist').css({display: 'none'});
            });
        });
    }
}

function playTrack(track) {
    if (track < 0) {
        track = trackList.length - 1;
    } else if (track > trackList.length - 1) {
        track = 0;
    }
    $('[data-index-playlist=' + trackList[currentTrack].song_id + ']').closest('ul').removeClass('active-track');
    currentTrack = track; // Needed when clicking directly on the track

    duration = -1;
    currentTrackCover.attr('src', getCoverPathFromSongPath(trackList[track].path));
    currentTitle.html(trackList[track].title);
    currentArtist.html(trackList[track].artist);
    playerElement.src = trackList[track].path;
    playerElement.load();
    playerElement.play();
    playButton.removeClass('play-button');
    playButton.addClass('pause-button');
    $('[data-index-playlist=' + trackList[currentTrack].song_id + ']').closest('ul').addClass('active-track');
}

function getCoverPathFromSongPath(songPath) {
    return songPath.substring(0, songPath.lastIndexOf('/')) + '/Cover.png';
}

function setCurrentTrackList(searchTerm, searchResults, operation = trackListOperations.APPEND ) {
    prevSearchTerm = searchTerm;
    if (operation === trackListOperations.REPLACE) {
        trackList = searchResults;
        playTrack(0);
    } else if (operation === trackListOperations.PREPEND) {
        filteredSearchResults = searchResults.filter(function(song) {
            if (displayedSongIDs[song.song_id] == null) {
                displayedSongIDs[song.song_id] = 1;
                return true;
            }
            return false;
        });
        trackList = filteredSearchResults.concat(trackList);
    } else {
        filteredSearchResults = searchResults.filter(function(song) {
            if (displayedSongIDs[song.song_id] == null) {
                displayedSongIDs[song.song_id] = 1;
                return true;
            }
            return false;
        });
        trackList = trackList.concat(filteredSearchResults);
    }
    //TODO: This can be optimized to only render the new data and append it
    var html = Mustache.render(playListTemplate, {"playlist": trackList});
    $('#container-frame').html(html);
    $('#search-results').css({display: 'none'});
    $('#playlist').css({display: 'block'});
}

function timeUpdate() {
    var playPercent = timelineWidth * (playerElement.currentTime / playerElement.duration);
    currentTime[0].innerHTML = playerElement.currentTime.toMMSS();
    timeLineHead.css('left', playPercent + 'px');
}

window.addEventListener('load', function() {showSongs('')}, false);
window.addEventListener('resize', function() {
    timelineWidth = $('#timeline-container').outerWidth() - 20; //Need to compensate for head size
});

window.addEventListener('submit', function(event) {
    event.preventDefault();
});

function bindUI() {
    playerElement.load();
    finderBox.bind('keyup', function(event) {
        if (event.key == "ArrowDown") {
            playTrack(currentTrack + 1);
            return;
        }
        if (event.key == "ArrowUp") {
            playTrack(currentTrack - 1);
            return;
        }
        if (event.key != "Enter") {
            if (inputBox.val() !== '') {
                showSongs(inputBox.val());
            } else {
                $('#search-results').css({display: 'none'});
                $('#playlist').css({display: 'block'});
                if (!playerElement.paused || playerElement.currentTime) {
                    $('[data-index-playlist=' + trackList[currentTrack].song_id + ']').closest('ul').addClass('active-track');
                }
            }
        } else {
            if (searchResults.length > 0) {
                if (prevSearchTerm !== currentSearchTerm) {
                    if (event.ctrlKey) {
                        setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.REPLACE);
                    } else if (event.shiftKey) {
                        setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.PREPEND);
                    } else {
                        setCurrentTrackList(currentSearchTerm, searchResults, trackListOperations.APPEND);
                    }
                }
                if (playerElement.paused || !playerElement.currentTime) {
                    playTrack(currentTrack);
                }
                inputBox.val('');
            }
        }
    });

    player.bind('canplaythrough', function() {
        duration = playerElement.duration;
    });

    player.bind('timeupdate', timeUpdate);

    player.bind('ended', function(e) {
        playTrack(currentTrack + 1);
    });

    playButton.bind('click', function() {
        if (trackList.length === 0) {
            return;
        }

        if (playerElement.paused || !playerElement.currentTime) {
            playerElement.play();
        } else {
            playerElement.pause();
        }
        playButton.toggleClass('pause-button');
        playButton.toggleClass('play-button');
    });

    $('#prev-button').bind('click', function() {
        playTrack(currentTrack - 1);
    });

    $('#next-button').bind('click', function() {
        playTrack(currentTrack + 1);
    });

    timeline.bind('click', function(event) {
        if (duration > 0) {
            playerElement.currentTime = parseInt(playerElement.duration * clickPercent(event));
        }
    });

    $('#timeline-head').draggable({
        appendTo: $('#timeline'),
        axis: "x",
        containment: $('#timeline'),
        start: function(event, ui) {
            player.unbind('timeupdate', timeUpdate);
        },
        drag: function(event, ui) {
            if (playerElement.duration > 0) {
                currentTime.html(parseInt(playerElement.duration * clickPercent(event)).toMMSS());
            }
        },
        stop: function(event, ui) {
            if (duration > 0) {
                playerElement.currentTime = parseInt(playerElement.duration * clickPercent(event));
            }
            player.bind('timeupdate', timeUpdate);
        }
    });
}

$(document).ready(bindUI);
