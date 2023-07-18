#import library
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

#import library flask sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import os

#inisiasi objek
app = Flask(__name__)

#inisiasi objek flask restful
api = Api(app)

#inisiasi objek flask cors
CORS(app)

#inisialisasi objek flask sqlalchemy
db = SQLAlchemy(app)

#mengkonfigurasi dulu database
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

#membuat database model 
class ModelDatabase(db.Model):
    #membuat field/colom
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    umur = db.Column(db.Integer)
    alamat = db.Column(db.TEXT)

    #membuat method untuk menyimpan data 
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False
        
#mengcreate database
db.create_all()

#inisiasi variable kosong bertipe dictionary
identitas = {} 

#membuat class resource
class ContohResource(Resource):
    def get(self):
        #menampilkan data dari database sqlite]
        query = ModelDatabase.query.all()

        #melakuan iterasi pada ModelDatabase
        output = [
            {
                "id":data.id,
                "nama":data.nama,
                "umur":data.umur,
                "alamat":data.alamat
            }
            for data in query
        ]
        response = {
            "code" : 200,
            "msg" : "Query data sukses",
            "data" : output
        }

        return response, 200
    
#membuat class baru untuk mengedit / menghaous data
class UpdateResource(Resource):
    def put(self, id):
        #konsumsi id untuk query di model database nya
        #pilih data data yang ingin diedit berdasarkan id yang dimasukan
        query = ModelDatabase.query.get(id)

        #form untuk mengedit data 
        editNama = request.form["nama"]
        editUmur = request.form["umur"]
        editAlamat = request.form["alamat"]

        #mereplace nilai yang ada disetiap field/kolom
        query.nama = editNama
        query.umur = editUmur
        query.alamat = editAlamat
        db.session.commit()

        response = {
            "msg": "Data berhasil di edit",
            "code": 200
        }

        return response
    
    def post(self):
        dataNama = request.form["nama"]
        dataUmur = request.form["umur"]
        dataAlamat = request.form["alamat"]
        
        #masukan data ke dalam database model 
        model = ModelDatabase(nama=dataNama, umur=dataUmur, alamat=dataAlamat)
        model.save()

        response = {
            "msg" : "Data berhasil di input",
            "code": 200
        }
        return response, 200
    #delete all / hapus semua data
    def delete(self):
        #query all data
        query = ModelDatabase.query.all()
        #looping
        for data in query:
            db.session.delete(data)
            db.session.commit()
        response = {
            "msg": "Semua data berhasil di hapus",
            "code": 200
        }
        return response, 200

    
    #delete by id, bukan delete all
    def delete(self, id):
        queryData = ModelDatabase.query.get(id)

        #panggil method untuk delete data by id
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "msg": "Data berhasil di hapus",
            "code": 200
        }
        return response, 200

#setup resourcenya
api.add_resource(ContohResource, "/api", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateResource, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=1000)