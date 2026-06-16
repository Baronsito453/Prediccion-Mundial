$(document).ready(function(){

    $("#generar").click(function(){

        $.get("/predicciones", function(data){

            let html = "";

            data.data.forEach(function(partido){

                html += `
                <tr>
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