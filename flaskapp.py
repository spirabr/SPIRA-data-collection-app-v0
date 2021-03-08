
# -*- coding: utf-8 -*-
import sys
import os, os.path
import gc # Garbage Collector'
from datetime import datetime
import uuid
from flask import Flask, render_template, request, redirect, make_response, Response,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session as SessionORM
from sqlalchemy import create_engine
import json
import logging
import logging.handlers
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.son import SON
import hashlib
from bson.objectid import ObjectId
from flask_session import Session
from functools import wraps


app = Flask(__name__,
            static_url_path='',
            static_folder='pages',
            template_folder='pages/templates')

SESSION_TYPE = 'filesystem'
SESSION_FILE_DIR = '/tmp'
app.config.from_object(__name__)
Session(app)

# força login
def restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('auth', False):
            return redirect("logon?err=99")
        return f(*args, **kwargs)
    return decorated_function

# Mongo
client = MongoClient("")
database = client["flaskapp"]

def cookiesRead(cookieStr):
   # Recupera cookie gravado    
   return str(request.cookies.get(cookieStr)).strip() 

def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def cookiesSave(t,cookieStr,cookieContent):
   # Checa Cookie e grava se não houver - Este cookie funciona como uma *chave primária*
   if cookiesRead(cookieStr) == 'None' :
      resp = make_response(render_template(t))
      resp.set_cookie(cookieStr,cookieContent)
   else:
      resp = make_response(render_template(t))
   return resp

def sdb(request):
   # Função que salva o FORM no MySQL e o Wav no FS. Tb Faço backup no FS do FOORM.
   cookie = cookiesRead('flaskapp')

   # Sem cookie? Sem save for you
   if cookie == 'None' :
      return  make_response(render_template('f.html'))

   # Novos campos que não estão no form   
   dataDeCriacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
   enderecoIp = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
   useragent = request.headers.get('User-Agent')

   # Backup no FS em json do form enviado
   with open("/var/www/FlaskApp/data/" + cookie + '.json', 'w') as f:
        dic1 = {k: v for k, v in request.form.items()}
        dic1["dataDeCriacao"] = dataDeCriacao    
        dic1["enderecoIp"] = enderecoIp
        dic1["useragent"] = useragent    
        json.dump(dic1, f)
        f.close()

   # ORM stuffs
   Base = automap_base()
   engine = create_engine('').connect()
   Base.prepare(engine, reflect=True)
   Diagnosticos = Base.classes.diagnosticos
   sessionDB = SessionORM(engine)
   

   # Já respondeu o form? Ciao belo
   diago = sessionDB.query(Diagnosticos).filter(Diagnosticos.diagID == cookie).count()
   if diago > 0 :
      return make_response(render_template('o.html')) 
   del diago
   # Como não respondeu, salvo.
   
   # Dados do form
   if str(request.values.get('idade')) == 'None':
         idade = request.values.get('idade')
   else:
         idade = request.values.get('idade') if int(str(request.values.get('idade'))) < 127 else 127

   genero = request.values.get('genero')

   if str(request.values.get('febre')) == 'None':
         febre = request.values.get('febre')
   else:
         febre = request.values.get('febre') if int(str(request.values.get('febre'))) < 127 else 127
   
   if str(request.values.get('tosse')) == 'None':
         tosse = request.values.get('tosse')
   else:
         tosse = request.values.get('tosse') if int(str(request.values.get('tosse'))) < 127 else 127
   
   if str(request.values.get('dorDeGarganta')) == 'None':
         dorDeGarganta = request.values.get('dorDeGarganta')
   else:
         dorDeGarganta = request.values.get('dorDeGarganta') if int(str(request.values.get('dorDeGarganta'))) < 127 else 127
   
   if str(request.values.get('coriza')) == 'None':
         coriza = request.values.get('coriza')
   else:
         coriza = request.values.get('coriza') if int(str(request.values.get('coriza'))) < 127 else 127

   semsin = request.values.get('semsin')
   faltaDeAr = request.values.get('faltaDeAr')
   doencaCronicaPulmao = request.values.get('doencaCronicaPulmao')
   doencaCoroniana = request.values.get('doencaCoroniana')
   pressaoAlta = request.values.get('pressaoAlta')
   diabetes = request.values.get('diabetes')
   semenfer = request.values.get('semenfer')

   # Objeto novo a ser inserido via ORM
   new_diag = Diagnosticos(diagID = cookie
   ,idade = idade  
   ,genero = genero
   ,febre = febre
   ,tosse = tosse
   ,dorDeGarganta = dorDeGarganta
   ,coriza = coriza
   ,semsin = semsin
   ,faltaDeAr = faltaDeAr
   ,doencaCronicaPulmao = doencaCronicaPulmao
   ,doencaCoroniana = doencaCoroniana
   ,pressaoAlta = pressaoAlta
   ,diabetes = diabetes
   ,semenfer = semenfer
   ,dataDeCriacao = dataDeCriacao
   ,enderecoIp = enderecoIp
   ,useragent = useragent)
   
   # Vai pro MySQL já!
   sessionDB.add(new_diag)
   sessionDB.commit()
   sessionDB.flush()
   sessionDB.close()

   # tenta destuir tudo que possa ter ficado
   del engine
   del Diagnosticos
   del sessionDB
   gc.collect

   return  make_response(render_template('o.html'))

@app.route('/')
def inicio():
   # Home do Site
   u = str(uuid.uuid4())
   return cookiesSave('i.html','flaskapp',u)
   
@app.route('/f')
def formulario():
   # Form de Pesquisa - PRINCIPAL
   useragent = request.headers.get('User-Agent') 
   if useragent.find('FBA') > 0 :      
      if useragent.find('Chrome') > 0 :
            return render_template('fbb.html',browser='Chrome')
      else :
            return render_template('fbb.html',browser='Safari')
   u = str(uuid.uuid4())
   return cookiesSave('f.html','flaskapp',u)

@app.route('/a')
def audio():
   # Audio check -- OLD ??? --
   u = str(uuid.uuid4())
   return cookiesSave('a.html','flaskapp',u)

@app.route('/r')
def frases():
   # Iframe que grava voz -- OLD ??? --
   id = int(request.args.get('id'))
   frases = ['','O amor ao próximo ajuda a enfrentar o coronavírus com a força que a gente precisa.', 'Batatinha quando nasce, espalha rama pelo chão.', 'Parabéns a você, nesta data querida, muitas felicidades, muitos anos de vida.']
   instrucoes = ['','Leia a frase:', 'Leia a frase:', 'Cante ou Leia a frase:']
   return render_template('r.html',frase=frases[id],instrucao=instrucoes[id])

@app.route('/s', methods=['POST'])
def insert ():
    # Processa form da pesquisa
    return sdb(request)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   # grava arquivos (frases faladas) no FS
   cookie = cookiesRead('flaskapp')
   if cookie == 'None':
      return 'sem cookie!'
   id = request.values.get('id')
   if request.method == 'POST':
      f = request.files['audio_data']
      f.save('/var/www/FlaskApp/audios/' + cookie + '_' + id + '.wav')
      #f.save('c:\\tmp\\' + cookie + '_' + id + '.wav')
      f.flush()
      f.close()
   return 'file uploaded successfully'

@app.route('/o')
def obrigado():
   # Página de Obrigado
   resp = make_response(render_template('o.html'))
   return resp      

@app.errorhandler(404)
# Página 404
def not_found_404(e):
  return render_template('404.html')

@app.errorhandler(500)
def internal_server_error_500(e):
  # Página de Erro 500
  return render_template('500.html')

@app.route('/t')
def table():
   # Tem utilidade???
   return render_template('t.html')

@app.route('/form', methods=['POST'])
@restricted
def formPOST():
   # Salva anotações feita por formGET
   collection_ = database["human"]
   collection = database["human"]
   human_dict = request.form.to_dict()

   _id = human_dict['_id_']
   myquery = { "_id": ObjectId(_id) }
   newvalues = { "$set": { "done": "2" } }
   collection_.update_one(myquery, newvalues)

   human_dict["data"] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   human_dict["humano"] =  session.get('humano', False)
   collection.insert_one(human_dict)
   return redirect("anotacoes")

@app.route('/signup', methods=['POST'])
def signupPOST():
   # Cria novo Usuário
   collection = database["logon"]
   email = request.values.get('email')
   query = {}
   query["email"] = email.lower()
   projection = {}
   projection["nome"] = u"$nome"
   projection["_id"] = 0
   cursor = collection.find(query, projection = projection)
   nome = '1'
   for doc in cursor:
      nome = doc
   if(nome!='1'):
      goto = 'signup?email=1'
      return redirect(goto)
   s_dict = request.form.to_dict()
   s_dict["data"] =  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
   email = s_dict["email"]
   s_dict["email"] = email.lower()
   s_dict["senha2"] =  ''
   formPassword = request.values.get('senha')
   h = hashlib.md5(formPassword.encode())
   password = h.hexdigest()
   s_dict["senha"] =  password
   s_dict["ativo"] =  '0'
   collection.insert_one(s_dict)
   return redirect("logon?logon=1")

@app.route('/logon')
def logonGet():
   #Render form de Logon
   logon = request.values.get('logon')
   return render_template('logon.html',logon = logon)

@app.route('/signup')
def signupGet():
   # REnder form de Signup
   email = request.values.get('email')
   return render_template('signup.html', email = email)


@app.route('/logon', methods=['POST'])
def logonPOST():
   # Autentica User
   collection = database["logon"]
   email = request.values.get('email')
   formPassword = request.values.get('senha')
   h = hashlib.md5(formPassword.encode())
   password = h.hexdigest()
   query = {}
   query["email"] = email.lower()
   query["senha"] = password
   projection = {}
   projection["nome"] = u"$nome"
   projection["_id"] = 0
   cursor = collection.find(query, projection = projection)
   nome = '1'
   for doc in cursor:
      nome = doc
   if(nome=='1'):
      goto = "logon?logon=2"
      session['auth'] = False
   else:
      goto = 'ranking'
      session['auth'] = True
      session['humano'] = nome['nome']
   return redirect(goto)

@app.route('/ranking')
@restricted
def ranking():
   # Ranking de quem anotou
   collection = database["human"]  
   pipeline = [
      {
         u"$match": {
               u"done": {
                  u"$ne": u"2"
               }
         }
      }, 
      {
         u"$group": {
               u"_id": {
                  u"humano": u"$humano"
               },
               u"COUNT(*)": {
                  u"$sum": 1
               }
         }
      }, 
      {
         u"$project": {
               u"humano": u"$_id.humano",
               u"COUNT(*)": u"$COUNT(*)",
               u"_id": 0
         }
      }, 
      {
         u"$sort": SON([ (u"COUNT(*)", -1) ])
      }
   ]

   cursor = collection.aggregate(
      pipeline, 
      allowDiskUse = True
   )

   cursor = collection.aggregate(
      pipeline, 
      allowDiskUse = True
   )
   #try:
      #for doc in cursor:
       #  print(doc)
   #finally:
      #client.close()
   return render_template('ranking.html', objects = cursor)

def root_dir():  # pragma: no cover
    return os.path.abspath('/extra/spira/anotacoes/dados_clipped/')
    
def get_file(filename):  # pragma: no cover
    # Read de arquivo para não dar acesso ao file system
    try:
        src = os.path.join(root_dir(), filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src,"rb").read()
    except IOError as exc:
        return str(exc)

@app.route('/aud')
@restricted
def aud():  # pragma: no cover
   # Stream do arquivo para não dar acesso ao file system
   arquivo = request.values.get('arquivo')
   mime = "audio/wav"
   if arquivo.find("/") == -1:      
      content = get_file('controles/audio/' + arquivo)
   else:
      content = get_file('pacientes/audio/' + arquivo)
       
   return Response(content, mimetype=mime)

@app.route('/anotacoes')
@restricted
def anotacoes():
   # Datatable de anotacoes
   collection = database["human"]
      
   query = {"done": {"$ne": '2' }}
   sort = [ (u"done", 1) ]

   projection = {}
   projection["base"] = u"$base"
   projection["arquivo"] = u"$arquivo"
   projection["idade"] = u"$idade"
   projection["sexo"] = u"$sexo"
   projection["oxigenacao"] = u"$oxigenacao"
   projection["humano"] = u"$humano"
   projection["aprovado"] = u"$aprovado"
   projection["data"] = u"$data"
   projection["done"] = u"$done"
   projection["frase_falada"] = u"frase_falada"
   projection["dificuldade_falar"] = u"dificuldade_falar"
   projection["pausa_meio_palavras"] = u"pausa_meio_palavras"
   projection["guaguejou"] = u"guaguejou"
   projection["ruido_fundo"] = u"ruido_fundo"
   projection["ruido_instrumento"] = u"ruido_instrumento"
   projection["voz_medico_inicio"] = u"voz_medico_inicio"
   projection["_id"] = 0
   cursor = collection.find(query, sort = sort, projection = projection)
   return render_template('anotacoes.html', objects = cursor)

@app.route('/form')
@restricted
def formGET():

   #return "Sistema em Manutenção"

   # Render do form de anotacoes
   database = client["flaskapp"]
   collection = database["human"]
   arquivo = request.values.get('arquivo')
   query = {}
   query["arquivo"] = arquivo
   projection = {}
   projection["tupla"] =  u"$tupla" 
   projection["arquivo"] =  u"$arquivo" 
   projection["base"] = u"$base"
   projection["idade"] = u"$idade"
   projection["sexo"] = u"$sexo"
   projection["oxigenacao"] = u"$oxigenacao"
   projection["_id"] = u"$_id"
   cursor = collection.find(query, projection = projection)
   return render_template('form.html',objects = cursor)

@app.route('/postdoc')
def postdoc():
   #Render page postdoc
   return render_template('postdoc.html')

@app.route('/description')
def description():
   #Render page description
   return render_template('description.html')

if __name__ == '__main__':
   app.secret_key = 'qyqtqqt51515haha773h38!!@#'
   app.run(debug = True,host='0.0.0.0',ssl_context='adhoc')

