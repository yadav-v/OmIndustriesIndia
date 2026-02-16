// Live search: dropdown suggestions + full results navigation
document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('searchInput');
  const resultsBox = document.getElementById('searchResults');
  if (!input) return;

  let debounceTimer = null;
  let activeIndex = -1;
  let items = [];

  input.addEventListener('input', function(e) {
    const q = input.value.trim();
    clearTimeout(debounceTimer);
    if (q.length < 2) {
      hideResults();
      return;
    }
    debounceTimer = setTimeout(() => fetchSuggestions(q), 250);
  });

  input.addEventListener('keydown', function(e) {
    if (!resultsBox || resultsBox.style.display === 'none') return;
    if (e.key === 'ArrowDown') {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, items.length - 1);
      updateActive();
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      updateActive();
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (activeIndex >= 0 && items[activeIndex]) {
        goToProduct(items[activeIndex].slug);
      } else {
        navigateToSearchResults();
      }
    } else if (e.key === 'Escape') {
      hideResults();
    }
  });

  document.addEventListener('click', function(ev) {
    if (!resultsBox.contains(ev.target) && ev.target !== input) {
      hideResults();
    }
  });

  function fetchSuggestions(q) {
    fetch(`/search?q=${encodeURIComponent(q)}`)
      .then(res => res.json())
      .then(data => {
        items = Array.isArray(data) ? data : [];
        renderResults(items, q);
      }).catch(err => {
        console.error('Search error', err);
        hideResults();
      });
  }

  function renderResults(list, q) {
    if (!list || list.length === 0) {
      hideResults();
      return;
    }
    activeIndex = -1;
    resultsBox.innerHTML = '';
    const ul = document.createElement('ul');
    ul.className = 'list-group';
    list.forEach((it, idx) => {
      const li = document.createElement('li');
      li.className = 'list-group-item list-group-item-action';
      li.setAttribute('role', 'option');
      li.innerHTML = `<strong>${escapeHtml(it.name)}</strong> <small class="text-muted d-block">${escapeHtml(it.short_desc || '')}</small>`;
      li.addEventListener('click', () => goToProduct(it.slug));
      li.addEventListener('mouseenter', () => {
        activeIndex = idx; updateActive();
      });
      ul.appendChild(li);
    });
    resultsBox.appendChild(ul);
    resultsBox.style.display = 'block';
  }

  function updateActive() {
    const nodes = resultsBox.querySelectorAll('.list-group-item');
    nodes.forEach((n, i) => {
      n.classList.toggle('active', i === activeIndex);
    });
  }

  function hideResults() {
    resultsBox.style.display = 'none';
    resultsBox.innerHTML = '';
    activeIndex = -1;
    items = [];
  }

  window.searchNow = function() {
    navigateToSearchResults();
  };

  window.searchAgain = function() { navigateToSearchResults(); };

  function navigateToSearchResults() {
    const q = input.value.trim();
    if (q.length > 0) {
      window.location.href = `/search-results?q=${encodeURIComponent(q)}`;
    }
  }

  function goToProduct(slug) {
    if (!slug) return;
    window.location.href = `/services/product/${encodeURIComponent(slug)}`;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return String(str).replace(/[&<>"'`]/g, function (s) {
      return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;', '`':'&#96;'})[s];
    });
  }
});
