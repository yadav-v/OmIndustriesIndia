// Search input on key press (live search as you type - shows dropdown)
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener('keyup', function(e) {
      // On Enter key, navigate to search results page
      if (e.key === 'Enter') {
        navigateToSearchResults();
      } else {
        // On other keys, show dropdown results
        performSearch();
      }
    });
  }
});

// Search button click - navigate to full results page
function searchNow() {
  navigateToSearchResults();
}

// Navigate to search results page
function navigateToSearchResults() {
  const query = document.getElementById("searchInput").value.trim();
  if (query.length > 0) {
    window.location.href = `/search-results?q=${encodeURIComponent(query)}`;
  }
}

// Live search - shows dropdown results while typing
function performSearch() {
  const query = document.getElementById("searchInput").value.trim();
  const resultsDiv = document.getElementById("searchResults");

  // Clear results if input is empty
  if (query.length === 0) {
    resultsDiv.innerHTML = '';
    resultsDiv.style.display = 'none';
    return;
  }

  // Fetch results from backend API
  fetch(`/search?q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        // Display results
        let html = '';
        data.forEach(product => {
          html += `
            <a href="/services/product/${product.slug}" class="result-item">
              <i class="fas fa-cube me-2"></i>${product.name}
            </a>
          `;
        });
        resultsDiv.innerHTML = html;
        resultsDiv.style.display = 'block';
      }
    })
    .catch(error => {
      console.error('Search error:', error);
    });
}

// Close search results when clicking outside
document.addEventListener('click', function(event) {
  const searchBox = document.querySelector('.box');
  const resultsDiv = document.getElementById("searchResults");
  
  if (searchBox && !searchBox.contains(event.target)) {
    if (resultsDiv) {
      resultsDiv.style.display = 'none';
    }
  }
});

// Alias function for search results page
function searchAgain() {
  navigateToSearchResults();
}
