from flask import Flask, render_template, request, redirect
from markupsafe import escape

import requests as outputRequests
import json
import sys

import config

#declaracion de variables globales
configFile='config/config.json'
parametro=""

app = Flask(__name__)

@app.route('/<dispositivo>/')
def raiz(dispositivo):
#    try:
        #leo el fichero de configuracion
        print('DISPOSITIVO dispositivo: ' + dispositivo,sys.stdout)

        with open(configFile) as json_file:
            configuracion = json.load(json_file)
            Proceso=configuracion.get('Proceso')
            Ip=Proceso['IP']

            Apps=configuracion.get('Apps')
            #print('Configuracion Apps=\n nombre: ', Apps[1]['nombre'],' IP: ', Apps[1]['IP'], '\n\n', file=sys.stdout)
            for x in Apps:
                if(x['nombre']==dispositivo):
                    print('Encontrado!! IP: ', x['IP'], sys.stdout)
                    IPDispositivo=x['IP']
                    print('IPDispositivo: ' + IPDispositivo, sys.stdout)
                    return render_template('main.html', IP=Ip, IPDISPOSITIVO=IPDispositivo, DISPOSITIVO=dispositivo)                    

            print('App no configurada',sys.stdout)
            return f'<p>App no configurada</p>'
          
            return f'<p>Hello, World!<br>We are in {escape(dispositivo)}!!!!!</p><BR> se han configrado'
#    except :
#        print("No se pudo obtener el fichero de configuracion")            
#        return f'Algo salio mal...'

@app.route('/<dispositivo>/<servicio>')
def ficheros(dispositivo,servicio):
#    try:
        #leo el fichero de configuracion
        print('SERVICIO: dispositivo: ' + dispositivo + ' | servicio: ' + servicio + '@',sys.stdout)

        with open(configFile) as json_file:
            configuracion = json.load(json_file)
            Proceso=configuracion.get('Proceso')
            Ip=Proceso['IP']

            Apps=configuracion.get('Apps')
            for x in Apps:
                if(x['nombre']==dispositivo):
                    IPDispositivo=x['IP']
                    Servicios=x['Servicios']
                    for s in Servicios:
                        if(s['nombre']==servicio):
                            fichero=s['fichero']
                            print('Encontrado serivcio: ' + servicio + ' | Fichero: ' + fichero, sys.stdout)
                            return render_template(fichero, IP=Ip, IPDISPOSITIVO=IPDispositivo, DISPOSITIVO=dispositivo)

                    print('Serivcio no encontrado: ' + servicio, sys.stdout)
                    #Leo los parametros y redirecciono
                    parametros=""
                    for param in request.args:
                        if parametros!="": parametros += "&"
                        valor=request.args[param]
                        parametros += param + "=" + valor

                    return redirect('http://'+IPDispositivo+'/'+servicio+'?'+parametros, code=302)

            print('App no configurada',sys.stdout)
            return f'<p>App no configurada</p>'
#    except :
#        print("No se pudo obtener el fichero de configuracion")            
#        return f'Algo salio mal...'
