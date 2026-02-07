<script>
  function searchProduct() {
    const input = document.getElementById("searchInput").value.toLowerCase();

    if (input.includes("hydro") || input.includes("pump") || input.includes("pump")) {
      window.location.href = "hydro_pump";
    } 
    else if (input.includes("thrustor")) {
      window.location.href = "/products/thrustor";
    } 
    else if (input.includes("motor")) {
      window.location.href = "/products/gear-motor";
    } 
    else {
      alert("Product not found!");
    }
  }
</script>
