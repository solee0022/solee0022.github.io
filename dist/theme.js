(() => {
  const root = document.documentElement;
  const system = window.matchMedia('(prefers-color-scheme: dark)');
  let preference = null;
  try { preference = localStorage.getItem('solee-theme'); } catch (_) {}
  if (!['light', 'dark'].includes(preference)) preference = null;
  const apply = theme => {
    root.dataset.theme = theme;
    const button = document.querySelector('.theme-toggle');
    if (!button) return;
    const dark = theme === 'dark';
    button.setAttribute('aria-label', `Switch to ${dark ? 'light' : 'dark'} mode`);
    button.setAttribute('aria-pressed', String(dark));
    button.querySelector('.theme-label').textContent = dark ? 'Light' : 'Dark';
    button.querySelector('.theme-icon').textContent = dark ? '☀' : '☾';
  };
  apply(preference || (system.matches ? 'dark' : 'light'));
  document.addEventListener('DOMContentLoaded', () => {
    apply(root.dataset.theme);
    document.querySelector('.theme-toggle').addEventListener('click', () => {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try { localStorage.setItem('solee-theme', preference); } catch (_) {}
      apply(preference);
    });
    const sections = [...document.querySelectorAll('main section[id]')];
    const links = [...document.querySelectorAll('nav a[href^="#"]')];
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(entries => {
        for (const entry of entries) if (entry.isIntersecting) {
          links.forEach(link => {
            if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
            else link.removeAttribute('aria-current');
          });
        }
      }, {rootMargin: '-15% 0px -65% 0px'});
      sections.forEach(section => observer.observe(section));
    }
  });
  system.addEventListener('change', event => {
    if (!preference) apply(event.matches ? 'dark' : 'light');
  });
})();
