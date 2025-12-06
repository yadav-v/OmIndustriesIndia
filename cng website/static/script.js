// Example interactivity (you can expand this)
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('click', () => {
    alert("This button is for demo purpose only!");
  });
});
document.getElementById('openPopup').addEventListener('click', function() {
  document.getElementById('popupForm').style.display = 'flex';
});

document.getElementById('closePopup').addEventListener('click', function() {
  document.getElementById('popupForm').style.display = 'none';
});
window.onclick = function(event) {
  if (event.target == document.getElementById("popupForm")) {
    document.getElementById("popupForm").style.display = "none";
  }
}

// Email button action
document.getElementById('sendEmailBtn').addEventListener('click', function() {
  const email = 'you@yourdomain.com';
  const subject = encodeURIComponent('Inquiry from OM Industries');
  const body = encodeURIComponent('Hello OM Industries,\n\nI would like to know about...');
  window.location.href = `mailto:${email}?subject=${subject}&body=${body}`;
});


