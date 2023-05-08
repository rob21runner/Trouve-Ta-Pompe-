import folium
from folium.plugins import MarkerCluster
import requests
import branca
import numpy as np
import pandas as pd
from geopy.geocoders import Nominatim


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location(texte):
    print(f"{texte}  {type(texte)}")
    geolocator = Nominatim(user_agent="trouvetapompe")
    try:
        location = geolocator.geocode(texte)
        latitude = location.latitude
        longitude = location.longitude

        location_data = {'latitude': latitude, 'longitude': longitude}
    except:
        location_data = {'latitude': None, 'longitude': None}
    if not location_data['latitude'] or not location_data['longitude']:
        ip_address = get_ip()
        response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
        location_data = {
            "latitude": response.get("latitude"),
            "longitude": response.get("longitude")
        }

    return location_data



def clean_data(values):
    dt = pd.DataFrame()
    j = 0
    for i in values['records']:
        data = i['fields']
        # print(data)
        if 'carburants_disponibles' in data:
            if not 'sp98_prix' in data:
                sp98 = str(np.nan)
                sp98_maj = str(np.nan)
            else:
                sp98 = float(data['sp98_prix'])
                sp98_maj = data['sp98_maj']
            if not 'sp95_prix' in data:
                sp95 = str(np.nan)
                sp95_maj = str(np.nan)
            else:
                sp95 = float(data['sp95_prix'])
                sp95_maj = data['sp95_maj']
            if not 'e10_prix' in data:
                e10 = str(np.nan)
                e10_maj = str(np.nan)
            else:
                e10 = float(data['e10_prix'])
                e10_maj = data['e10_maj']
            if not 'e85_prix' in data:
                e85 = str(np.nan)
                e85_maj = str(np.nan)
            else:
                e85 = float(data['e85_prix'])
                e85_maj = data['e85_maj']
            if not 'gazole_prix' in data:
                gazole = str(np.nan)
                gazole_maj = str(np.nan)
            else:
                gazole = float(data['gazole_prix'])
                gazole_maj = data['gazole_maj']
            if not 'gplc' in data:
                gplc = str(np.nan)
                gplc_maj = str(np.nan)
            else:
                gplc = float(data['gplc_prix'])
                gplc_maj = data['gplc_maj']
            if not 'region' in data:
                region = np.nan
            else:
                region = data['region']
            if not 'departement' in data:
                departement = np.nan
            else:
                departement = data['departement']
            if not 'cp' in data:
                cp = np.nan
            else:
                cp = data['cp']
            if not 'ville' in data:
                ville = np.nan
            else:
                ville = data['ville']
            if not 'adresse' in data:
                adresse = np.nan
            else:
                adresse = data['adresse']
            proper_data = {
                "Id": data['id'],
                "Region": region,
                "Departement": departement,
                "Code": cp,
                "Ville": ville,
                "Adresse": adresse,
                "Lat": data['latitude'],
                "Long": data['longitude'],
                "Distance": data['dist'],
                "24/24": data['horaires_automate_24_24'],
                "Disponible": data['carburants_disponibles'],
                "SP98_prix": sp98,
                "SP98_maj": sp98_maj,
                "SP95_prix": sp95,
                "SP95_maj": sp95_maj,
                "E10_prix": e10,
                "E10_maj": e10_maj,
                "E85_prix": e85,
                "E85_maj": e85_maj,
                "Gazole_prix": gazole,
                "Gazole_maj": gazole_maj,
                "GPLc_prix": gplc,
                "GPLc_maj": gplc_maj
            }
            dt = pd.concat([dt, pd.DataFrame(proper_data, index=[j])])
            j += 1
    return dt


def make_popup(adress, distance, maj, sp98, sp95, e10, e85, gazole, gplc):
    html = """<!DOCTYPE html>
    <html>
    <style>
        body {
            margin: 0
        }
        
        .rect {
            font-family: 'Inter', sans-serif;
            font-style: normal;
            line-height: 20px;
            width: 450px;
            border-radius: 20px;
        }
        
        .title.first {
            margin-top: 0;
        }

        .title {
            font-weight: 700;
            font-size: 20px;
            line-height: 20px;
            text-align: center;
            color: #353B48;
            margin-top: 10px;
        }

        .main {
            font-weight: 400;
            font-size: 14px;
            text-align: center;
            color: #353B48;
            margin-top: 7px;
        }

        .prices {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }

        .price {
            font-weight: 400;
            font-size: 14px;
            text-align: center;
            color: #353B48;
            margin: 7px 15px 0;
        }
    </style>
    <body>
        <div class="rect">
            <div class="cat">
                <div class="title first">Infos</div>
                <div class="main">""" + adress + """<br>""" + distance + """km</div>
            </div>
            <div class="cat">
                <div class="title">Prix</div>
                <div class="main">Dernière Mise à Jour : """ + maj + """</div>
                <div class="prices">
                """
    if sp98 != "None":
        html = html + """<div class="price">SP98 : """ + sp98 + """ €</div>"""
    if sp95 != "None":
        html = html + """<div class="price">SP95 : """ + sp95 + """ €</div>"""
    if gazole != "None":
        html = html + """<div class="price">Gazole : """ + gazole + """ €</div>"""
    if e10 != "None":
        html = html + """<div class="price">E10 : """ + e10 + """ €</div>"""
    if e85 != "None":
        html = html + """<div class="price">E85 : """ + e85 + """ €</div>"""
    if gplc != "None":
        html = html + """<div class="price">GPLc : """ + gplc + """ €</div>"""
    html = html + """
                </div>
            </div>
            <div class="cat">
                <div class="title" style="margin-bottom: 10px">Fréquentation : Elevée</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def add_pump(dt, m):

    gazole_min = dt.loc[dt["Gazole_prix"] != "nan", "Gazole_prix"].min()
    sp98_min = dt.loc[dt["SP98_prix"] != "nan", "SP98_prix"].min()
    e10_min = dt.loc[dt["E10_prix"] != "nan", "E10_prix"].min()
    marker_cluster = MarkerCluster().add_to(m)
    for i in dt.index:
        color = "green"
        val = dt.iloc[i]
        lat = float(val['Lat']) / 10 ** 5
        long = float(val['Long']) / 10 ** 5
        fuel = ""
        if val['SP95_prix'] != "nan":
            sp95 = val['SP95_prix']
            maj = val['SP95_maj']
        else:
            sp95 = None
        if val['SP98_prix'] != "nan":
            sp98 = val['SP98_prix']
            maj = val['SP98_maj']
            if sp98 == sp98_min:
                color = "red"
        else:
            sp98 = None
        if val['E10_prix'] != "nan":
            e10 = val['E10_prix']
            maj = val['E10_maj']
            if e10 == e10_min:
                color = "blue"
        else:
            e10 = None
        if val['E85_prix'] != "nan":
            e85 = val['E85_prix']
            maj = val['E85_maj']
        else:
            e85 = None
        if val['Gazole_prix'] != "nan":
            gazole = val['Gazole_prix']
            maj = val['Gazole_maj']
            if gazole == gazole_min:
                color = "lightgray"
        else:
            gazole = None
        if val['GPLc_prix'] != "nan":
            gplc = val['GPLc_prix']
            maj = val['GPLc_maj']
        else:
            gplc = None
        adresse = f"{val['Adresse']}, {val['Code']} {val['Ville']}"
        html = make_popup(adresse, str(float(int(float(val['Distance'])))/1000), maj, str(sp98), str(sp95), str(e10), str(e85),
                          str(gazole), str(gplc))
        iframe = branca.element.IFrame(html=html, width=450, height=230)
        popup = folium.Popup(iframe, parse_html=True)

        marker = folium.Marker(
            location=[lat, long],
            popup=popup,
            icon=folium.Icon(color=color, icon="car", prefix="fa"),
            color=color
        )
        if color == "green":
            marker_cluster.add_child(marker)
        else:
            marker.add_to(m)
    return m


def create_map():
    adress = input("Entrez votre adresse : ")
    loc_data = get_location(adress)
    m = folium.Map(location=[loc_data["latitude"], loc_data["longitude"]])

    values = requests.get(
        f"https://data.economie.gouv.fr/api/records/1.0/search/?dataset=prix-des-carburants-en-france-flux-instantane-v2&q=&rows=1000&geofilter.distance={loc_data['latitude']}%2C+{loc_data['longitude']}%2C+35000").json()

    dt = clean_data(values)

    add_pump(dt, m)
    MarkerCluster(name="Cluster").add_to(m)
    m.save("index.html")
