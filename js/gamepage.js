$('.join').click(function (){
    var username = $('#username').val();
    var currGame = event.target.id;
    if (username != "") {
        var game_url = window.location.protocol + "//" + window.location.host + '/game/' + currGame + '/playerConnect?username=' + username;
        $.post(game_url, function (data) {
           if (data == "error") {
               alert("Sorry, game is full");
           }
           else if (data == "ok") {
               alert("ok")
               window.location.href = window.location.protocol + "//" + window.location.host + '/game/' + currGame + '/visible_table?player=' + username;
           }
           else {
               alert("bad post return")
           }
        }).fail(function () {
                alert("failed on post")
            });
    }
    else {
        alert("Invalid username or game")
    }
});