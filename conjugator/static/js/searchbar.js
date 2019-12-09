document.querySelector('.search-bar').addEventListener('click', (e) => {
  if (e.target.classList.contains('letter')) {
      e.preventDefault();
      const inputEl = document.querySelector('#search');
      inputEl.value += e.target.innerHTML;
      inputEl.focus();
  }
});