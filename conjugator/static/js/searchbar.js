document.querySelector('.search-bar').addEventListener('mousedown', (e) => {
  if (e.target.classList.contains('letter')) {
      e.preventDefault();
      const inputEl = document.querySelector('#search');
      inputEl.value += e.target.innerHTML;
      inputEl.focus();
  }
});

document.querySelector('.navbar-toggler').addEventListener('click', () => {
  document.querySelector("#navbarNav").classList.toggle('collapse');
});


const verbAutoComplete = new autoComplete({
    selector: 'input[id="search"]',
    source: function(term, suggest) {
        const xhr = new XMLHttpRequest();
        const url = 'http://127.0.0.1:8000/autocomplete';
        xhr.open('GET', url, true)
        xhr.responseType = 'json';
        xhr.onreadystatechange = function() {
            if (this.readyState === 4 && this.status === 200) {
                matches = this.response.filter(verb => verb.includes(term.toLowerCase()));
                suggest(matches);
            }
        }
        xhr.send();
    }
});