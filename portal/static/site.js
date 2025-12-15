// portal/static/site.js
document.addEventListener('DOMContentLoaded', function () {
  // Show loader on form submit
  document.querySelectorAll('form').forEach((form) => {
    form.addEventListener('submit', () => {
      const loader = document.getElementById('site-loader');
      if (loader) loader.classList.remove('d-none');
    });
  });

  // Small interaction: add ripple-like press effect on buttons
  document.querySelectorAll('.btn').forEach((btn) => {
    btn.addEventListener('mousedown', () => btn.classList.add('pressed'));
    btn.addEventListener('mouseup', () => btn.classList.remove('pressed'));
    btn.addEventListener('mouseleave', () => btn.classList.remove('pressed'));
  });
});
