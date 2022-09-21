let page = 1;

$(document).ready(function () {
  // $(".feed").html("");
  // showAllplaylists(page);
});

let firstScroll = true;
$(window).scroll(function () {
  var scrolltop = $(window).scrollTop();
  if (scrolltop == $(document).height() - $(window).height()) {
    console.log("맨끝 도착");
    if (firstScroll) {
      $(".feed").html("");
    }
    showAllplaylists(page++, firstScroll);
    firstScroll = false;
  }
});

let playlistIndex = 0;
function showAllplaylists(page) {
  console.log("currentpage : ", page);
  $.ajax({
    type: "GET",
    url: `/list/all`,
    data: { page: page },
    success: function (response) {
      if (response["result"] == "success") {
        all_playlists = response["all_playlists"];
        for (let i = 0; i < all_playlists?.length; i++) {
          makeList(
            playlistIndex++,
            all_playlists[i]["user"],
            all_playlists[i]["title"],
            all_playlists[i]["songs"]
          );
        }
      }
    },
  });
}

function showPopularlist() {
  $.ajax({
    type: "GET",
    url: "/list/popular",
    data: {},
    success: function (response) {
      // 성공하면
      if (response["result"] == "success") {
        alert("포스팅 성공!");
        // 3. 성공 시 페이지 새로고침하기
        window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}

function makeList(index, user, title, songs) {
  console.log(index);
  let tempHtml_pl = `<li>
                      <div class="playlist-block playlist-block-${index}">
                        <p class="area-title area-title-${index}">${title} by ${user}</p>
                        <ul class="songs-${index}"></ul>
                      </div>
                    </li>`;
  $(".feed").append(tempHtml_pl);

  if (!songs || songs.length === 0) return;
  for (let j = 0; j < 3; j++) {
    let song_name = songs[j]["songname"];
    let song_artist = songs[j]["artist"];

    let tempHtml_s = `<li>${j + 1}. ${song_name} - ${song_artist}</li>`;

    $(`.songs-${index}`).append(tempHtml_s);
  }
  let spreadButtonHtml = `<button class="spread-button spread-button-${index}"><i class="fa-solid fa-caret-right"></i> 펼쳐보기 </button>`;
  $(`.playlist-block-${index}`).append(spreadButtonHtml);

  const toggleSpreadButton = (function () {
    let spread = false;
    let showCount = 3;
    return function () {
      spread = !spread;
      if (spread) {
        spreadButton.innerHTML = `<i class="fa-solid fa-caret-down"></i> 접기`;
        showCount = songs.length;
        toggle("fold", "spread", showCount);
      } else {
        spreadButton.innerHTML = `<i class="fa-solid fa-caret-right"></i> 펼쳐보기`;
        showCount = 3;
        toggle("spread", "fold", showCount);
      }
    };
  })();

  let spreadButton = document.querySelector(`.spread-button-${index}`);
  spreadButton.addEventListener("click", toggleSpreadButton.bind(null, index));

  function toggle(currentState, nextState, showCount) {
    let start;
    if (currentState === "fold" && nextState === "spread") {
      start = 3;
    } else if (currentState === "spread" && nextState === "fold") {
      start = 0;
      $(`.songs${index}`).html("");
    }

    for (let j = start; j < showCount; j++) {
      let song_name = songs[j]["songname"];
      let song_artist = songs[j]["artist"];
      let tempHtml_s = `<li>${j + 1}. ${song_name} - ${song_artist}</li>`;

      $(`.songs${index}`).append(tempHtml_s);
    }
  }
}

function addPlaylist() {
  let user = $("#add-user").val();
  let title = $("#add-playlist").val();

  $.ajax({
    type: "POST",
    url: "/add/playlist",
    data: { user_give: user, title_give: title },
    success: function (response) {
      if (response["result"] == "success") {
        alert("플레이 리스트 만들기 성공!");

        window.location.reload();
      } else {
        alert("다시 입력하세요!");
      }
    },
  });
}
