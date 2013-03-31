$('#bet-button').click(function () {
    console.log("bet button clicked");
    var game_id = window.location.pathname.replace("/game/", "").replace("/visible_table", "");
    var username = window.location.search.replace("?player=", "");
    var value = $('#bet-val').val()
    var intRegex = /^\d+$/;
    if(intRegex.test(value)) {
        var link = window.location.protocol + '//' + window.location.host + '/game/' + game_id + '/action?player=' + username + '&action=bet&value=' + value;
        $.post(link, function(data) {
            if (data == "ok") {
                alert("Bet placed successfully");
                //window.location.href = 'http://127.0.0.1:8080/game/' + game_id + '/visible_table?player=' + username;
                window.location.reload();
            }
            else if (data == "error") {
                alert("Bet failed");
            }
            else {
                alert(data);
            }
        }).fail(function () {
                alert("post failed");
            });
    }
    else {
        alert("Please use only positive integers for your bet")
    }
});

$('#play-button').click(function () {
    console.log("play button clicked");
    var game_id = window.location.pathname.replace("/game/", "").replace("/visible_table", "");
    var username = window.location.search.replace("?player=", "");
    var check_status_link = window.location.protocol + '//' + window.location.host + '/game/' + game_id + '/status?player=' + username;
    $.get(check_status_link, function(data) {
        var status = JSON.parse(data);
        check_play = 0
        actions_array = JSON.parse(status.your_actions)
        $.each(actions_array, function () {
            if (this == "play") {
                check_play = 1;
            }
        });
        if (check_play === 1) {
            var link = window.location.protocol + '//' + window.location.host + '/game/' + game_id + '/action?player=' + username + '&action=play';
            $.post(link, function(data) {
                if (data == "ok") {
                    alert("Play was successful");
                    window.location.reload();
                }
                else if (data == "error") {
                    alert("Play failed");
                }
                else {
                    alert(data);
                }
            }).fail(function () {
                    alert("post failed");
                });
        }
    }).fail(function () {
            alert("post failed");
        });
});

$('#draw-button').click(function () {
    console.log("draw button clicked");
    var game_id = window.location.pathname.replace("/game/", "").replace("/visible_table", "");
    var username = window.location.search.replace("?player=", "");
    var link = 'http://127.0.0.1:8080/game/' + game_id + '/action?action=bet';
    postHandler(link, data, bet())
});

$('#fold-button').click(function () {
    console.log("play button clicked");
    var game_id = window.location.pathname.replace("/game/", "").replace("/visible_table", "");
    var username = window.location.search.replace("?player=", "");
    var link = 'http://127.0.0.1:8080/game/' + game_id + '/action?action=bet';
    postHandler(link, data, bet())
});

$('#dd-button').click(function () {
    console.log("play button clicked");
    var game_id = window.location.pathname.replace("/game/", "").replace("/visible_table", "");
    var username = window.location.search.replace("?player=", "");
    var link = 'http://127.0.0.1:8080/game/' + game_id + '/action?action=bet';
    postHandler(link, data, bet())
});

function postHandler(link, data, func) {
    $.post(link, data, func).fail(function () {
        alert("Error 404 :(");
    });
}

function bet()
{

}

function play()
{

}
