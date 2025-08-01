// Función para confirmar eliminación
function confirmarEliminacion(id) {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
        window.location.href = `/tienda/eliminar/${id}/`;
    }
}

// Función para mostrar/ocultar formulario de edición
function toggleEdicion(id = null) {
    const form = document.getElementById('editForm');
    if (id) {
        // Rellenar formulario con datos del producto
        const producto = document.querySelector(`.producto[data-id="${id}"]`);
        if (producto) {
            form.querySelector('[name="nombre"]').value = producto.dataset.nombre;
            form.querySelector('[name="precio"]').value = producto.dataset.precio;
            form.querySelector('[name="cantidad"]').value = producto.dataset.cantidad;
            form.querySelector('[name="id"]').value = id;
            form.style.display = 'block';
        }
    } else {
        form.style.display = 'none';
    }
}

// Event listeners básicos
document.addEventListener('DOMContentLoaded', function() {
    // Botones de eliminar
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function() {
            confirmarEliminacion(this.dataset.id);
        });
    });

    // Botones de editar
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', function() {
            toggleEdicion(this.dataset.id);
        });
    });

    // Cancelar edición
    document.getElementById('cancelEdit').addEventListener('click', function() {
        toggleEdicion();
    });
});