from flask import Flask,render_template, request,session
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__) 

uri= 'postgresql://postgres:postgres@localhost:5432/exercicio'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)


class Departamento(db.Model):
    __tablename__ = 'departamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    #data_atualizacao = db.Column(db.DateTime, unique=True,default=db.func.now())

    def salvar(self, d):
        verifica=hasattr(d, 'id')
        if (verifica):
            db.session.merge(d)
        else:
            db.session.add(d)
            db.session.commit()


@app.route('/d/salvar',methods=["POST","GET"])
def depto_inserir():
    if request.method == "POST":
        d = Departamento()
        d.nome = request.form['nome']
        cod=request.form["id"]
        if (cod):
            print("tem id")
            d.id=int(cod)

        d1=d
        d.salvar(d1)
        return render_template('inserirDepartamento.html')

    return render_template('inserirDepartamento.html')


@app.route('/d/listar')
def depto_listar():
    l = Departamento.query.all()
    return render_template('listarDepartamentos.html',dlista=l)


@app.route('/d/editar/<id>')
def editarDepartamento(id):
    d = Departamento.query.get(id)
    return render_template('editarDepartamento.html',depto=d)


@app.before_first_request
def before():
    db.create_all()



if __name__ == '__main__':
    app.secret_key = 'minha chave'
    app.env = 'development'
    app.run(debug = True)
