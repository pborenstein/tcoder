// script.js

const img = document.getElementById('img');
const refreshBtn = document.getElementById('refresh');

function getRandomImage() {
  const randomImageUrl = `https://picsum.photos/400/?random=${Math.random()}`;
  img.src = randomImageUrl;
}

refreshBtn.addEventListener('click', getRandomImage);