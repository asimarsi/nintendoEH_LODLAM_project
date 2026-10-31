/* 1. Mobile navigation: keyboard-friendly and closed after selecting a section. */
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
  mobileNav.hidden = true;
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  mobileNav.hidden = !open;
});
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && !mobileNav.hidden) { closeMenu(); menuButton.focus(); }
});

/* 2. Filter the catalogue without changing the source data. */
const cards = [...document.querySelectorAll('.entity-card')];
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const search = document.querySelector('#entity-search');
let category = 'all';
function updateEntities() {
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  cards.forEach(card => {
    const matches = (category === 'all' || card.dataset.group === category) &&
      card.dataset.name.includes(query);
    card.hidden = !matches;
    if (matches) visible++;
  });
  document.querySelector('#entity-count').textContent = `Showing ${visible} of ${cards.length} entities`;
  document.querySelector('.empty-state').hidden = visible !== 0;
}
filterButtons.forEach(button => button.addEventListener('click', () => {
  category = button.dataset.filter;
  filterButtons.forEach(item => {
    const active = item === button;
    item.classList.toggle('active', active);
    item.setAttribute('aria-pressed', String(active));
  });
  updateEntities();
}));
search.addEventListener('input', updateEntities);

/* 3. Follow the reader's position and update the section guide. */
const sections = [...document.querySelectorAll('.report-section')];
const guideLinks = [...document.querySelectorAll('.reading-nav nav a')];
let scheduled = false;
function updateReadingPosition() {
  const scrollable = document.documentElement.scrollHeight - window.innerHeight;
  document.querySelector('.reading-progress span').style.width = `${scrollable > 0 ? 100 * window.scrollY / scrollable : 0}%`;
  let current = sections[0].id;
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= 180) current = section.id;
  }
  guideLinks.forEach(link => {
    const active = link.hash === `#${current}`;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; requestAnimationFrame(updateReadingPosition); }
}, { passive: true });
updateReadingPosition();

/* 4. Open credits before following an attribution link inside the disclosure. */
function revealCredits() {
  if (location.hash.startsWith('#credit-') || location.hash === '#image-credits') {
    document.querySelector('#image-credits').open = true;
    requestAnimationFrame(() => document.querySelector(location.hash)?.scrollIntoView());
  }
}
window.addEventListener('hashchange', revealCredits);
revealCredits();
