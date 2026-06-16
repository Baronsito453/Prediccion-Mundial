$(document).ready(function(){

    $("#generar").click(function(){

        $.get("/predicciones", function(data){

            let html = "";

            data.data.forEach(function(partido){

                // Buscamos qué fase es para ponerle su color correspondiente del CSS
                let claseFase = "fase-grupo"; // Por defecto blanco para Grupos

                if (partido.competition_name.includes("FINAL")) {
                    claseFase = "fase-final";       // Amarillo/Dorado para la gran final
                } else if (partido.competition_name.includes("ELIMINATORIAS")) {
                    claseFase = "fase-eliminatoria"; // Gris elegante para Octavos, Cuartos y Semis
                }

                // Armamos la fila inyectándole la clase detectada arriba
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

        });

    });

});
