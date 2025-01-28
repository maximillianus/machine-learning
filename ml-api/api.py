import pickle

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
import numpy as np

app = Flask(__name__)
api = Api(app)

clf = pickle.load(open('./notebook/iris_clf.pkl', 'rb'))

class HelloWorld(Resource):
    def get(self):
        return 'Welcome to Fraud Detection Service v0'

class HealthCheck(Resource):
    def get(self):
        try:
            return {'health': 'OK'}, 200
        except Exception as e:
            print(e)
            return {'health': 'NOT OK'}, 500

class Multi(Resource):
    def get(self, num):
        return {'result': num * 5}

class Classify(Resource):
    def get(self):
        return '\"Classify\" endpoint'

    def post(self):
        data = request.get_json()
        input_data = [data['sl'], data['sw'], data['pl'], data['pw']]
        input_data = np.array([input_data])
        print('data:', input_data)
        print('data type:', type(input_data) )
        print('Prediction:', clf.predict(input_data))
        return {'prediction': clf.predict(input_data).tolist()[0]}

# Endpoint
api.add_resource(HelloWorld, '/')
api.add_resource(HealthCheck, '/health')
api.add_resource(Multi, '/multi/<int:num>')
api.add_resource(Classify, '/classify')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
