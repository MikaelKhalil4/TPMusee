
# ==================================================================
#
# Schéma d un serveur
#
# ===================================================================

from  flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)



@app.route('/init')
def init():
     resultat = []
     return jsonify(resultat)
     

@app.route('/tictac')
def tictac():
    t = request.args.get("Time",default=0,type=float)
    
    resultat = []
    return jsonify(resultat)


@app.route('/salle/')
def onSalle():
  i = request.args.get("I",default=0,type=int)
  j = request.args.get("J",default=0,type=int)
  print("CHANGEMENTDE SALLE : i=",i," - j=",j)
  
  resultat = []
  return jsonify(resultat)

@app.route('/click/')
def onClick():
    x = request.args.get('X', default=0,type=float)
    y = request.args.get('Y', default=0,type=float)
    z = request.args.get('Z', default=0,type=float)
    nomObjet = request.args.get('Nom')

    if nomObjet != None : 

        print("Objet sélectionné : ",nomObjet)
        print("Point d'intersection : ",x," - ", y ," - ",z)

    resultat = []
    return jsonify(resultat)


@app.route('/assets')
def assets():
    materiaux = {}
    
    materiaux["rouge"] = {"color":[1,0,0]}
    materiaux["vert"]  = {"color":[0,1,0]} 
    materiaux["bleu"]  = {"color":[0,0,1]} 
    materiaux["blanc"] = {"color":[1,1,1], "texture":"./assets/textures/murs/dante.jpg","uScale":1,"vScale":1}
    materiaux["murBriques"] = {"color":[1,1,1], "texture":"./assets/textures/murs/briques.jpg","uScale":2,"vScale":1}
    materiaux["murBleu"] = {"color":[1,1,1], "texture":"./assets/textures/murs/bleuCanard.jpg","uScale":2,"vScale":1} 
    materiaux["parquet"] = {"color":[1,1,1], "texture":"./assets/textures/sol/parquet.jpg","uScale":2,"vScale":2}   
if __name__ == "__main__" : 
    app.run(debug=True)
