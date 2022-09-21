function deletePlaylist(index) {

  let delete_title = $(".area-title" + index).text();

  $.ajax({
    type: "POST",
    url: "/delete/playlist",
    data: { delete_give: delete_title },
    success: function (response) {
      if (response["result"] == "success") {

        alert("플레이 리스트 삭제 완료!")
        window.location.reload();

      } else {
        alert("다시 입력하세요!")
      }
    }
  })
}

function searchSong() {
  let search_song = $("#search-song").val();

  $.ajax({
    type: "POST",
    url: "/search",
    data: { search_give: search_song },
    success: function (response) {
      if (response["result"] == "success") {
        console.log(response['song']);
        searchList = response['song'];
        for (let i = 0; i < searchList.length; i++) {
          makeSearchList(searchList[i]['song_name'], searchList[i]['song_singer']);
        }
      }
    }
  })
}

function makeSearchList(songName, songArtist) {
  let tempHtml = `<div class="search-songs-area">
                    <p class="search-result">검색 결과</p>
                    <p>${songName} - ${songArtist}</p>
                  </div>`
    $(".search-result").append(tempHtml);
}
// line 42-43 해결하기 : 미리 만들어놓기
// 버튼 추가하여 연결

function addSong() {
  let song = $("#add-song").text();
  let artist = $("#add-artist").text();
  let title = $("#add-title").text();
  // 버튼에 해당하는 텍스트 요소
  // 함수 인자로 id값 사용

  $.ajax({
    type: "POST",
    url: "/add/song",
    data: { song_give: song, artist_give: artist, title_give: title },
    success: function (response) {
      // 성공하면
      if (response["result"] == "success") {
        alert("포스팅 성공!");
        // 3. 성공 시 페이지 새로고침하기
        // window.location.reload();
      } else {
        alert("다시 입력하세요!");
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
        alert("포스팅 성공!");
        // 3. 성공 시 페이지 새로고침하기
        // window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}
