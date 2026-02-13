// Search input on key press - navigate to search results page
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById("searchInput");
  if (searchInput) {
    searchInput.addEventListener('keyup', function(e) {
      // On Enter key, navigate to search results page
      if (e.key === 'Enter') {
        navigateToSearchResults();
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

// Alias function for search results page
function searchAgain() {
  navigateToSearchResults();
}
