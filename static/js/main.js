/**
 * СОЧНОАВТО - Main JavaScript
 */

// Search autocomplete - URL настраивается в data-search-url атрибуте
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('searchInput');
  const searchResults = document.getElementById('searchResults');
  
  if (searchInput && searchResults) {
    const searchUrl = searchInput.dataset.searchUrl || '/api/search/';
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
        fetch(searchUrl + '?search=' + encodeURIComponent(query))
          .then(response => response.json())
          .then(data => {
            let results = [];
            if (Array.isArray(data)) {
              results = data;
            } else if (data.results) {
              results = data.results;
            } else if (data.Stamp || data.Model || data.stamp || data.model) {
              results = [data];
            }
            renderSearchResults(results, searchResults);
            searchResults.classList.toggle('d-none', results.length === 0);
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

function renderSearchResults(results, container) {
  const baseUrl = container.dataset.offerBaseUrl || '';
  container.innerHTML = results.map(item => {
    const title = (item.Stamp || item.stamp || '') + ' ' + (item.Model || item.model || '');
    const meta = [
      item.Year || item.year,
      item.EngineVolume || item.engine_volume,
      item.Transmission || item.transmission
    ].filter(Boolean).join(' | ');
    
    const slug = item.slug || item.Slug;
    const id = item.id || item.Id;
    const url = item.url || item.Url || (slug ? baseUrl + slug + '/' : id ? baseUrl + id + '/' : '#');
    
    return `<a href="${url}" class="search-result-item">
      <div class="search-result-title">${escapeHtml(title.trim() || 'Автомобиль')}</div>
      ${meta ? `<div class="search-result-meta">${escapeHtml(meta)}</div>` : ''}
    </a>`;
  }).join('');
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

// Carousel: свайпы на телефоне (touch: true при инициализации)
document.querySelectorAll('.carousel').forEach(function (el) {
  if (typeof bootstrap === 'undefined' || !bootstrap.Carousel) return;
  bootstrap.Carousel.getOrCreateInstance(el, { touch: true });
});