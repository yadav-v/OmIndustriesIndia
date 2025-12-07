// Slick Slider Initialization
$(document).ready(function () {
  if ($('.heroSlider').length) {

    $('.heroSlider').slick({
      dots: false,
      infinite: true,
      speed: 500,
      fade: true,
      cssEase: 'linear',
      autoplay: true,
      autoplaySpeed: 4000,
      arrows: false   // disable default arrows
    });

    // Custom Btn Events
    $('.hero-prev').click(function () {
      $('.heroSlider').slick('slickPrev');
    });

    $('.hero-next').click(function () {
      $('.heroSlider').slick('slickNext');
    });
  }
});


// Rating Input Styling for both regular and modal
document.addEventListener('DOMContentLoaded', function() {
  // Handle regular rating input
  const ratingInputs = document.querySelectorAll('.rating-input input[type="radio"]');
  const starLabels = document.querySelectorAll('.rating-input .star-label');
  
  ratingInputs.forEach((input, index) => {
    input.addEventListener('change', function() {
      starLabels.forEach((label, labelIndex) => {
        if (labelIndex <= index) {
          label.classList.add('active');
        } else {
          label.classList.remove('active');
        }
      });
    });
  });
  
  // Set initial active state for regular input
  const checkedInput = document.querySelector('.rating-input input[type="radio"]:checked');
  if (checkedInput) {
    const checkedIndex = Array.from(ratingInputs).indexOf(checkedInput);
    starLabels.forEach((label, labelIndex) => {
      if (labelIndex <= checkedIndex) {
        label.classList.add('active');
      }
    });
  }
  
  // Handle modal rating input
  const modalRatingInputs = document.querySelectorAll('.rating-input-modal input[type="radio"]');
  const modalStarLabels = document.querySelectorAll('.rating-input-modal .star-label-modal');
  
  modalRatingInputs.forEach((input, index) => {
    input.addEventListener('change', function() {
      modalStarLabels.forEach((label, labelIndex) => {
        if (labelIndex <= index) {
          label.classList.add('active');
        } else {
          label.classList.remove('active');
        }
      });
    });
  });
  
  // Set initial active state for modal input
  const modalCheckedInput = document.querySelector('.rating-input-modal input[type="radio"]:checked');
  if (modalCheckedInput) {
    const modalCheckedIndex = Array.from(modalRatingInputs).indexOf(modalCheckedInput);
    modalStarLabels.forEach((label, labelIndex) => {
      if (labelIndex <= modalCheckedIndex) {
        label.classList.add('active');
      }
    });
  }
  
  // Reset modal form when modal is closed
  const feedbackModal = document.getElementById('feedbackModal');
  if (feedbackModal) {
    feedbackModal.addEventListener('hidden.bs.modal', function () {
      const form = feedbackModal.querySelector('form');
      if (form) {
        form.reset();
        // Reset to default rating
        const defaultInput = feedbackModal.querySelector('input[type="radio"][value="5"]');
        if (defaultInput) {
          defaultInput.checked = true;
          modalStarLabels.forEach((label, labelIndex) => {
            if (labelIndex <= 0) { // 5 stars is first (index 0)
              label.classList.add('active');
            } else {
              label.classList.remove('active');
            }
          });
        }
      }
    });
  }
});
