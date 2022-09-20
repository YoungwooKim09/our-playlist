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
