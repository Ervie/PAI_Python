// zmienna globalna zawierająca adres radia
var currentChannelUrl;

// Ustawianie playera
$(document).ready(function () {

    var stream = {
        title: "",
        mp3: ""
    },
            ready = false;

    $("#jquery_jplayer_1").jPlayer({
        ready: function (event) {
            ready = true;
            $(this).jPlayer("setMedia", stream);
        },
        pause: function () {
        },
        error: function (event) {
            if (ready && event.jPlayer.error.type === $.jPlayer.error.URL_NOT_SET) {
                // Setup the media stream again and play it.
                $(this).jPlayer("setMedia", stream).jPlayer("play");
            }
        },
        cssSelectorAncestor: "#jp_container_1",
        swfPath: "../player",
        solution: 'html, flash',
        supplied: "mp3, oga",
        useStateClassSkin: true,
        autoBlur: false,
        smoothPlayBar: true,
        keyEnabled: true
    });

    $("#currentChannelLogo").attr('src', "static/app/image/icons/300px/placeholder.png");

    currentChannelUrl = ""
});

// Reset Stacji
//$(this).jPlayer("clearMedia");
$(document).ready(function () {
    $("#MediaResetBtn").click(function () {
        $('#jquery_jplayer_1').jPlayer('clearMedia');
        $("#currentChannelLogo").attr('src', "static/app/image/icons/300px/placeholder.png");
        currentChannelUrl = ""
    });
});
    
// Przedładowania stacji
$(document).ready(function () {
	$("#ChangeChannelBtn").click(function () {

		RandomNumber = Math.random();

		if (RandomNumber > 0.66) {
			var stream = {
				title: "RMF Classic",
				mp3: "http://195.150.20.243:8000/rmf_classic"
			}
			imgSrc = "static/app/image/icons/300px/classic.png"

		} else if (RandomNumber > 0.33) {
			var stream = {
				title: "Gensokyo Radio",
				mp3: "http://stream.gensokyoradio.net:8000/stream/1/"
			}
			imgSrc = "static/app/image/icons/300px/gensokyo.png"
		} else {
			var stream = {
				title: "VGM Radio",
				mp3: "http://radio.vgmradio.com:8040/stream"
			}
			imgSrc = "static/app/image/icons/300px/vgm.png"
		}

		$('#jquery_jplayer_1').jPlayer('setMedia', stream);
		$("#currentChannelLogo").attr('src', imgSrc);
		
		currentChannelUrl = stream.mp3
	});
});

// Wczytywanie meta co 3 sekund
$(document).ready(function () {

    setInterval(refreshMeta, 3000)

});

function refreshMeta() {
    $.ajax({
        url: 'metadata',
        type: "POST",
        data: {
            'currentChannelUrl': currentChannelUrl,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()},
        success: function (data) {
            $('#jp-meta').html(data);
        }
    })
};
