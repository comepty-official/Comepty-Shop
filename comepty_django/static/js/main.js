/* =============================================
   COMEPTY — Main JavaScript
============================================= */

// Theme management
function initTheme() {
  const saved = localStorage.getItem('comepty-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  updateThemeIcon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('comepty-theme', next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const icon = document.getElementById('themeIcon');
  if (icon) icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
}

// Mobile menu
function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  const btn = document.getElementById('hamburger');
  menu.classList.toggle('open');
  btn.classList.toggle('open');
}

// User dropdown
function toggleUserMenu() {
  const dropdown = document.getElementById('userDropdown');
  if (dropdown) dropdown.classList.toggle('open');
}

// Close dropdowns on outside click
document.addEventListener('click', function(e) {
  if (!e.target.closest('.nav-user-menu')) {
    const d = document.getElementById('userDropdown');
    if (d) d.classList.remove('open');
  }
  if (!e.target.closest('.hamburger') && !e.target.closest('.mobile-menu')) {
    const m = document.getElementById('mobileMenu');
    if (m) m.classList.remove('open');
  }
});

// CSRF cookie helper
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// AJAX Like toggle
function toggleLike(productId, btn) {
  const csrfToken = getCookie('csrftoken');
  if (!csrfToken) {
    window.location.href = '/users/login/';
    return;
  }

  fetch(`/products/${productId}/like/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
  .then(r => {
    if (r.status === 403 || r.redirected) {
      window.location.href = '/users/login/';
      return null;
    }
    return r.json();
  })
  .then(data => {
    if (!data) return;
    const icon = btn.querySelector('i');
    const countEl = btn.querySelector('.like-count') || btn.querySelector('span');

    if (data.liked) {
      if (icon) icon.className = 'bi bi-heart-fill';
      btn.classList.add('liked');
      animatePop(btn);
    } else {
      if (icon) icon.className = 'bi bi-heart';
      btn.classList.remove('liked');
    }

    if (countEl) countEl.textContent = data.count;

    // Also update the main like button if it's a card click
    const mainLikeCount = document.getElementById('likeCount');
    if (mainLikeCount) mainLikeCount.textContent = data.count;
  })
  .catch(err => console.error('Like error:', err));
}

// AJAX Save toggle
function toggleSave(productId, btn) {
  const csrfToken = getCookie('csrftoken');
  if (!csrfToken) {
    window.location.href = '/users/login/';
    return;
  }

  fetch(`/products/${productId}/save/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': csrfToken,
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
  .then(r => {
    if (r.status === 403 || r.redirected) {
      window.location.href = '/users/login/';
      return null;
    }
    return r.json();
  })
  .then(data => {
    if (!data) return;
    const icon = btn.querySelector('i');

    if (data.saved) {
      if (icon) icon.className = 'bi bi-bookmark-fill';
      btn.classList.add('saved');
      animatePop(btn);
    } else {
      if (icon) icon.className = 'bi bi-bookmark';
      btn.classList.remove('saved');
    }
  })
  .catch(err => console.error('Save error:', err));
}

// Pop animation for like/save
function animatePop(el) {
  el.style.transform = 'scale(1.25)';
  setTimeout(() => el.style.transform = '', 200);
}

// Auto-dismiss alerts
function initAlerts() {
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-6px)';
      alert.style.transition = 'all 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 4000);
  });
}

// Scroll reveal animation
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.product-card, .section-card, .blog-card, .user-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(16px)';
    el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(el);
  });
}

// Lazy load images
function initLazyLoad() {
  if ('loading' in HTMLImageElement.prototype) return;
  const images = document.querySelectorAll('img[loading="lazy"]');
  const imgObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src || img.src;
        imgObserver.unobserve(img);
      }
    });
  });
  images.forEach(img => imgObserver.observe(img));
}

// Category bar active item scrolling
function scrollCatIntoView() {
  const active = document.querySelector('.cat-pill.active');
  if (active) {
    active.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  initTheme();
  initAlerts();
  initScrollReveal();
  initLazyLoad();
  scrollCatIntoView();
});
