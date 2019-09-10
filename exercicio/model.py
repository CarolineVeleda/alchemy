from flask import Flask,render_template, request,session, redirect
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

app = Flask(__name__) 

uri= 'postgresql://postgres:postgres@localhost:5432/exercicio'
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

'''
class Departamento(db.Model):
    __tablename__ = 'departamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    #data_atualizacao = db.Column(db.DateTime, unique=True,default=db.func.now())
'''

class Departamento(db.Model):
    __tablename__ = 'departamento'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_atualizacao = db.Column(db.DateTime, unique=True,default=db.func.now(), onupdate=db.func.now())
    funcionarios = db.relationship ('Funcionario', backref= 'departamento', lazy= 'select')
    endereco = db.relationship ('Endereco', lazy= 'joined', uselist= False)
    idendereco = db.Column(db.Integer, db.ForeignKey('endereco.id', ondelete='set null', onupdate='cascade'))

    def salvar(self, d):
        #verifica=hasattr(d, 'id')
        if (d.id):
            db.session.merge(d)
            db.session.commit()
        else:
            db.session.add(d)
            db.session.commit()
 
    def excluir(self,id):
        db.session.delete(id)
        db.session.commit()


class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    iddepartamento = db.Column(db.Integer, db.ForeignKey('departamento.id', ondelete='cascade', onupdate='cascade'))


class Endereco(db.Model):
    __tablename__ = 'endereco'
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.Integer, nullable=False)
    rua = db.Column(db.String(100), nullable=False)

    def salvar(self, e):
        #verifica=hasattr(e, 'id')
        if (e.id):
            print("endereco: tem id")
            print(e.id)
            db.session.merge(e)
            db.session.commit()
        else:
            print("endereco: não tem id")
            db.session.add(e)
            db.session.commit()
 
    def excluir(self,id):
        db.session.delete(id)
        db.session.commit()
    



@app.route('/d/salvar',methods=["POST","GET"])
def depto_inserir():
    if request.method == "POST":
        d = Departamento()
        d.nome = request.form['nome']
        
        e = Endereco()
        e.numero = request.form['numero']
        e.rua = request.form['rua']

        coddepto=request.form["iddepartamento"]
        codendereco=request.form["idendereco"]

        if (coddepto):
            d.id=int(coddepto)
        
        if (codendereco):
            e.id=int(codendereco)

        d.endereco = e
        d1=d
        e1=e
        d.salvar(d1)
        e.salvar(e1)
        return redirect("/d/listar")

    return render_template('inserirDepartamento.html')


@app.route('/d/listar')
def deptoListar():
    l = Departamento.query.all()
    return render_template('listarDepartamentos.html',dlista=l)


@app.route('/d/editar/<id>')
def editarDepartamento(id):
    d = Departamento.query.get(id)
    return render_template('editarDepartamento.html',depto=d)


@app.route('/d/excluir/<id>')
def excluirDepartamento(id):
    d = Departamento()
    dbusca = Departamento.query.get(id)
    d.excluir(dbusca)
    return redirect("/d/listar")





@app.before_first_request
def before():
    db.create_all()



if __name__ == '__main__':
    app.secret_key = 'minha chave'
    app.env = 'development'
    app.run(debug = True)
