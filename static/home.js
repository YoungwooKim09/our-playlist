const sortTabArea = document.querySelector(".sort-tab-area");
const sortByTime = document.querySelector(".by-time");
const sortByRandom = document.querySelector(".by-random");
const loginButton = document.querySelector(".home-button-login");

let currentSelectedSortBy = "time";
sortByTime.addEventListener(
  "click",
  selectSortOption.bind(null, "time", currentSelectedSortBy)
);

sortByRandom.addEventListener(
  "click",
  selectSortOption.bind(null, "random", currentSelectedSortBy)
);

function selectSortOption(clicked) {
  if (clicked === "time" && currentSelectedSortBy === "random") {
    sortByTime.classList.add("selected-sort-by");
    sortByRandom.classList.remove("selected-sort-by");
    currentSelectedSortBy = "time";
  } else if (clicked === "random" && currentSelectedSortBy === "time") {
    sortByRandom.classList.add("selected-sort-by");
    sortByTime.classList.remove("selected-sort-by");
    currentSelectedSortBy = "random";
  }
}

const homeLoginButton = document.querySelector(".home-button-login");

$(document).ready(function () {
  if (getUserInfo()) {
    homeLoginButton.classList.add("hide");
  }
});

function getUserInfo() {
  const cookies = document.cookie?.split("; ");
  for (let cookie of cookies) {
    const [name, value] = cookie.split("=");
    if (name === "userinfo") {
      userinfo = JSON.parse(value);
      return userinfo;
    }
  }
}
