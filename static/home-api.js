let page = 1;

$(document).ready(function () {
  $(".feed").html("");
  const blocks = document.querySelectorAll(".playlist-block");

  for (let i = 0; i < blocks.length; ++i) {
    const attr = blocks[i].getAttribute("order");
    blocks[i].classList.add(`songs${attr}`);
  }

  // showAllplaylists(page);
});

$(window).scroll(function () {
  var scrolltop = $(window).scrollTop();
  if (scrolltop == $(document).height() - $(window).height()) {
    console.log("맨끝 도착");
    showAllplaylists(++page);
  }
});

function toggle(currentState, nextState, maxCount) {
  // const block = document
  //   .querySelectorAll(".playlist-block")[0]
  //   .getAttribute("order");

  let start;
  if (currentState === "fold" && nextState === "spread") {
    start = 3;
  } else if (currentState === "spread" && nextState === "fold") {
    start = 0;
    $(`.songs${index}`).html("");
  }

  // for (let j = start; j < maxCount; j++) {
  //   let song_name = songs[j]["songname"];
  //   let song_artist = songs[j]["artist"];
  //   let tempHtml_s = `<li>${j + 1}. ${song_name} - ${song_artist}</li>`;

  //   $(`.songs${index}`).append(tempHtml_s);
  // }
}

const toggleSpreadButton = (function () {
  let spread = false;
  let maxCount = 3;
  return function () {
    spread = !spread;
    if (spread) {
      spreadButton.innerHTML = `<i class="fa-solid fa-caret-down"></i> 접기`;
      maxCount = 20;
      toggle("fold", "spread", maxCount);
    } else {
      spreadButton.innerHTML = `<i class="fa-solid fa-caret-right"></i> 펼쳐보기`;
      maxCount = 3;
      toggle("spread", "fold", maxCount);
    }
  };
})();

let spreadButton = document.querySelector(`.spread-button`);
spreadButton.addEventListener("click", toggleSpreadButton.bind(null));

function showAllplaylists(page) {
  console.log("currentpage : ", page);
  $.ajax({
    type: "GET",
    url: `/list/all`,
    data: { page: page },
    success: function (response) {
      if (response["result"] == "success") {
        all_playlists = response["all_playlists"];
        console.log("all_playlists", all_playlists);
        for (let i = 0; i < all_playlists?.length; i++) {
          makeList(
            i,
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
  let tempHtml_pl = `<li>
                      <div class="playlist-block playlist-block${index}">
                        <p class="area-title area-title${index}">${title} by ${user}</p>
                        <ul class="songs${index}"></ul>
                      </div>
                    </li>`;
  $(".feed").append(tempHtml_pl);

  if (!songs || songs.length === 0) return;
  for (let j = 0; j < 3; j++) {
    let song_name = songs[j]["songname"];
    let song_artist = songs[j]["artist"];

    let tempHtml_s = `<li>${j + 1}. ${song_name} - ${song_artist}</li>`;

    $(`.songs${index}`).append(tempHtml_s);
  }
  let spreadButtonHtml = `<button class="spread-button spread-button${index}"><i class="fa-solid fa-caret-right"></i> 펼쳐보기 </button>`;
  $(`.playlist-block${index}`).append(spreadButtonHtml);
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
