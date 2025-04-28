import folium
import csv
from folium.plugins import MarkerCluster
from branca.element import Template, MacroElement

# -----------------------------
# 1. Créer la carte de base
# -----------------------------
carte = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles='CartoDB dark_matter',
    control_scale=True
)

# -----------------------------
# 2. Ajouter un cluster
# -----------------------------
cluster = MarkerCluster().add_to(carte)

# -----------------------------
# 3. Charger les données des aéroports
# -----------------------------
with open("airports.dat", encoding="utf-8") as fichier:
    lecteur = csv.reader(fichier)
    for ligne in lecteur:
        try:
            nom = ligne[1]
            ville = ligne[2]
            pays = ligne[3]
            latitude = float(ligne[6])
            longitude = float(ligne[7])

            # Créer un popup stylisé
            popup_html = f"""
            <div style='font-family: Arial; font-size: 13px; color: #333;'>
              <h4 style='margin-bottom:5px;'>✈️ {nom}</h4>
              <b>🏙️ Ville :</b> {ville}<br>
              <b>🌍 Pays :</b> {pays}
            </div>
            """

            folium.CircleMarker(
                location=[latitude, longitude],
                radius=3,
                popup=folium.Popup(popup_html, max_width=300),
                color='tomato',
                fill=True,
                fill_opacity=0.8
            ).add_to(cluster)

        except Exception:
            continue

# -----------------------------
# 4. Ajouter un titre personnalisé sur la carte
# -----------------------------
titre_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed; 
    top: 20px; left: 50px; width: 400px; height: auto; 
    z-index:9999;
    background-color: rgba(255, 255, 255, 0.85);
    padding: 15px;
    border-radius: 10px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
    font-family: Arial, sans-serif;
">
    <h3 style="margin: 0; font-size: 18px;">🌐 Carte mondiale des aéroports</h3>
    <p style="font-size: 14px;">
        Cette carte interactive présente plus de 7 000 aéroports dans le monde.<br>
        Elle illustre la répartition des infrastructures aériennes et les pôles majeurs de la mondialisation.
    </p>
</div>
{% endmacro %}
"""

titre = MacroElement()
titre._template = Template(titre_html)
carte.get_root().add_child(titre)

# -----------------------------
# 5. Ajouter une mini-légende
# -----------------------------
legende_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed; 
    bottom: 30px; left: 50px; width: 180px; height: auto; 
    z-index:9998;
    background-color: rgba(0, 0, 0, 0.7);
    padding: 10px;
    border-radius: 8px;
    color: white;
    font-size: 13px;
    font-family: Arial, sans-serif;
">
    <b>Légende :</b><br>
    🔴 Aéroport<br>
    🧭 Zoom / déplacement<br>
    🖱️ Cliquez pour les infos<br>
</div>
{% endmacro %}
"""

legende = MacroElement()
legende._template = Template(legende_html)
carte.get_root().add_child(legende)

# -----------------------------
# 6. Enregistrer la carte
# -----------------------------
carte.save("carte_aeroports_stylée.html")
print("✅ Carte générée avec succès ! Ouvre 'carte_aeroports_stylée.html' dans ton navigateur.")