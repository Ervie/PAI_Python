
// Odświezanie polecanek meta co minutę
$(document).ready(function () {
    // pierwszy raz od razu przy wczytaniu
    refreshSuggestions()

    setInterval(refreshSuggestions, 60000)
});

function refreshSuggestions() {
    $.ajax({
        url: 'sidebar',
        success: function (data) {
            $('#sidebar').html(data);
        }
    })
};

// Pierwsza sugestia
$(document).ready(function () {
    $('body').on('click', '#firstSuggestion', function () {
        var stream = {
            title: $('body').data('firstChannelName'),
            mp3: $('body').data('firstChannelUrl')
        }

        imgSrc = $('body').data('firstImagePath')

        $('#jquery_jplayer_1').jPlayer('setMedia', stream);
        $("#currentChannelLogo").attr('src', imgSrc);

        logListeningTime();
        currentChannelUrl = $('body').data('firstChannelUrl');
        currentChannelName = $('body').data('firstChannelName');

        loadRating();
    });
});

// Druga sugestia
$(document).ready(function () {
    $("body").on('click', '#secondSuggestion', function () {
        var stream = {
            title: $('body').data('secondChannelName'),
            mp3: $('body').data('secondChannelUrl')
        }

        imgSrc = $('body').data('secondImagePath')

        $('#jquery_jplayer_1').jPlayer('setMedia', stream);
        $("#currentChannelLogo").attr('src', imgSrc);

        logListeningTime();
        currentChannelUrl = $('body').data('secondChannelUrl');
        currentChannelName = $('body').data('secondChannelName');

        loadRating();
    });
});

// Trzecia sugestia
$(document).ready(function () {
    $("body").on('click', '#thirdSuggestion', function () {
        var stream = {
            title: $('body').data('thirdChannelName'),
            mp3: $('body').data('thirdChannelUrl')
        }

        imgSrc = $('body').data('thirdImagePath')

        $('#jquery_jplayer_1').jPlayer('setMedia', stream);
        $("#currentChannelLogo").attr('src', imgSrc);

        logListeningTime();
        currentChannelUrl = $('body').data('thirdChannelUrl');
        currentChannelName = $('body').data('thirdChannelName');

        loadRating();
    });
});

// Inicjalizacja ratingu
$(document).ready(function () {
    $('#userStarRating').rating({
        hoverEnabled: false,
        showCaption: false
    });
});

// Zmiana ratingu
$(document).on('ready', function () {
    $("#userStarRating").rating().on("rating.clear", function (event) {
        if (currentChannelName != "") {

            $.ajax({
                url: 'rating',
                type: "POST",
                data: {
                    'currentChannelName': currentChannelName,
                    'value': "0",
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                }
            })
        }
    }).on("rating.change", function (event, value) {
        if (currentChannelName != "") {

            $.ajax({
                url: 'rating',
                type: "POST",
                data: {
                    'currentChannelName': currentChannelName,
                    'value': value,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                }
            })
        }
    });
});

// Wczytanie ratingu
function loadRating() {

    $.ajax({
        url: 'rating',
        type: "GET",
        data: {
            'currentChannelName': currentChannelName,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data) {
            $("#userStarRating").rating("update", data);
        }
    })
};

// Wczytanie listy stacji
$(document).on('ready', function () {

    $.ajax({
        url: 'channelList',
        type: "GET",
        success: function (data, textStatus, jqXHR) {
            i = 0;
            $.each(
                data,
                function (i) {
                    $("#station-list").append("<li><a class='channelRef' id='" + data[i] + "'>" + data[i] + "</a></li>");
                }
            );

        }
    })

    $.ajax({
    	url: 'privateChannelList',
    	type: "GET",
    	success: function (data, textStatus, jqXHR) {
    		i = 0;
    		$.each(
                data,
                function (i) {
                	$("#station-list").append("<li><a class='privateChannelRef' id='" + data[i] + "'>" + data[i] + "</a></li>");
                }
            );

    	}
    })

});