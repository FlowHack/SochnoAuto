// Carousel: свайпы на телефоне (touch: true при инициализации)
document.querySelectorAll('.carousel').forEach(function (el) {
  if (typeof bootstrap === 'undefined' || !bootstrap.Carousel) return;
  bootstrap.Carousel.getOrCreateInstance(el, { touch: true });
});