document.addEventListener('DOMContentLoaded', () => {
  // Header shadow on scroll
  const header = document.getElementById('header');
  if (header) {
    addEventListener('scroll', () => {
      if (scrollY > 10) header.classList.add('header-scrolled');
      else header.classList.remove('header-scrolled');
    });
  }

  // Theme toggle (light/dark)
  const html = document.documentElement;
  const toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    });
    // restore
    if (localStorage.getItem('theme') === 'dark') html.classList.add('dark');
  }

  // Add-to-cart animation
  const cartButtons = document.querySelectorAll('.add-to-cart-btn');
  cartButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      if (btn.classList.contains('added')) return;
      btn.classList.add('added');
      btn.textContent = 'Added!';
      setTimeout(() => {
        btn.classList.remove('added');
        btn.textContent = 'Add to cart';
      }, 1800);
    });
  });

  // ============================
  // Intentional vulnerabilities
  // ============================

  // DOM XSS via innerHTML
  try {
    const params = new URLSearchParams(location.search);
    const msg = params.get('msg');
    if (msg) {
      const wel = document.getElementById('welcome') || document.body;
      wel.innerHTML += `<div class="mt-2 text-rose-700">${msg}</div>`; // vulnerable
    }
  } catch (_) {}

  // eval on user input
  try {
    const code = new URLSearchParams(location.search).get('debug');
    if (code) {
      // eslint-disable-next-line no-eval
      eval(code); // vulnerable
    }
  } catch (_) {}

  // open-redirect style + tabnabbing (paired with base.html link)
  try {
    const link = document.getElementById('ext-offer-link');
    if (link) {
      const dest = new URLSearchParams(location.search).get('next');
      if (dest) link.href = dest; // vulnerable
    }
  } catch (_) {}
});
