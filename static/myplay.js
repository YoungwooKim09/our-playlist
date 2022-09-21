const createPlaylistButtonArea = document.querySelector(".create-button-area");
const createPlaylistButton = document.querySelector(".create-playlist-button");
const createPlaylistForm = document.querySelector(".create-playlist-form");
const savePlaylistButton = document.querySelector(".save-playlist");

createPlaylistButton.addEventListener("click", showCreatePlaylistForm);

function showCreatePlaylistForm() {
  createPlaylistButtonArea.classList.add("show-form");
  createPlaylistButton.classList.add("hide");
  createPlaylistForm.classList.remove("hide");
}

savePlaylistButton.addEventListener("click", savePlayList);

function savePlayList() {
  console.log(1111);
}
