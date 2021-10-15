from os import sep
from nominatim import Nominatim
from geopy.geocoders import Nominatim
import folium
import csv
import json
import pandas as pd


def get_details(lat_str: str, lon_str: str):
    try:
        geolocator = Nominatim(user_agent="MrCl0wnLab")
        location = geolocator.reverse(f"{lat_str}, {lon_str}").raw
        if location:
            return location
    except:
        return str()


def data_enrichment(source_csv_list: list):
    for csv_line in source_csv_list:
        try:
            if csv_line.get('lat') and csv_line.get('lon'):
                ret_ = get_details(csv_line.get('lat'), csv_line.get('lon'))
                # MERG CSV
                csv_merg = dict(csv_line, **ret_.get('address'))
                # PANDA CONVERT JSON TO CSV
                csv_str = pd.json_normalize(csv_merg)
                print(csv_str)

                csv_str.to_csv(ENRICHED_DATA_AIPORT,mode='a',sep=';', index=False, encoding='utf-8',header=False)
        except:
            pass


# Using as command line
if __name__ == '__main__':
    DATA_AIRPORT = 'data_airport.csv'
    ENRICHED_DATA_AIPORT = 'enriched_data_aiport_especial.csv'

    FILE_SOURCE_LINES = open(DATA_AIRPORT, 'r').readlines()
    FILE_SOURCE_FORMAT_CSV = list(csv.DictReader(FILE_SOURCE_LINES))

    data_enrichment(FILE_SOURCE_FORMAT_CSV)

    exit()

    """
    {
        'place_id': 61698631, 
        'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. https: //osm.org/copyright', 
        'osm_type': 'node', 
        'osm_id': 5534337024, 'lat': '-31.3242105', 'lon': '-64.2100051', 
        'display_name': '36, Avenida La Voz del Interior, Córdoba, Municipio de Córdoba, Pedanía Capital, Departamento Capital, Córdoba, X5000, Argentina', 
        'address': {'aeroway': '36', 
        'road': 'Avenida La Voz del Interior', 
        'city': 'Córdoba',
        'municipality': 'Municipio de Córdoba', 
        'county': 'Pedanía Capital', 
        'state_district': 'Departamento Capital', 
        'state': 'Córdoba', 
        'postcode': 'X5000', 
        'country': 'Argentina', 
        'country_code': 'ar'}, 
        'boundingbox': ['-31.3242605', '-31.3241605', '-64.2100551', '-64.2099551']
    }
    """
