$(document).ready(function () {
    $("#list-box").html("");
    showAllplaylists();
});

function showAllplaylists() {
    $.ajax({
        type: "GET",
        url: "/list/all",
        data: {},
        success: function (response) {
            if (response["result"] == "success") {

                all_playlists = response['all_playlists']

                for (let i = 0; i < all_playlists.length; i++) {
                    makeList(all_playlists[i]["user"], all_playlists[i]["title"], all_playlists[i]["songs"]);
                }
            }
        }
    })
}

function makeList(user, title, songs) {

    let tempHtml_pl = `<div class="playlist-block">
                        <p class="area-title">${user} by ${title}</p>
                        <button>펼쳐보기</button>
                    </div>`
    $(".feed").append(tempHtml_pl);

    for (let j = 0; j < songs.length; j++) {
        
        let song_name = songs[j]['songname']
        let song_artist = songs[j]['artist']

        let tempHtml_s = `<p>1. ${song_name} - ${song_artist}</p>`;

        $(".area-title").append(tempHtml_s);

    }
}


function addPlaylist() {
    let user = $("#add-user").val();
    let title = $("#add-playlist").val();


    $.ajax({
        type: "POST",
        url: "/add/playlist",
        data: { user_give: user, title_give: title },
        success: function (response) { // 성공하면
            if (response["result"] == "success") {
                alert("포스팅 성공!");
                // 3. 성공 시 페이지 새로고침하기
                window.location.reload();
            } else {
                alert("다시 입력하세요!")
            }
        }
    })
}