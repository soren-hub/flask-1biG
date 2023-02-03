from flask import Flask, jsonify
from data import data_elements
from pyproj import CRS
from pyproj import Transformer
import pandas as pd

app = Flask(__name__) #servidor

@app.route('/data_antigua', methods = ['GET'])
def getData():
    return jsonify({"ELEMENTOS (SIN CAMBIO DE UNIDADES) DE LA DATA": data_elements, "message": "estos son los datos"})

@app.route('/data_antigua/<string:data_name>')
def getProduct(data_name):
    dataelementsFound = [data_element for data_element in data_elements if data_element['name'] == data_name]
    if (len(dataelementsFound) > 0):
        return jsonify({"TUS COORDENADAS SIN CAMBIO DE UNIDADES SON": dataelementsFound[0]})
    return jsonify({"message": "data not found"})

#FUNCIÓN TRANSFORMADORA DE UNIDADES:

from_crs = CRS.from_proj4("+proj=utm +zone=19 +south +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
to_crs = CRS.from_epsg(4326)
proj = Transformer.from_crs(from_crs, to_crs, always_xy=True)
def convert_coordinates():
    result = []
    for element in data_elements:
        posx = element['coord'][0]
        posy = element['coord'][1]
        transformed_coord = proj.transform(float(posx),float(posy))
        result.append(transformed_coord)
    return result
convert_coordinates()

def create_data_elements_dict(converted_coordinates):
    result = []
    for index, coord in enumerate(converted_coordinates):
        element = {
            "name": "inv" + str(index + 1),
            "coord": [str(coord[0]), str(coord[1])]
        }
        result.append(element)
    return result

converted_coordinates = convert_coordinates()
data_elements_dict = create_data_elements_dict(converted_coordinates)

#COORDENADAS NUEVAS:
@app.route('/data_nueva')
def getCoordinates():
    return jsonify({"LISTA DE ELEMENTOS CON LAS UNIDADES NUEVAS": data_elements_dict})

@app.route('/data_nueva/<string:data_name>')
def getProduct_2(data_name):
    dataelementsFound_2 = [data_element for data_element in data_elements_dict if data_element['name'] == data_name]
    if (len(dataelementsFound_2) > 0):
        return jsonify({"LAS COORDENADAS NUEVAS QUE CORRESPONDEN AQUI SON": dataelementsFound_2[0]})
    return jsonify({"message": "data not found"})

if __name__ == '__main__':
    app.run(debug=True, port=4000)
