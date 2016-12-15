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

        logListeningTime();
        currentChannelUrl = $('body').data('firstChannelUrl');
        currentChannelName = $('body').data('firstChannelName');
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
    });
});

function logListeningTime() {
	endDate = new Date();
	endDateISO = endDate.toISOString();
	startDateISO = startDate.toISOString();

	$.ajax({
		url: 'logTime',
		type: "POST",
		data: {
			'currentChannelName': currentChannelName,
			'startTimestamp': startDateISO,
			'endTimestamp': endDateISO,
			'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
		},
		success: function (data) {
			$('#jp-meta').html(data);
		}
	})
}