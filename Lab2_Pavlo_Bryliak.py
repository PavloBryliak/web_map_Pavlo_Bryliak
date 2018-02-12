import folium
from geopy.geocoders import ArcGIS
from geopy.geocoders import Nominatim


def file_num():
    """
    Function for opening a txt file that returns list information
    about film (year, place of filming)
    """
    lst = list()
    number = int(input("Please, enter a number of films! "))
    file = open("locations.list", "r")
    n = 0
    for line in file:
        if n >= 15:
            lst.append(' '.join(line.split()).split(" "))
        n += 1
        if n == number:
            file.close()
            return lst


def countries_all():
    """
    Function that returns list of countries
    """
    file = open("countries.txt", "r")
    lst = list()
    for country in file:
        lst.append(" ".join(country.split()).split(" "))
    file.close()
    return lst


def new_dictionary():
    """
    Function for generating a dictionary with key (year) and values (countries)
    """
    years = {str(i) for i in range(1888, 2018)}
    future_dict = file_num()
    countries = countries_all()
    set1 = set()
    for i in countries:
        set1.add(str(" ".join(i)))
    dict1 = dict()
    for element in future_dict:
        values = set()
        for j in element:
            if j in set1:
                values.add(j)
            if len(j) == 6:
                if str(j[1] + j[2] + j[3] + j[4]) in years:
                    key = str(j[1] + j[2] + j[3] + j[4])
        if key in dict1:
            dict1[key].update(values)
        else:
            dict1[key] = values
    return dict1


geolocator = ArcGIS()


def mapr():
    """
    Function that creates layers using information from txt files and add these layers to the map
    """
    mae = folium.Map()
    geolocator = Nominatim()
    dict1 = new_dictionary()
    year = input("Choose an year: ")
    places = dict1[year]
    print(places)
    for i in places:
        location = geolocator.geocode(i, timeout=30)
        mae.add_child(folium.Marker(location=[location.latitude, location.longitude], icon=folium.Icon()))

    d = folium.FeatureGroup(name="Population")
    d.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                               style_function=lambda i: {
                                   'fillColor': 'green' if i['properties']['POP2005'] <= 10000000
                                   else 'orange' if 10000000 < i['properties']['POP2005'] < 20000000
                                   else 'red'}))

    m = folium.FeatureGroup(name="NATO countries")
    n = folium.FeatureGroup(name="G7 countries")

    file = open("countries.txt", "r")
    file_ = open("G7.txt", "r")
    file_1 = open("NATO.txt", "r")

    for l in file:
        location = geolocator.geocode(l, timeout=30)
        if l in file_:
            n.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                      icon=folium.Icon(color='red', icon_color='green')))
        if l in file_1:
            m.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                      icon=folium.Icon(color='violet', icon_color='yellow')))

    file_1.close()
    file_.close()
    file.close()
    mae.add_child(n)
    mae.add_child(m)
    mae.add_child(folium.TileLayer(tiles='Stamen Terrain'))
    mae.add_child(folium.TileLayer(tiles='Stamen Toner'))
    mae.add_child(d)
    mae.add_child(folium.LayerControl())
    mae.save("map.html")


mapr()
