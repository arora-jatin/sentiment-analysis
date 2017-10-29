from flask import Flask, request
from flask_restful import Resource, Api
from flask.ext.jsonpify import jsonify
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from flask_cors import CORS

cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(authenticator)
bucket = cluster.open_bucket('Data')

app = Flask(__name__)
api = Api(app)
CORS(app)

class SurveyResponsw(Resource):
	def get(self, survey_id):
		rv = bucket.get(survey_id)
		print(rv.value)
		return jsonify(rv.value)

api.add_resource(SurveyResponsw, '/surveyresponse/<survey_id>')

if __name__ == '__main__':
     app.run(host='0.0.0.0')