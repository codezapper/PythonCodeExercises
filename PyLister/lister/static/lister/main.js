// Adapted from http://codepen.io/katzkode/pen/Kfgix

var playlist = $('#playlist');
var player = $('#audioplayer')[0];
var playButton = $('#play-pause-button');
var playHead = $('#play-head')[0];
var currentTime = $('li#song-time');
var currentTrackText = $('div#current-track-title');
var currentTrackCover = $('img#current-track-cover');
var shuffleButton = $('#shuffle-button');
var cycleButton = $('#cycle-button');
var onPlayHead = false;
var timeline = document.getElementById('timeline');
// var timelineWidth = timeline.offsetWidth - playHead.offsetWidth;
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

playButton[0].addEventListener('click', function() {
    playButton.toggleClass('play-button');
    playButton.toggleClass('pause-button');
});

// player.addEventListener('timeupdate', timeUpdate, false);

// player.addEventListener('ended', function(e) {
//     goToNextTrack();
// });

// player.addEventListener('canplaythrough', function() {
//     duration = player.duration;
// }, false);

function timeUpdate() {
    var playPercent = timelineWidth * (player.currentTime / duration);
    currentTime[0].innerHTML = player.currentTime.toMMSS();
    playHead.style.marginLeft = playPercent + 'px';
    if (player.currentTime == duration) {
        playButton.className = 'play';
    }
}

// timeline.addEventListener('click', function(event) {
//     movePlayHead(event);
//     player.currentTime = duration * clickPercent(event);
// }, false);

function clickPercent(e) {
    return (e.pageX - timeline.offsetLeft) / timelineWidth;
}

// playHead.addEventListener('mousedown', mouseDownOnPlayHead, false);

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
        playHead.style.marginLeft = newMarginLeft + 'px';
    }
    if (newMarginLeft < 0) {
        playHead.style.marginLeft = '0px';
    }
    if (newMarginLeft > timelineWidth) {
        playHead.style.marginLeft = timelineWidth + 'px';
    }
}

function getCurrentTrackPath() {
    return trackList[getCurrentTrack()].path;
}

function getCurrentTrack() {
    currentTrackText[0].innerHTML = trackList[currentTrack].title;
    return currentTrack;
}

function play() {
    if (currentTrackIndex <= 0) {
        setCurrentTrack(getNextTrack());
    } else {
        player.play();
    }

    playButton.className = 'pause';
}

function pause() {
    player.pause();
    playButton.className = 'play';
}

function playOrPause() {
    if (player.paused) {
        play();
    } else {
        pause();
    }
}

function getCoverPathFromSongPath(songPath) {
    return songPath.substring(0, songPath.lastIndexOf('/')) + '/Folder.jpg';
}

function getNextTrack() {
    if ((currentTrackIndex + 1) > Object.keys(trackList).length) {
        if (useCycled) {
            currentTrackIndex = 1;
        } else {
            return -1;
        }
    } else {
        currentTrackIndex++;
    }

    if (useShuffled && (currentTrackIndex > -1)) {
        return shuffledList[currentTrackIndex - 1];
    }

    return currentTrackIndex;
}

function getPrevTrack() {
    if ((currentTrackIndex - 1) < 1) {
        if (useCycled) {
            currentTrackIndex = Object.keys(trackList).length;
        } else {
            return -1;
        }
    } else {
        currentTrackIndex--;
    }

    if (useShuffled && (currentTrackIndex > -1)) {
        return shuffledList[currentTrackIndex - 1];
    }

    return currentTrackIndex;
}

function goToNextTrack() {
    setCurrentTrack(getNextTrack());
}

function goToPrevTrack() {
    setCurrentTrack(getPrevTrack());
}

function playTrack(track) {
    setCurrentTrack(track);
}

function setCurrentTrack(track) {
    initTrackListIfNeeded();
    if (track > -1) {
        $('[data-index="' + currentTrack + '"').closest('ul').removeClass('active-track');
        currentTrack = track;
        if (!useShuffled) {
            currentTrackIndex = track;
        }
        $('[data-index="' + currentTrack + '"').closest('ul').addClass('active-track');
        currentTrackPath = getCurrentTrackPath();
        currentTrackCover.attr('src', getCoverPathFromSongPath(currentTrackPath));
        player.src = currentTrackPath;
        playButton.className = 'pause';
        player.play();
    }
}

function getShuffledList() {
    if (shuffledList.length === 0) {
        shuffledList = Object.keys(trackList);
        for (var i = shuffledList.length; i > 0; i--) {
            var j = Math.floor(Math.random() * i);
            [shuffledList[i - 1], shuffledList[j]] = [shuffledList[j], shuffledList[i - 1]];
        }
    }
    return shuffledList;
}

function toggleShuffle() {
    useShuffled = !useShuffled;
    if (useShuffled) {
        getShuffledList();
    } else {
        currentTrackIndex = shuffledList[currentTrackIndex - 1];
    }
    shuffleButton.toggleClass('shuffle-button-off');
    shuffleButton.toggleClass('shuffle-button-on');
}

function toggleCycle() {
    useCycled = !useCycled;
    cycleButton.toggleClass('cycle-button-off');
    cycleButton.toggleClass('cycle-button-on');
}

function showAlbums() {
    setCurrentSection(1);
    $.get('/lister/albums/',
        function(template) {
            $.getJSON('/lister/albums_data/', function(albums) {
                var html = Mustache.render(template, albums);
                $('#content-frame').html(html);
                trackList = albums.albums_list;
            });
        }
    );
}

function showArtists() {
    setCurrentSection(2);
    $.get('/lister/artists/',
        function(template) {
            $.getJSON('/lister/artists_data/', function(artists) {
                var html = Mustache.render(template, artists);
                $('#content-frame').html(html);
                trackList = artists.artists_list;
            });
        }
    );
}

function showYears() {
    setCurrentSection(3);
    $.get('/lister/years/',
        function(template) {
            $.getJSON('/lister/years_data/', function(years) {
                var html = Mustache.render(template, years);
                $('#content-frame').html(html);
                trackList = years.years_list;
            });
        }
    );
}

function showSingleAlbum(albumId) {
    setCurrentSection(1);
    songs = [];
    $.get('/lister/songs/',
        function(template) {
            $.getJSON('/lister/albums_data/' + albumId.toString(), function(albums) {
                var html = Mustache.render(template, albums);
                $('#content-frame').html(html);
                trackList = albums.songs_list;
            });
        }
    );
}

function showSingleArtist(artistId) {
    setCurrentSection(2);
    songs = [];
    $.get('/lister/songs/',
        function(template) {
            $.getJSON('/lister/artists_data/' + artistId.toString(), function(artists) {
                var html = Mustache.render(template, artists);
                $('#content-frame').html(html);
                trackList = artists.songs_list;
            });
        }
    );
}

function showSingleYear(year) {
    setCurrentSection(3);
    songs = [];
    $.get('/lister/songs/',
        function(template) {
            $.getJSON('/lister/years_data/' + year.toString(), function(years) {
                var html = Mustache.render(template, years);
                $('#content-frame').html(html);
                trackList = years.songs_list;
            });
        }
    );
}

function showSongs(searchTerm) {
    setCurrentSection(0);
    songs = [];
    $.get('/lister/songs/', function(template) {
        $.getJSON('/lister/search/' + searchTerm, function(songs) {
            var html = Mustache.render(template, songs);
            $('#container-frame').html(html);
            trackList = songs.songs_list;
        });
    });
}

finderBox.addEventListener('keyup', function(event) {
    showSongs(inputBox.value);
});

function initTrackListIfNeeded() {

}

function volumeUp() {
    if (player.volume < 1) {
        player.volume += 0.1;
    }
}

function volumeDown() {
    if (player.volume > 0) {
        player.volume -= 0.1;
    }
}

function setCurrentSection(index) {
    for (i = 0; i < $('.menu-container > li').length; i++ ) {
        if (i == index) {
            $('.menu-container > li')[i].className = 'active-menu';
            $('.menu-container > li > a')[i].className = 'active-menu';
        } else {
            $('.menu-container > li')[i].className = 'row-1';
            $('.menu-container > li > a')[i].className = 'row-1';
        }
    }
}

window.addEventListener('load', showSongs, false);
window.addEventListener('mouseup', mouseUp, false);
window.addEventListener('submit', function(event) {
    event.preventDefault();
});
