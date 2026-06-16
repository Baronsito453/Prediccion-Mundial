from flask import Flask, render_template, jsonify
import requests
import time

app = Flask(__name__)

HEADERS = {
    'x-apisports-key': '81b9ca7a3d5f0c9bd24e3e2fa0d89c75',
    'x-rapidapi-host': 'v3.football.api-sports.io'
}

CACHE_IDS = {}
CACHE_STATS = {}

@app.route('/')
def home():
    return render_template('index.html')


def obtener_id_equipo(nombre_equipo):
    if nombre_equipo in CACHE_IDS:
        return CACHE_IDS[nombre_equipo]
        
    url = "https://v3.football.api-sports.io/teams"
    try:
        response = requests.get(url, headers=HEADERS, params={'search': nombre_equipo}, timeout=5)
        if response.status_code == 200:
            resultados = response.json().get("response", [])
            if resultados:
                id_encontrado = resultados[0]["team"]["id"]
                CACHE_IDS[nombre_equipo] = id_encontrado
                return id_encontrado
    except Exception as e:
        print(f"⚠️ Error buscando ID de {nombre_equipo}: {e}")
    return None


def simular_ganador_directo(local, visitante):
    id_l = obtener_id_equipo(local)
    id_v = obtener_id_equipo(visitante)
    
    if not id_l or not id_v:
        return local
        
    url_stats = "https://v3.football.api-sports.io/teams/statistics"
    try:
        if id_l in CACHE_STATS:
            data_l = CACHE_STATS[id_l]
        else:
            res_local = requests.get(url_stats, headers=HEADERS, params={'league': 1, 'season': 2022, 'team': id_l}, timeout=5)
            data_l = res_local.json().get("response", {})
            CACHE_STATS[id_l] = data_l
            time.sleep(0.1)

        if id_v in CACHE_STATS:
            data_v = CACHE_STATS[id_v]
        else:
            res_visitante = requests.get(url_stats, headers=HEADERS, params={'league': 1, 'season': 2022, 'team': id_v}, timeout=5)
            data_v = res_visitante.json().get("response", {})
            CACHE_STATS[id_v] = data_v
            time.sleep(0.1)

        goles_l = data_l.get("goals", {}).get("for", {}).get("average", {}).get("total", "1.5")
        goles_v = data_v.get("goals", {}).get("for", {}).get("average", {}).get("total", "1.2")
        
        g_local = float(goles_l) if goles_l else 1.5
        g_visitante = float(goles_v) if goles_v else 1.2
        
        if g_local >= g_visitante:
            return local
        else:
            return visitante
    except Exception:
        return local


@app.route('/predicciones')
def predicciones():
    try:
        print("🔮 Generando bloques con formato de Equipos para Fase de Grupos...")
        datos_formateados = []
        
        partidos_grupos = [
            {"local": "Netherlands", "visitante": "Senegal", "fase": "GRUPO A"},
            {"local": "England", "visitante": "USA", "fase": "GRUPO B"},
            {"local": "Argentina", "visitante": "Mexico", "fase": "GRUPO C"},
            {"local": "France", "visitante": "Denmark", "fase": "GRUPO D"},
            {"local": "Spain", "visitante": "Germany", "fase": "GRUPO E"},
            {"local": "Belgium", "visitante": "Croatia", "fase": "GRUPO F"},
            {"local": "Brazil", "visitante": "Switzerland", "fase": "GRUPO G"},
            {"local": "Portugal", "visitante": "Uruguay", "fase": "GRUPO H"}
        ]
        
        for partido in partidos_grupos:
            ganador = simular_ganador_directo(partido["local"], partido["visitante"])
            datos_formateados.append({
                "home_team": f"Equipo 1: {partido['local']}",
                "away_team": f"Equipo 2: {partido['visitante']}",
                "competition_name": partido["fase"],
                "prediction": f"Predicción: Gana {ganador}",
                "result": "Fase de Grupos"
            })

        octavos = [
            ("Netherlands", "USA"), ("Argentina", "Denmark"),
            ("France", "Mexico"), ("England", "Senegal"),
            ("Spain", "Croatia"), ("Brazil", "Uruguay"),
            ("Belgium", "Germany"), ("Portugal", "Switzerland")
        ]
        
        ganadores_octavos = []
        for loc, vis in octavos:
            ganador = simular_ganador_directo(loc, vis)
            ganadores_octavos.append(ganador)
            datos_formateados.append({
                "home_team": f"Rival 1: {loc}",
                "away_team": f"Rival 2: {vis}",
                "competition_name": "ELIMINATORIAS - OCTAVOS",
                "prediction": f"Avanza: {ganador}",
                "result": "Eliminatoria"
            })

        cuartos = [
            (ganadores_octavos[0], ganadores_octavos[1]),
            (ganadores_octavos[2], ganadores_octavos[3]),
            (ganadores_octavos[4], ganadores_octavos[5]),
            (ganadores_octavos[6], ganadores_octavos[7])
        ]
        
        ganadores_cuartos = []
        for loc, vis in cuartos:
            ganador = simular_ganador_directo(loc, vis)
            ganadores_cuartos.append(ganador)
            datos_formateados.append({
                "home_team": f"Cruce 1: {loc}",
                "away_team": f"Cruce 2: {vis}",
                "competition_name": "ELIMINATORIAS - CUARTOS",
                "prediction": f"Avanza: {ganador}",
                "result": "Eliminatoria"
            })

        semis = [
            (ganadores_cuartos[0], ganadores_cuartos[1]),
            (ganadores_cuartos[2], ganadores_cuartos[3])
        ]
        
        ganadores_semis = []
        for loc, vis in semis:
            ganador = simular_ganador_directo(loc, vis)
            ganadores_semis.append(ganador)
            datos_formateados.append({
                "home_team": f"Semifinalista 1: {loc}",
                "away_team": f"Semifinalista 2: {vis}",
                "competition_name": "ELIMINATORIAS - SEMIFINAL",
                "prediction": f"Avanza: {ganador}",
                "result": "Eliminatoria"
            })

        final_local = ganadores_semis[0]
        final_visitante = ganadores_semis[1]
        campeon = simular_ganador_directo(final_local, final_visitante)
        
        datos_formateados.append({
            "home_team": final_local,
            "away_team": final_visitante,
            "competition_name": "🏆 GRAN FINAL 🏆",
            "prediction": f"🥇 CAMPEÓN: {campeon} 🥇",
            "result": "FINAL"
        })

        return jsonify({"data": datos_formateados})
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"data": [], "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)