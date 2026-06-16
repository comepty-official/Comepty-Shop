/* Comepty — Main JS */

document.addEventListener('DOMContentLoaded', function () {

  // ---- DARK MODE ----
  const themeToggle = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('comepty-theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      const current = document.documentElement.getAttribute('data-theme');
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('comepty-theme', next);
    });
  }

  // ---- IMAGE GALLERY (product detail) ----
  const thumbs = document.querySelectorAll('.gallery-thumb');
  const mainImg = document.getElementById('galleryMain');

  thumbs.forEach(function (thumb) {
    thumb.addEventListener('click', function () {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');
      if (mainImg) {
        mainImg.style.opacity = '0';
        setTimeout(function () {
          mainImg.src = thumb.dataset.full;
          mainImg.style.opacity = '1';
        }, 150);
        mainImg.style.transition = 'opacity 0.2s ease';
      }
    });
  });

  // ---- LIKE BUTTON (AJAX) ----
  const likeBtn = document.getElementById('likeBtn');
  if (likeBtn) {
    likeBtn.addEventListener('click', function () {
      const slug = likeBtn.dataset.slug;
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
      if (!csrfToken) {
        window.location.href = '/users/login/?next=' + window.location.pathname;
        return;
      }
      fetch('/products/' + slug + '/like/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken.value,
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
        .then(r => r.json())
        .then(data => {
          const countEl = document.getElementById('likeCount');
          if (countEl) countEl.textContent = data.count;
          if (data.liked) {
            likeBtn.classList.add('liked');
            likeBtn.title = 'Unlike';
            likeBtn.querySelector('span') && (likeBtn.querySelector('span').textContent = '❤️');
            // Pulse animation
            likeBtn.style.transform = 'scale(1.3)';
            setTimeout(() => likeBtn.style.transform = '', 200);
          } else {
            likeBtn.classList.remove('liked');
            likeBtn.title = 'Like';
            likeBtn.querySelector('span') && (likeBtn.querySelector('span').textContent = '🤍');
          }
        })
        .catch(console.error);
    });
  }

  // ---- SAVE BUTTON (AJAX) ----
  const saveBtn = document.getElementById('saveBtn');
  if (saveBtn) {
    saveBtn.addEventListener('click', function () {
      const slug = saveBtn.dataset.slug;
      const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
      if (!csrfToken) {
        window.location.href = '/users/login/?next=' + window.location.pathname;
        return;
      }
      fetch('/products/' + slug + '/save/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken.value,
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
        .then(r => r.json())
        .then(data => {
          if (data.saved) {
            saveBtn.classList.add('saved');
            saveBtn.title = 'Unsave';
          } else {
            saveBtn.classList.remove('saved');
            saveBtn.title = 'Save';
          }
        })
        .catch(console.error);
    });
  }

  // ---- AUTO-DISMISS ALERTS ----
  const alerts = document.querySelectorAll('.alert-comepty');
  alerts.forEach(function (alert) {
    setTimeout(function () {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-8px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 4000);
  });

  // ---- INTERSECTION OBSERVER (card animation) ----
  const cards = document.querySelectorAll('.product-card');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    cards.forEach(function (card) {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      observer.observe(card);
    });
  }

  // ---- IMAGE UPLOAD PREVIEW ----
  const imageInputs = document.querySelectorAll('.image-file-input');
  imageInputs.forEach(function (input) {
    input.addEventListener('change', function () {
      const slot = input.closest('.image-upload-slot');
      const file = input.files[0];
      if (file && slot) {
        const reader = new FileReader();
        reader.onload = function (e) {
          slot.style.backgroundImage = 'url(' + e.target.result + ')';
          slot.style.backgroundSize = 'cover';
          slot.style.backgroundPosition = 'center';
          slot.style.color = 'transparent';
          const icon = slot.querySelector('.upload-icon');
          if (icon) icon.style.display = 'none';
          const label = slot.querySelector('.upload-label');
          if (label) label.style.display = 'none';
        };
        reader.readAsDataURL(file);
      }
    });
  });

  // ---- MOBILE SEARCH ----
  const mobileSearchToggle = document.getElementById('mobileSearchToggle');
  const mobileSearchBar = document.getElementById('mobileSearchBar');
  if (mobileSearchToggle && mobileSearchBar) {
    mobileSearchToggle.addEventListener('click', function () {
      mobileSearchBar.classList.toggle('show');
      if (mobileSearchBar.classList.contains('show')) {
        mobileSearchBar.querySelector('input') && mobileSearchBar.querySelector('input').focus();
      }
    });
  }

  // ---- SMOOTH SCROLL TO TOP ----
  const scrollTopBtn = document.getElementById('scrollTopBtn');
  if (scrollTopBtn) {
    window.addEventListener('scroll', function () {
      scrollTopBtn.style.opacity = window.scrollY > 300 ? '1' : '0';
    });
    scrollTopBtn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

});
