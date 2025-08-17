document.addEventListener('DOMContentLoaded', function() {
  const userAvatar = document.querySelector('.user-avatar');
  const dropdown = document.getElementById('user-dropdown');

  if (userAvatar && dropdown) {
    // Alternar menú al hacer clic en el avatar
    userAvatar.addEventListener('click', function(event) {
      event.stopPropagation(); // Evita que el clic llegue al documento
      dropdown.classList.toggle('show');
    });

    // Cerrar menú al hacer clic en cualquier parte del documento
    document.addEventListener('click', function() {
      if (dropdown.classList.contains('show')) {
        dropdown.classList.remove('show');
      }
    });

    // Prevenir que el menú se cierre al hacer clic dentro de él
    dropdown.addEventListener('click', function(event) {
      event.stopPropagation();
    });
  }
});