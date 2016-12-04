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
    $('body').on('click','#firstSuggestion', function () {

        var stream = {
            title: $('body').data('firstChannelName'),
            mp3: $('body').data('firstChannelUrl')
        }

        imgSrc = $('body').data('firstImagePath')

        $('#jquery_jplayer_1').jPlayer('setMedia', stream);
        $("#currentChannelLogo").attr('src', imgSrc);


        currentChannelUrl = $('body').data('firstChannelUrl')
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

        currentChannelUrl = $('body').data('secondChannelUrl')
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

        currentChannelUrl = $('body').data('thirdChannelUrl')
    });
});