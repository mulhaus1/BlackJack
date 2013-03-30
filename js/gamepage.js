$('.join').click(function (){
    var username = $('#username').val;
    var currGame = $(this.id)
    if (username != null && currGame != null) {
        var game_url = 'http://127.0.0.1:8080/game/' + currGame + '/playerConnect?username=' + username;
        $.post(link, function (data) {
           if (data == 0) {
               alert("Sorry, game is full");
           }
           else if (data == 1) {
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