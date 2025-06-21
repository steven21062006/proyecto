// Utiliza localStorage para manejar productos

function getProductos() {
    return JSON.parse(localStorage.getItem("productos")) || [];
}

function guardarProducto(producto) {
    const productos = getProductos();
    productos.push(producto);
    localStorage.setItem("productos", JSON.stringify(productos));
}

function actualizarProducto(index, productoActualizado) {
    const productos = getProductos();
    productos[index] = productoActualizado;
    localStorage.setItem("productos", JSON.stringify(productos));
}

function eliminarProducto(index) {
    const productos = getProductos();
    productos.splice(index, 1);
    localStorage.setItem("productos", JSON.stringify(productos));
}

function mostrarProductos() {
    const productos = getProductos();
    const contenedor = document.getElementById("productGrid");
    contenedor.innerHTML = "";

    if (productos.length === 0) {
        document.getElementById("noProducts").style.display = "block";
        return;
    } else {
        document.getElementById("noProducts").style.display = "none";
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
                <div class="product-detail"><strong>Talla:</strong> ${prod.talla}</div>
                <div class="product-detail"><strong>Color:</strong> ${prod.color}</div>
                <div class="product-detail"><strong>Descripción:</strong> ${prod.descripcion}</div>
            </div>
            <div class="product-price">$${prod.precio}</div>
            <div class="product-stock"><strong>Cantidad:</strong> ${prod.cantidad}</div>
            <div class="product-actions">
                <button class="btn btn-edit" onclick="editarProducto(${index})">Editar</button>
                <button class="btn btn-delete" onclick="eliminarProducto(${index}); mostrarProductos();">Eliminar</button>
            </div>
        `;
        contenedor.appendChild(card);
    });
}

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

    guardarProducto(producto);
    alert("✅ Producto agregado correctamente");
    event.target.reset();
}

document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("productGrid")) {
        mostrarProductos();
    }

    const form = document.getElementById("addProductForm");
    if (form) {
        form.addEventListener("submit", agregarProductoDesdeFormulario);
    }
});
