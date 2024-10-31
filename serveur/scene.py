


class Acteur : 
  def __init__(self, nom, leType):
    self.json = {"op":"CREATE",
        "id":nom,
        "type":leType,
        "components":[]
        }
        
  def add(self,comp):
    self.json["components"].append(comp)
    return self
    
  def addS(self,l):
    self.json["components"] = self.json["components"] + l
    return self
    
  def toJSON(self):
    return self.json


class Scene : 
  def __init__(self):
    self.scene = {}     # contient tous les acteurs
    self.assets = {}
    
  def actors(self):
    return list(self.scene.keys())
    
  def actor(self,nom,leType):
    a = Acteur(nom, leType)
    self.scene[nom] = a
    return a
    
  def getActor(self, nom):
    return self.scene[nom]

    
  def jsonify(self):
    acteurs = list(self.scene.values())
    l = [x.toJSON() for x in acteurs]
    return l    
    
    
# Les incarnations
# ================

def poster(nom,l,h,url):
  return {
           "type" : "poster",
           "data" : {"name":nom, "largeur":l, "hauteur":h, "tableau":url}
         }
         
def sphere(nom,d,m):
  return {
           "type" : "sphere",
           "data" : {"name":nom, "diameter":d, "material":m}
         }
         
def box(nom,l,h,e,m):
  return {
           "type" : "box",
           "data" : {"name":nom, "width":l, "height":h, "depth":e, "material":m}
         }
         
def wall(nom,l,h,e,m):
  return {
           "type" : "wall",
           "data" : {"name":nom, "width":l, "height":h, "depth":e,"material":m}
         }
         
         
       
         
def porte(nom, l,h,e):
  return {
            "type" : "porte" ,
            "data" : {"name" : nom, "width":l, "height":h, "depth":e}
           
         }
 
def title(nom, titre):
  return {
           "type" : "titre",
           "data" : {"name":nom, "titre":titre}
         }
                 
         
# Le graphe de scène
# ==================
         
def position(x,y,z):
  return {
           "type" : "position",
           "data" : {"x":x, "y":y, "z":z}
         }
         
def rotation(x,y,z):
  return {
           "type" : "rotation",
           "data" : {"x":x, "y":y, "z":z}
         }
         
def anchoredTo(parent):
  return {
           "type":"anchoredTo",
           "data": {"parent":parent}
         }
         
# ===========================================================================

def rejectedByAll(d):
  return {
            "type" : "repulsion",
            "data" : {"range":d}
         }

def friction(k):
  return {
            "type" : "frottement",
            "data" : {"k":k}
         }
         
def attractedBy(acteur):
  return {
           "type" : "attraction",
           "data" : {"attractedBy":acteur}
         }
   
