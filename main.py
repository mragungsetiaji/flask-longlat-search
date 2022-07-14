from flask import Flask, jsonify, request
from sklearn.neighbors import KDTree
import numpy as np

app = Flask(__name__)

class Data:

    def __init__(self):
        self.data = dict()
        self.tree = None

    def add_data(self, index: int, longitude: float, latitude: float):
        self.data[index] = [longitude, latitude]

    def reset(self):
        self.data = dict()
        self.tree = None

    def train(self):
        # convert self.data to numpy array
        data = np.array(list(self.data.values()))
        # create KDTree
        self.tree = KDTree(data, metric='euclidean')

    def get_neighbors(self, longitude: float, latitude: float, k: int):
        # convert longitude and latitude to numpy array
        point = np.array([longitude, latitude])
        # get k nearest neighbors
        distance, index = self.tree.query([point], k=k)
        # convert neighbort into dict with index and distance
        query = list()
        for i in range(0, len(distance[0])):
          x = {'index':int(index[0][i]), 'distance':float(distance[0][i])}
          query.append(x)
        return query

data = Data()

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok'})

@app.route('/add', methods=['POST'])
def add_data():
    # extract longitude and latitude from request
    longitude = request.json.get('longitude')
    latitude = request.json.get('latitude')
    # extract index from request
    index = request.json.get('index')
    # add data to data
    data.add_data(int(index), float(longitude), float(latitude))
    # retrain
    data.train()
    # return success message
    return jsonify({'success': True})

@app.route('/train', methods=['POST'])
def train():
    # retrain
    data.train()
    # return success message
    return jsonify({'success': True})

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data.data)

@app.route('/query', methods=['GET'])
def query():
    # extract longitude and latitude from request
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    # extract k from request
    k = request.args.get('k')
    # get neighbors
    neighbors = data.get_neighbors(float(longitude), float(latitude), int(k))
    # return neighbors
    return jsonify({'neighbors': neighbors})

if __name__ == '__main__':
    app.run(debug=True)
    

