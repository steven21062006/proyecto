document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('puja-form');
    if (!form) return; // No mostrar JS si no hay formulario

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        formData.append('subasta_id', subastaId);

        fetch(`/api/pujas/${subastaId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                // 1. Actualiza el precio actual
                document.getElementById('current-bid').innerText = `$${data.monto}`;

                // 2. Agrega la nueva puja al inicio de la tabla
                const history = document.getElementById('bid-history');
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${data.usuario}</td>
                    <td>$${data.monto}</td>
                    <td>${data.fecha}</td>
                `;
                history.prepend(newRow);

                form.reset();
                alert('¡Puja realizada con éxito!');
            } else {
                alert(data.error || 'Error al realizar la puja');
            }
        })
        .catch(err => {
            console.error(err);
            alert('Error al procesar la puja');
        });
    });
});
