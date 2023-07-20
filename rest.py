#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

#inisialisasi objek
app = Flask(__name__)
api = Api(app)
CORS(app)

#inisialisasi variabel kosong bertipe dictionary
identitas = {}

#membuat class resource
class ContohResource(Resource):
    def get(self):
       # response = {"msg": "Hallo dunia ini restful pertamaku"}
        return identitas
    
    def post(self):
        nama = request.form["nama"]
        umur = request.form["umur"]
        alamat = request.form["alamat"]
        identitas["nama"] = nama
        identitas["umur"] = umur
        identitas["alamat"] = alamat
        respose = {"msg": "Data berhasil dimasukan"}
        return respose
    
#setup resource nya
api.add_resource(ContohResource, "/api", methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, port=5005)