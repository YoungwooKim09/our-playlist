const sortTabArea = document.querySelector(".sort-tab-area");
const sortByTime = document.querySelector(".by-time");
const sortByRandom = document.querySelector(".by-random");

sortTabArea.addEventListener(
  "click",
  (function selectSortOption() {
    let selected = "time";
    return () => {
      if (selected === "time") {
        selected = "random";
        sortByRandom.classList.add("selected-sort-by");
        sortByTime.classList.remove("selected-sort-by");
      } else {
        selected = "time";
        sortByTime.classList.add("selected-sort-by");
        sortByRandom.classList.remove("selected-sort-by");
      }
    };
  })()
);
