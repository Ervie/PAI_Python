// Ustawianie playera
$(document).ready(function () {

    var stream = {
        title: "Gensokyo Radio",
    mp3: "http://stream.gensokyoradio.net:8000/stream/1/"
    },
            ready = false;

    $("#jquery_jplayer_1").jPlayer({
        ready: function (event) {
            ready = true;
            $(this).jPlayer("setMedia", stream);
        },
        pause: function () {
            $(this).jPlayer("clearMedia");
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

    $("#currentChannelLogo").attr('src', "static/app/image/icons/gensokyo.png");
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
			imgSrc = "static/app/image/icons/classic.png"

		} else if (RandomNumber > 0.33) {
			var stream = {
				title: "Gensokyo Radio",
				mp3: "http://stream.gensokyoradio.net:8000/stream/1/"
			}
			imgSrc = "static/app/image/icons/gensokyo.png"
		} else {
			var stream = {
				title: "RMF Game Music",
				mp3: "http://185.69.192.87/GAMEMUSIC"
			}
			imgSrc = "static/app/image/icons/gamemusic.png"
		}

		$('#jquery_jplayer_1').jPlayer('setMedia', stream);
		$("#currentChannelLogo").attr('src', imgSrc);
		
	});
});

// Wczytywanie meta co 10 sekund
$(document).ready(function () {

    setInterval(refreshMeta, 3000)

});

function refreshMeta() {
    $.ajax({
        url: 'metadata',
        success: function (data) {
            $('#jp-meta').html(data);
        }
    })
};
