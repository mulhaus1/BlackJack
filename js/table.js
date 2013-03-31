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
