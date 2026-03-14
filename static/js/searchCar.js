document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  
  if (searchInput && searchResults) {
    const searchUrl = '/api/web1/search-car/';
    let debounceTimer;
    
    searchInput.addEventListener('input', function() {
      const query = this.value.trim();
      
      clearTimeout(debounceTimer);
      
      if (query.length < 2) {
        searchResults.classList.add('d-none');
        searchResults.innerHTML = '';
        return;
      }
      
      debounceTimer = setTimeout(function() {
        fetch(searchUrl + '?page=1&search=' + encodeURIComponent(query))
          .then(response => response.json())
          .then(data => {
            if (data.html_cards) {
              searchResults.classList.remove('d-none');
              searchResults.innerHTML = data.html_cards
            }
          })
          .catch(() => {
            searchResults.classList.add('d-none');
          });
      }, 300);
    });
    
    searchInput.addEventListener('focus', function() {
      if (searchResults.innerHTML && !searchResults.classList.contains('d-none')) {
        searchResults.classList.remove('d-none');
      }
    });
    
    document.addEventListener('click', function(e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.add('d-none');
      }
    });
  }
});

async function replaceSearchCars(element) {
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');

  const page = Number(element.getAttribute('data-page'))

  const query = searchInput.value.trim();
  const searchUrl = `/api/web1/search-car/?page=${page}&search=` + encodeURIComponent(query)

  const result = await fetch(
        searchUrl,
        {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
    const resultJSON = await result.json()
    const htmlSearchCars = resultJSON.html_cards

    searchResults.innerHTML = htmlSearchCars
}

