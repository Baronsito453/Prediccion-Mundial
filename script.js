$(document).ready(function(){

    $("#generar").click(function(){

        // TRUCO VISUAL: Cambiamos el texto del botón y lo congelamos para avisar que está jalando la API
        const boton = $("#generar");
        boton.prop("disabled", true).text("⏳ Simulando Mundial... Espera por favor");

        $.get("/predicciones", function(data){

            let html = "";

            data.data.forEach(function(partido){

                let claseFase = "fase-grupo"; 

                if (partido.competition_name.includes("FINAL")) {
                    claseFase = "fase-final";       
                } else if (partido.competition_name.includes("ELIMINATORIAS")) {
                    claseFase = "fase-eliminatoria"; 
                }

                html += `
                <tr class="${claseFase}">
                    <td>${partido.home_team}</td>
                    <td>${partido.away_team}</td>
                    <td>${partido.competition_name}</td>
                    <td>${partido.prediction}</td>
                    <td>${partido.result}</td>
                </tr>
                `;
            });

            $("#resultado").html(html);

            // Regresamos el botón a su estado normal cuando acabe
            boton.prop("disabled", false).text("Cargar Predicciones");

        }).fail(function(xhr, status, error) {
            // Si la API truena o da error, avisamos aquí y reactivamos el botón
            console.error("Error en la petición:", error);
            alert("⚠️ Hubo un detalle al conectar con la API o se agotaron los créditos. Revisa los logs.");
            boton.prop("disabled", false).text("Cargar Predicciones");
        });

    });

});
