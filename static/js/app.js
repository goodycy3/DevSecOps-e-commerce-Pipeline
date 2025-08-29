document.addEventListener('DOMContentLoaded', () => {
  // Header shadow on scroll
  const header = document.getElementById('header');
  if (header) {
    addEventListener('scroll', () => {
      if (scrollY > 10) header.classList.add('header-scrolled');
      else header.classList.remove('header-scrolled');
    });
  }

  // Theme toggle
  const html = document.documentElement;
  const toggle = document.getElementById('themeToggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      html.classList.toggle('dark');
      localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
    });
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

  // Safe query string display (if you want to mirror ?msg= as plain text)
  try {
    const el = document.getElementById('welcome');
    const msg = new URLSearchParams(location.search).get('msg');
    if (el && msg) {
      const div = document.createElement('div');
      div.className = 'mt-2 text-slate-700';
      div.textContent = msg; // text only, no HTML
      el.appendChild(div);
    }
  } catch (_) {}
});
