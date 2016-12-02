$(document).ready(function () {

    var stream = {
        title: "Touhou Radio",
        mp3: "http://37.59.41.178:8000/;stream/1"
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
});

$(document).ready(function () {
	$("#ChangeChannelBtn").click(function () {

		RandomNumber = Math.random();

		if (RandomNumber > 0.66) {
			var stream = {
				title: "RMF Classic",
				mp3: "http://195.150.20.243:8000/rmf_classic"
			}
		} else if (RandomNumber > 0.33) {
			var stream = {
				title: "Touhou Radio",
				mp3: "http://37.59.41.178:8000/;stream/1"
			}
		} else {
			var stream = {
				title: "RMF Game Music",
				mp3: "http://185.69.192.87/GAMEMUSIC"
			}
		}

		

		
		$('#jquery_jplayer_1').jPlayer('setMedia', stream);
		
	});
});
