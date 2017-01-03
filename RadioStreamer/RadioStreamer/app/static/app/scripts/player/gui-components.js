// zmienne do przetrzymywania informacji o polecankach
var firstChannelName;
var firstChannelUrl;
var secondChannelName;
var secondChannelUrl;
var thirdChannelName;
var thirdChannelUrl;

// Odświezanie polecanek co minutę
$(document).ready(function () {
    // pierwszy raz od razu przy wczytaniu
    refreshSuggestions()

    setInterval(refreshSuggestions, 60000)
});

function refreshSuggestions() {
    $.ajax({
        url: 'suggestions',
        success: function (data) {
            $('#sidebar').html(data);
        },
        success: function (data, textStatus, jqXHR) {
            firstChannelName = data.FirstChannelName;
            firstChannelUrl = data.FirstChannelUrl;
            secondChannelName = data.SecondChannelName;
            secondChannelUrl = data.SecondChannelUrl;
            thirdChannelName = data.ThirdChannelName;
            thirdChannelUrl = data.ThirdChannelUrl;

            $.ajax({
                url: 'sidebar',
                type: "GET",
                data: {
                    'firstChannelName': firstChannelName,
                    'secondChannelName': secondChannelName,
                    'thirdChannelName': thirdChannelName,
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (data) {
                    $('#sidebar').html(data);
                }
            })
        }
    });
};

// Pierwsza sugestia
$(document).ready(function () {
	$('body').on('click', '#firstSuggestion', function () {
		if (currentChannelName != firstChannelName) {
			var stream = {
				title: firstChannelName,
				mp3: firstChannelUrl
			}

			imgSrc = "static/app/image/icons/300px/" + firstChannelName + ".png";

			$('#jquery_jplayer_1').jPlayer('setMedia', stream);
			$("#currentChannelLogo").attr('src', imgSrc);

			logListeningTime();
			currentChannelUrl = firstChannelUrl;
			currentChannelName = firstChannelName;

			startDate = new Date();
			loadAdditionalInfo();
		}
    });
});

// Druga sugestia
$(document).ready(function () {
	$("body").on('click', '#secondSuggestion', function () {
		if (currentChannelName != secondChannelName) {
			var stream = {
				title: secondChannelName,
				mp3: secondChannelUrl
			}

			imgSrc = "static/app/image/icons/300px/" + secondChannelName + ".png";

			$('#jquery_jplayer_1').jPlayer('setMedia', stream);
			$("#currentChannelLogo").attr('src', imgSrc);

			logListeningTime();
			currentChannelUrl = secondChannelUrl;
			currentChannelName = secondChannelName;

			startDate = new Date();
			loadAdditionalInfo();
		}
    });
});

// Trzecia sugestia
$(document).ready(function () {
	$("body").on('click', '#thirdSuggestion', function () {
		if (currentChannelName != thirdChannelName) {
			var stream = {
				title: thirdChannelName,
				mp3: thirdChannelUrl
			}

			imgSrc = "static/app/image/icons/300px/" + thirdChannelName + ".png";

			$('#jquery_jplayer_1').jPlayer('setMedia', stream);
			$("#currentChannelLogo").attr('src', imgSrc);

			logListeningTime();
			currentChannelUrl = thirdChannelUrl;
			currentChannelName = thirdChannelName;

			startDate = new Date();
			loadAdditionalInfo();
		}
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
                url: 'additionalInfo',
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
                url: 'additionalInfo',
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
function loadAdditionalInfo() {

    $.ajax({
        url: 'additionalInfo',
        type: "GET",
        data: {
            'currentChannelName': currentChannelName,
            'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
        },
        success: function (data, textStatus, jqXHR) {
            $("#userStarRating").rating("update", data.value);
            $("#squaredOne").prop('checked', data.isFavorite);
        }
    })
};

// Wczytanie listy stacji
$(document).on('ready', function () {
	// Wszystkie
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
	// Prywatne
	$.ajax({
		url: 'privateChannelList',
		type: "GET",
		success: function (data, textStatus, jqXHR) {
			i = 0;
			$.each(
                data,
                function (i) {
                	$("#private-station-list").append("<li><a class='privateChannelRef' id='" + data[i] + "'>" + data[i] + "</a></li>");
                }
            );

		}
	})
	//Ulubione
	$.ajax({
		url: 'favoriteList',
		success: function (data, textStatus, jqXHR) {
		    $("#favorite-list").append("<li><a href='#' class='active'>Ulubione stacje</a></li>");
			i = 0;
			$.each(
				data,
				function (i) {
				    $("#favorite-list").append("<li><a class='channelRef site-text fav-channel' id='" + data[i] + "'>" + data[i] + "</a></li>");
				}
			)}
		});
});

// Przedładowywanie stacji ulubionych przy zmianie stanu checkboxa
$(document).on('ready', function () {
    $('#squaredOne').change(function () {

        if (document.getElementById('squaredOne').checked)
        {
            $.ajax({
                url: 'favoriteList',
                type: "POST",
                data: {
                    'currentChannelName': currentChannelName,
                    'operation': "Add",
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (data, textStatus, jqXHR) {
                    $("#favorite-list").empty();
                    $("#favorite-list").append("<li><a href='#' class='active'>Ulubione stacje</a></li>");
                    i = 0;
                    $.each(
                        data,
                        function (i) {
                            $("#favorite-list").append("<li class='fav-channel'><a class='channelRef site-text' id='" + data[i] + "'>" + data[i] + "</a></li>");
                        }
                    )}
            })
        }
        else
        {
            $.ajax({
                url: 'favoriteList',
                type: "POST",
                data: {
                    'currentChannelName': currentChannelName,
                    'operation': "Delete",
                    'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (data, textStatus, jqXHR) {
                    $("#favorite-list").empty();
                    $("#favorite-list").append("<li><a href='#' class='active'>Ulubione stacje</a></li>");
                    i = 0;
                    $.each(
                        data,
                        function (i) {
                            $("#favorite-list").append("<li class='fav-channel'><a class='channelRef site-text' id='" + data[i] + "'>" + data[i] + "</a></li>");
                        }
                    )
                }
            })
        }

    });

});