// Obtener productos desde localStorage o un arreglo vacío si no hay
function getProductos() {
    return JSON.parse(localStorage.getItem("productos")) || [];
}

// Guardar lista de productos en localStorage
function guardarProductos(productos) {
    localStorage.setItem("productos", JSON.stringify(productos));
}

// Mostrar productos en el contenedor de la landing
function mostrarProductos() {
    const productos = getProductos();
    const contenedor = document.getElementById("productGrid");
    const noProducts = document.getElementById("noProducts");

    if (!contenedor) return;

    contenedor.innerHTML = "";

    if (productos.length === 0) {
        if (noProducts) noProducts.style.display = "block";
        return;
    } else {
        if (noProducts) noProducts.style.display = "none";
    }

    productos.forEach((prod, index) => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-header">
                <div>
                    <h2 class="product-title">${prod.nombre}</h2>
                    <div class="product-brand">${prod.marca}</div>
                </div>
                <div class="product-category">${prod.categoria}</div>
            </div>
            <div class="product-details">
                <div class="product-detail"><strong>Talla:</strong> ${prod.talla || '-'}</div>
                <div class="product-detail"><strong>Color:</strong> ${prod.color || '-'}</div>
                <div class="product-detail"><strong>Descripción:</strong> ${prod.descripcion || '-'}</div>
            </div>
            <div class="product-price">$${prod.precio}</div>
            <div class="product-stock"><strong>Cantidad:</strong> ${prod.cantidad}</div>
            <div class="product-actions">
                <button class="btn btn-edit" onclick="editarProducto(${index})">Editar</button>
                <button class="btn btn-delete" onclick="eliminarProducto(${index})">Eliminar</button>
            </div>
        `;
        contenedor.appendChild(card);
    });
}

// Agregar producto desde formulario
function agregarProductoDesdeFormulario(event) {
    event.preventDefault();
    const producto = {
        nombre: document.getElementById("productName").value,
        categoria: document.getElementById("productCategory").value,
        marca: document.getElementById("productBrand").value,
        talla: document.getElementById("productSize").value,
        color: document.getElementById("productColor").value,
        precio: parseFloat(document.getElementById("productPrice").value).toFixed(2),
        cantidad: parseInt(document.getElementById("productQuantity").value),
        descripcion: document.getElementById("productDescription").value
    };

    const productos = getProductos();
    productos.push(producto);
    guardarProductos(productos);

    alert("✅ Producto agregado correctamente");
    event.target.reset();

    mostrarProductos();
    actualizarEstadisticas();
}

// Eliminar producto
function eliminarProducto(index) {
    if (!confirm("¿Seguro que quieres eliminar este producto?")) return;

    const productos = getProductos();
    productos.splice(index, 1);
    guardarProductos(productos);

    mostrarProductos();
    actualizarEstadisticas();
}

// Mostrar formulario de edición
function editarProducto(index) {
    const productos = getProductos();
    const producto = productos[index];
    if (!producto) return alert("Producto no encontrado");

    document.getElementById('productId').value = index;
    document.getElementById('editProductName').value = producto.nombre;
    document.getElementById('editProductCategory').value = producto.categoria;
    document.getElementById('editProductBrand').value = producto.marca;
    document.getElementById('editProductSize').value = producto.talla;
    document.getElementById('editProductColor').value = producto.color;
    document.getElementById('editProductPrice').value = producto.precio;
    document.getElementById('editProductQuantity').value = producto.cantidad;
    document.getElementById('editProductDescription').value = producto.descripcion;

    document.getElementById('editFormContainer').style.display = 'block';
}

// Cancelar edición
function cancelarEdicion() {
    const formContainer = document.getElementById('editFormContainer');
    if (formContainer) formContainer.style.display = 'none';
}

// Actualizar producto
function actualizarProducto(event) {
    event.preventDefault();
    const index = document.getElementById('productId').value;
    const productos = getProductos();

    productos[index] = {
        nombre: document.getElementById('editProductName').value,
        categoria: document.getElementById('editProductCategory').value,
        marca: document.getElementById('editProductBrand').value,
        talla: document.getElementById('editProductSize').value,
        color: document.getElementById('editProductColor').value,
        precio: parseFloat(document.getElementById('editProductPrice').value).toFixed(2),
        cantidad: parseInt(document.getElementById('editProductQuantity').value),
        descripcion: document.getElementById('editProductDescription').value
    };

    guardarProductos(productos);
    alert("✅ Producto actualizado");
    cancelarEdicion();
    mostrarProductos();
    actualizarEstadisticas();
}

// Estadísticas
function actualizarEstadisticas() {
    const productos = getProductos();

    const total = productos.length;
    const bajoStock = productos.filter(p => p.cantidad < 5).length;
    const valorTotal = productos.reduce((acc, p) => acc + (parseFloat(p.precio) * p.cantidad), 0);

    if (document.getElementById("totalProducts")) {
        document.getElementById("totalProducts").textContent = total;
    }
    if (document.getElementById("lowStockItems")) {
        document.getElementById("lowStockItems").textContent = bajoStock;
    }
    if (document.getElementById("totalValue")) {
        document.getElementById("totalValue").textContent = `$${valorTotal.toFixed(2)}`;
    }
}

// Buscar productos por nombre
function buscarProductos() {
    const query = document.getElementById("searchInput").value.toLowerCase();
    const productos = getProductos().filter(p =>
        p.nombre.toLowerCase().includes(query)
    );

    renderizarBusqueda(productos);
    actualizarEstadisticas();
}

// Filtrar productos por categoría
function filtrarProductos() {
    const filtro = document.getElementById("categoryFilter").value;
    const productos = getProductos();

    const filtrados = filtro ? productos.filter(p => p.categoria === filtro) : productos;
    renderizarBusqueda(filtrados);
    actualizarEstadisticas();
}

// Renderizar resultado filtrado/buscado
function renderizarBusqueda(productos) {
    const contenedor = document.getElementById("productGrid");
    const noProducts = document.getElementById("noProducts");

    if (!contenedor) return;
    contenedor.innerHTML = "";

    if (productos.length === 0) {
        if (noProducts) noProducts.style.display = "block";
        return;
    } else {
        if (noProducts) noProducts.style.display = "none";
    }

    productos.forEach((prod, index) => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.innerHTML = `
            <div class="product-header">
                <div>
                    <h2 class="product-title">${prod.nombre}</h2>
                    <div class="product-brand">${prod.marca}</div>
                </div>
                <div class="product-category">${prod.categoria}</div>
            </div>
            <div class="product-details">
                <div class="product-detail"><strong>Talla:</strong> ${prod.talla || '-'}</div>
                <div class="product-detail"><strong>Color:</strong> ${prod.color || '-'}</div>
                <div class="product-detail"><strong>Descripción:</strong> ${prod.descripcion || '-'}</div>
            </div>
            <div class="product-price">$${prod.precio}</div>
            <div class="product-stock"><strong>Cantidad:</strong> ${prod.cantidad}</div>
            <div class="product-actions">
                <button class="btn btn-edit" onclick="editarProducto(${index})">Editar</button>
                <button class="btn btn-delete" onclick="eliminarProducto(${index})">Eliminar</button>
            </div>
        `;
        contenedor.appendChild(card);
    });
}

// Inicialización
document.addEventListener("DOMContentLoaded", () => {
    mostrarProductos();
    actualizarEstadisticas();

    const formAgregar = document.getElementById("addProductForm");
    if (formAgregar) {
        formAgregar.addEventListener("submit", agregarProductoDesdeFormulario);
    }

    const formEditar = document.getElementById("editProductForm");
    if (formEditar) {
        formEditar.addEventListener("submit", actualizarProducto);
    }
});
