function deletePlaylist(index) {
  let delete_title = $(".area-title" + index).text();

  $.ajax({
    type: "POST",
    url: "/delete/playlist",
    data: { delete_give: delete_title },
    success: function (response) {
      if (response["result"] == "success") {
        alert("플레이 리스트 삭제 완료!");
        window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}

function searchSong(id) {
  let search_song = $("#input-search").val();
  let playlist_id = id

  $.ajax({
    type: "POST",
    url: "/search",
    data: { search_give: search_song },
    success: function (response) {
      if (response["result"] == "success") {
        console.log(response["song"]);
        searchList = response["song"];
        for (let i = 0; i < searchList.length; i++) {
          makeSearchList(
            searchList[i]["song_name"],
            searchList[i]["song_singer"],
            playlist_id
          );
        }
      }
    },
  });
}

function makeSearchList(songName, songArtist, playlist_id) {
  let tempHtml = `<li><span id="add-song">${songName}</span>
  <span> - </span>
  <span id="add-artist">${songArtist}</span>
  <button onclick="addSong(${songName},${songArtist},${playlist_id})">추가</button>
  </li>`
  $(".search-result").append(tempHtml);
}

// 버튼 추가하여 연결

function addSong(songName, songArtist, playlist_title) {
  let song = songName;
  let artist = songArtist;
  let title = playlist_title;
  // 버튼에 해당하는 텍스트 요소
  // 함수 인자로 id값 사용

  $.ajax({
    type: "POST",
    url: "/add/song",
    data: { song_give: song, artist_give: artist, title_give: title },
    success: function (response) {
      // 성공하면
      if (response["result"] == "success") {
        alert("저장 성공!");
        // 3. 성공 시 페이지 새로고침하기
        window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}

function deleteSong() {
  let title = $("#song-delete-title").text(); //버튼의 속성값
  let delete_song_name = $("#song-delete-name").text();
  let delete_song_artist = $("#song-delete-artist").text();

  $.ajax({
    type: "POST",
    url: "/delete/song",
    data: {
      title_give: title,
      song_give: delete_song_name,
      artist_give: delete_song_artist,
    },
    success: function (response) {
      if (response["result"] == "success") {
        alert("노래 삭제 성공!");
        window.location.reload();
      }
    },
  });
}

function addPlaylist(title, user) {
  console.log("add playlist 호출");
  $.ajax({
    type: "POST",
    url: "/add/playlist",
    data: { title: title, user: user },
    success: function (response) {
      // 성공하면
      if (response["result"] == "success") {
        location.reload();
        alert("포스팅 성공!");
        // 3. 성공 시 페이지 새로고침하기
        // window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}

function showMyPlaylists() {
  let userId = null;
  const cookies = document.cookie.split("; ");
  for (let cookie of cookies) {
    const [name, value] = cookie.split("=");
    if (name === "userinfo") {
      userinfo = JSON.parse(value);
      for (let key in userinfo) {
        if (key === "id") {
          userId = userinfo[key];
        }
      }
    }
  }
  $.ajax({
    type: "GET",
    url: `/list/myplaylist`,
    data: { user_id: userId },
    success: function (response) {
      console.log("success");
      // if (response["result"] == "success") {
      //   my_playlists = response["my_playlists"];
      //   console.log(my_playlists)
      // }
    },
  });
}
