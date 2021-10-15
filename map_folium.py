from os import sep
from typing import Dict
import folium
import csv
import operator
import collections
from folium.folium import Map
from folium.map import Popup,Figure
from folium.plugins import MarkerCluster,Draw, MiniMap


CSS_LOCAL = '''
        <style>
        .styled-table thead tr {
            background-color: #023e97;
            color: #ffffff;
            text-align: left;
        }

        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 500px;
            width:500px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
        }

        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
        }

        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }

        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }

        .styled-table tbody tr:last-of-type {
            border-bottom: 2px solid #023e97;
        }

        .styled-table tbody tr.active-row {
            font-weight: bold;
            color: #023e97;
        }

        .btn {
            border: 0px;
            border-radius: 5px;
            background-color: #025ce3;
            color: white !important;
            padding: 3px !important;
            font-size: 12px !important;
            cursor: pointer;
        }
        /* Green */
        .success {
            border-color: #0d6efd;
            color: white !important;
        }
        .success:hover {
            background-color: #0d6efd;
            color: white;
        }
        </style>
        '''
URL_MAPS = {
    'google':'https://www.google.com.br/maps/search/',
    'bing':'https://www.bing.com/maps?q=',
    'nomi':'https://nominatim.openstreetmap.org/ui/search.html?q=',
    'mapquest': 'https://www.mapquest.com/latlng/'
}

def convert_dict_html(data_dict:dict)->str:
    if data_dict:
        tmp_ = f''' <table class="styled-table">'''
        for key_str, value_str in data_dict.items():
            tmp_ += f'<tr><td><b>{key_str}</b>:</td><td>{value_str}</td></tr>\n'
        return tmp_+'</table>'


def validate_icon(line_data_aiport:str)->dict:
    return {
        'color': "red" if 'Internacional' in line_data_aiport else "black",
        'icon': "crosshairs" if 'Internacional' in line_data_aiport else "plane"
    }

def mount_url_map(url_click:str,text_click:str)->str:
    return f"<a target='_blank' class='btn success' href='{url_click}'>{text_click}</a>"

def add_countrol_Layers(obj_maps:folium):
    fig2=Figure(width=550,height=350)
    fig2.add_child(obj_maps)
    folium.TileLayer('Stamen Terrain').add_to(obj_maps)
    folium.TileLayer('Stamen Toner').add_to(obj_maps)
    folium.TileLayer('Stamen Water Color').add_to(obj_maps)
    folium.TileLayer('cartodbpositron').add_to(obj_maps)
    folium.TileLayer('cartodbdark_matter').add_to(obj_maps)
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',attr='Google',name='Google Maps').add_to(obj_maps)
    folium.LayerControl().add_to(obj_maps)

def maps(enriched_data_aiport: list)->Map:

    obj_maps = folium.Map(
        location=[-9.898478, -51.107451],
        zoom_start=4,
        tiles='openstreetmap',
        overlay=True,
        control=True,
    )

    add_countrol_Layers(obj_maps)


    for line_data_aiport in enriched_data_aiport:
        body_hmtl_str = convert_dict_html(line_data_aiport)
        icon_dict = validate_icon(line_data_aiport.get('airport'))
        lat_ = line_data_aiport.get('lat')
        lon_ = line_data_aiport.get('lon')
        url_maps_bing = mount_url_map(f'{URL_MAPS.get("bing")}{lat_}%2C{lon_}','Bing Maps')
        url_maps_google = mount_url_map(f'{URL_MAPS.get("google")}{lat_},{lon_}','Google Maps')
        url_maps_nominatim = mount_url_map(f'{URL_MAPS.get("nomi")}{lat_}+{lon_}','Nominatim Maps')
        url_maps_mapquest = mount_url_map(f'{URL_MAPS.get("mapquest")}{lat_},{lon_}?zoom=0','MapQuest Maps')

        folium.Marker(
            [lat_, lon_],
            popup=Popup(html=f"<h1 align='center'>{line_data_aiport.get('airport')}</h1> {body_hmtl_str} <br> Open: " +
                        f"{url_maps_bing}, {url_maps_google}, {url_maps_nominatim}, {url_maps_mapquest}", max_width='1500px'),
            tooltip=line_data_aiport.get('airport'),
            icon=folium.Icon(color=icon_dict.get('color'),
                             icon=icon_dict.get('icon'), prefix='fa'),


        ).add_to(obj_maps)
    return obj_maps

# Using as command line
if __name__ == '__main__':
    csv.register_dialect('piper', delimiter=';', quoting=csv.QUOTE_NONE)
    ENRICHED_DATA_AIPORT = 'enriched_data_aiport.csv'
    FILE_SOURCE_LINES = open(ENRICHED_DATA_AIPORT, 'r').readlines()
    FILE_SOURCE_FORMAT_CSV = list(csv.DictReader(FILE_SOURCE_LINES, dialect='piper'))

    MAPS_FOLIUM =  maps(FILE_SOURCE_FORMAT_CSV)

    minimap = MiniMap()
    MAPS_FOLIUM.add_child(minimap)

    draw = Draw(export=True)
    draw.add_to(MAPS_FOLIUM)

    MAPS_FOLIUM.get_root().header.add_child(folium.Element(CSS_LOCAL))
    MAPS_FOLIUM.save("output_map_folium.html")

    exit()
