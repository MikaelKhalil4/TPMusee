
# ==================================================================
#
# Schéma d un serveur
#
# ===================================================================
import random
import musee
import scene
import math
from  flask import Flask, jsonify, request
import graphe as g

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)

# Define global variables
laScene = None
mymusee = None
top_objects = None
is_from_the_previous_round = False
peinture_utilisee = {} #dictionnair cle:nom de la peinture, valeur:tableau
dx = 10
dz = 10

def RetourneTopTableauRelieAuTag():
    
    global mymusee
    graph = mymusee.graphe

    # Simulate entering a new room and randomly selecting a keyword (tag)
    all_tags = list(set(tag for noeud in graph.noeuds.values() if isinstance(noeud, g.Noeud) and not isinstance(noeud, g.Objet) for tag in [noeud.nom]))
    selected_tag_name = random.choice(all_tags)
    print(f"Selected tag: {selected_tag_name}")

    # Increase the interest of the selected tag to simulate user interest
    selected_tag_node = graph.noeuds[selected_tag_name]
    # selected_tag_node.interet += 5.0  # Increase the interest significantly

    # Optionally, you can normalize interest values if needed
    # graph.normalisationInteret()

    # Calculate the top N objects based on interest levels
    N = 10
    top_objects = graph.calculerObjetsDInteret(N)
    # selected_tag_node.interet = 1.0 #reset the value
    
    # Display the results
    print(f"\nTop {N} objects based on interest levels:")
    for obj in top_objects:
        tableau = mymusee.tableaux[obj.nom]
        print(f"- ID: {obj.nom}, Title: {tableau.nom}, Interest Level: {obj.interet}")
        print(f"  Tags: {', '.join(obj.tags)}")
        print()
    
    return top_objects





@app.route('/init')
def init():
    print("INIT")

    global laScene ,mymusee,dx,dz

    laScene= scene.Scene()
    mymusee = musee.Musee("./assets/expo/", "./serveur/inventaire.json")


    for i in range(0, 5):
        for j in range(0, 5):
            x = i * dx
            z = j * dz
            suffixe = str(i) + "-" + str(j)
            if i<4 and j<4:
             nomSalle = "salle-" + suffixe
             laScene.actor(nomSalle, "actor").add(scene.sphere(nomSalle, 0.2, "vert")) \
                .add(scene.position(x, 0, z))
            
            nomMurH = "H-" + suffixe
            laScene.actor(nomMurH, "actor").add(scene.wall(nomMurH, 8, 3, 0.1, "murBleu")) \
                .add(scene.position(x - dx / 2, 0, z - dz / 2))
            
            nomMurV = "V-" + suffixe
            laScene.actor(nomMurV, "actor").add(scene.wall(nomMurV, 8, 3, 0.1, "murBleu")) \
                .add(scene.position(x - dx / 2, 0, z - dz / 2)) \
                .add(scene.rotation(0, math.pi / 2, 0))
                    
            # Add the roof
            laScene.actor("toit", "actor") \
                .add(scene.box("toit", 50, 0.1, 50, "blanc")) \
                .add(scene.position(15, 3, 15))  # Center position for the roof
            # if i<4 and j<4:
            #  add_poster(nomSalle, x, z)  # Use the updated decorate function

    return jsonify(laScene.jsonify())



def add_poster(room_name, x_center, z_center, a=5, b=3, wall_thickness=0.07):

    global laScene ,mymusee,top_objects

    a -= wall_thickness 
    h = 2
    positions = [(a, h, b), (b, h, a), (b, h, -a), (a, h, -b), (-a, h, -b), (-b, h, -a), (-b, h, a), (-a, h, b)]
    
    for pos in positions:
        painting_name = "painting_" + str(x_center) + "_" + str(z_center) + "_" + str(round(pos[0])) + "_" + str(round(pos[2]))
    
        if painting_name not in laScene.scene:
            
            if (top_objects is None or len(top_objects)==0) and is_from_the_previous_round is False == 0:
                key, tableau = mymusee.get_rd_tableau()
            elif top_objects is not None and len(top_objects) > 0:
                key = top_objects.pop(0).nom
                tableau = mymusee.tableaux[key]
            else:
                 tableau = None
                

            if tableau is not None:

                orientation = 0
                if abs(pos[0]) > b:
                    orientation = math.pi / 2 * (1 if pos[0] > 0 else -1)
                elif abs(pos[2]) > b:
                    orientation = math.pi * (0 if pos[2] > 0 else 1)

                # Add the random tableau to the scene
                peinture_utilisee[painting_name] = tableau
                painting = laScene.actor(painting_name, "actor").add(scene.poster(painting_name, tableau.largeur / 100, tableau.hauteur / 100, tableau.url))
                painting.add(scene.position(pos[0], pos[1], pos[2])).add(scene.rotation(0, orientation, 0))
                painting.add(scene.anchoredTo(room_name))


@app.route('/tictac')
def tictac():
    t = request.args.get("Time", default=0, type=float)
    
    global mymusee
    if mymusee is not None:
        # Call synchrone method every time to smoothly dampen interests
        mymusee.graphe.synchrone()
    
    resultat = []
    return jsonify(resultat)









@app.route('/salle/')
def onSalle():
  i = request.args.get("I",default=0,type=int)
  j = request.args.get("J",default=0,type=int)
  print("CHANGEMENTDE SALLE : i=",i," - j=",j)

  if(i<4 and j<4):
        
        global laScene ,mymusee,top_objects,is_from_the_previous_round,dx,dz
        top_objects=[]

        suffixe = str(i) + "-" + str(j)           
        nomSalle = "salle-" + suffixe

        if(len(top_objects)==0):
            top_objects = RetourneTopTableauRelieAuTag()
        
        is_from_the_previous_round = False # reset the value
        add_poster(nomSalle, i * dx, j * dz)# at this level men kun mallayna el ouda, eza na2sa el ouda
        


        if(len(top_objects)>0):
            if(i<3):
                is_from_the_previous_round = True
                k=i+1
                suffixe = str(k) + "-" + str(j)           
                nomSalle = "salle-" + suffixe
                add_poster(nomSalle, k * dx, j * dz)
            elif (j<3):
                is_from_the_previous_round = True
                k=j+1
                suffixe = str(i) + "-" + str(k)           
                nomSalle = "salle-" + suffixe
                add_poster(nomSalle, i * dx, k * dz)


  
  return jsonify(laScene.jsonify())










@app.route('/click/')
def onClick():
    x = request.args.get('X', default=0,type=float)
    y = request.args.get('Y', default=0,type=float)
    z = request.args.get('Z', default=0,type=float)
    nomPeinture = request.args.get('Nom')

    if nomPeinture != None : 
        global mymusee,peinture_utilisee
        if nomPeinture in peinture_utilisee.keys():
            Tableau = peinture_utilisee[nomPeinture]
            Objet = mymusee.graphe.obtenirNoeudConnaissantNom(Tableau.cle)
            mymusee.graphe.asynchrone(Objet)

        print("Objet sélectionné : ",Objet.nom)
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
    materiaux["posterImage"] = {"color":[1,1,1], "texture":"../assets/expo/BAZ02.jpg","uScale":2,"vScale":2}   
    return jsonify(materiaux)


if __name__ == "__main__" : 
    app.run(debug=True)
