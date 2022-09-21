showMyPlaylists();

const createPlaylistButtonArea = document.querySelector(".create-button-area");
const createPlaylistButton = document.querySelector(".create-playlist-button");
const createPlaylistFormWrapper = document.querySelector(
  ".create-playlist-form-wrapper"
);

const createPlaylistForm = document.querySelector(".create-playlist-form");
const playlistTitleInput = document.querySelector(".playlist-title-input");
const savePlaylistButton = document.querySelector(".save-playlist");

createPlaylistButton.addEventListener("click", showCreatePlaylistForm);

function showCreatePlaylistForm() {
  createPlaylistButtonArea.classList.add("show-form");
  createPlaylistButton.classList.add("hide");
  createPlaylistFormWrapper.classList.remove("hide");
}

savePlaylistButton.addEventListener("click", savePlayList);

function savePlayList() {
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

  const title = playlistTitleInput.value;
  if (!title) return;
  addPlaylist(title, userId);
  playlistTitleInput.value = "";
}

createPlaylistForm.addEventListener("keydown", keyPress);

function keyPress(event) {
  if (event.key === "Enter") {
    event.preventDefault();
    savePlayList();
  }
}
