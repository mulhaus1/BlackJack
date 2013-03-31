$('.join').click(function (){
    var username = $('#username').val();
    var currGame = event.target.id;
    if (username != "") {
        var game_url = 'http://127.0.0.1:8080/game/' + currGame + '/playerConnect?username=' + username;
        $.post(game_url, function (data) {
           if (data == "error") {
               alert("Sorry, game is full");
           }
           else if (data == "ok") {
               alert("ok")
               window.location.href = 'http://127.0.0.1:8080/game/' + currGame + '/visible_table?player=' + username;
           }
           else {
               alert("error, unknown")
           }
        }).fail(function () {
                alert("failed on post")
            });
    }
    else {
        alert("Invalid username or game")
    }
});