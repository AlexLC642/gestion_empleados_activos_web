document.addEventListener('DOMContentLoaded', function () {
  const formularios = document.querySelectorAll('form');

  formularios.forEach(form => {
    form.addEventListener('submit', function (e) {
      const telefono = form.querySelector('input[name="telefono"]');
      const monto = form.querySelector('input[name="monto"]');

      if (telefono && !/^\d{8}$/.test(telefono.value)) {
        alert("El teléfono debe tener exactamente 8 dígitos.");
        e.preventDefault();
        return;
      }

      if (monto && parseFloat(monto.value) <= 0) {
        alert("El monto debe ser mayor a cero.");
        e.preventDefault();
        return;
      }
    });
  });

  // Confirmaciones para eliminar
  const eliminarLinks = document.querySelectorAll('a[onclick*="confirm"]');
  eliminarLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      if (!confirm("¿Estás seguro de eliminar este elemento?")) {
        e.preventDefault();
      }
    });
  });
});
