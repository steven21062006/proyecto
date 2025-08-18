// main.js - Animaciones vistosas para BLACK PANTHER

document.addEventListener('DOMContentLoaded', () => {
  // --- Animar títulos principales (h2) con fade + slide desde izquierda ---
  const titles = document.querySelectorAll('main h2');
  titles.forEach((title, i) => {
    title.style.opacity = '0';
    title.style.transform = 'translateX(-50px)';
    title.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
    setTimeout(() => {
      title.style.opacity = '1';
      title.style.transform = 'translateX(0)';
    }, 300 * i);
  });

  // --- Animar contenedores de categorías (.auction-list) con fade + zoom ---
  const categoryLists = document.querySelectorAll('.auction-list');
  categoryLists.forEach((list, i) => {
    list.style.opacity = '0';
    list.style.transform = 'scale(0.85)';
    list.style.transition = 'opacity 0.8s ease-out, transform 0.8s ease-out';
    setTimeout(() => {
      list.style.opacity = '1';
      list.style.transform = 'scale(1)';
    }, 400 * i + 800);
  });

  // --- Animaciones para botones (.btn, .btn-primary) ---
  const buttons = document.querySelectorAll('.btn, .btn-primary');
  buttons.forEach(btn => {
    // Efecto al pasar el mouse (hover)
    btn.style.transition = 'all 0.3s ease';
    btn.addEventListener('mouseenter', () => {
      btn.style.transform = 'scale(1.05)';
      btn.style.boxShadow = '0 8px 15px rgba(0,0,0,0.3)';
      btn.style.backgroundColor = '#b8b8b8ff'; // naranja vibrante
      btn.style.color = '#fff';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = 'none';
      btn.style.backgroundColor = ''; // vuelve a su color original
      btn.style.color = '';
    });
  });

  // --- Parpadeo suave en el botón "Explorar Subastas" ---
  const exploreBtn = document.querySelector('.btn-primary');
  if (exploreBtn) {
    exploreBtn.style.animation = 'pulseGlow 2.5s infinite ease-in-out';
  }

  // --- Hover imágenes productos con zoom y sombra ---
  const productImages = document.querySelectorAll('.auction-item img');
  productImages.forEach(img => {
    img.style.transition = 'transform 0.4s ease, box-shadow 0.4s ease';
    img.parentElement.addEventListener('mouseenter', () => {
      img.style.transform = 'scale(1.12)';
      img.style.boxShadow = '0 8px 20px rgba(0,0,0,0.4)';
    });
    img.parentElement.addEventListener('mouseleave', () => {
      img.style.transform = 'scale(1)';
      img.style.boxShadow = 'none';
    });
  });

  // --- Scroll suave para enlaces del menú que son internas ---
  document.querySelectorAll('nav a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
      e.preventDefault();
      const target = document.querySelector(anchor.getAttribute('href'));
      if (target) target.scrollIntoView({ behavior: 'smooth' });
    });
  });
});



