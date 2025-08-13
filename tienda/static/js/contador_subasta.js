function iniciarContador(fechaInicioStr, fechaFinStr) {
    const fechaInicio = new Date(fechaInicioStr).getTime();
    const fechaFin = new Date(fechaFinStr).getTime();
    const barra = document.getElementById("barraTiempo");
    const textoTiempo = document.getElementById("tiempoRestante");

    function actualizar() {
        const ahora = new Date().getTime();
        const restante = fechaFin - ahora;

        if (restante <= 0) {
            textoTiempo.innerText = "Subasta finalizada";
            barra.style.width = "0%";
            clearInterval(intervalo);
            return;
        }

        const dias = Math.floor(restante / (1000 * 60 * 60 * 24));
        const horas = Math.floor((restante % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutos = Math.floor((restante % (1000 * 60 * 60)) / (1000 * 60));
        const segundos = Math.floor((restante % (1000 * 60)) / 1000);

        textoTiempo.innerText = `${dias}d ${horas}h ${minutos}m ${segundos}s`;

        // Calcular porcentaje de tiempo restante
        const total = fechaFin - fechaInicio;
        const pasado = ahora - fechaInicio;
        const porcentaje = Math.max(0, 100 - (pasado / total) * 100);
        barra.style.width = porcentaje + "%";
    }

    actualizar();
    const intervalo = setInterval(actualizar, 1000);
}
