import json
import graphe
import random

class Tableau:
    def __init__(self, prefixe, cle, valeur):
        self.cle = cle
        self.peintre = valeur[1]
        self.nom = valeur[2]
        self.annee = valeur[3]
        self.hauteur = valeur[4]
        self.largeur = valeur[5]
        self.tags = valeur[6]
        self.url = prefixe + cle + ".jpg"

class Musee:
    def __init__(self, prefixe, nomFichier):
        self.tableaux = {}
        self.prefixe = prefixe
        
        self.relationsEntrePeintres = {
            'Manet': {'Monet': 1, 'Morisot': 1, 'Bazille': 0.5},
            'Monet': {'Sisley': 1, 'Caillebotte': 0.75}
        }

        data = {}

        # Creation du graphe et ajout des concepts
        # ========================================
        self.graphe = graphe.Graphe()
        self.graphe.root = graphe.Noeud("root", None, self.graphe)

        with open("./serveur/concepts.csv", "r") as f:
            for ligne in f:
                mots = ligne.split(',')
                fils = mots[0]
                pere = mots[1]
                noeudPere = self.graphe.ajouterNoeud(pere, None)
                noeudFils = self.graphe.ajouterNoeud(fils, None)
                self.graphe.ajouterArc(noeudFils, noeudPere, 1.0)

        # Lecture du fichier qui contient la description des tableaux
        # ===========================================================
        with open(nomFichier, "r") as f:
            data = json.load(f)

        self.peintres = data["peintres"]
        tableaux = data["tableaux"]
        self.tableaux = {}
        for cle in tableaux:
            self.tableaux[cle] = Tableau(prefixe, cle, tableaux[cle])
            l = tableaux[cle][6]  # la liste des tags

            # Dans le graphe chaque tableau est identifiee par : cle
            # cle permet d'acceder aux proprietes du tableau dans le dictionnaire self.tableaux
            noeudObjet = self.graphe.ajouterObjet(cle, l[:])
            for concept in l:
                noeudConcept = self.graphe.ajouterNoeud(concept, None)
                self.graphe.ajouterArc(noeudObjet, noeudConcept, 1.0)
            
        self.graphe.calculNiveau() #added this
        
        # Pour test
        # for noeud in self.graphe.noeuds:
        #     print("Nom : ", self.graphe.noeuds[noeud].nom)
        #     print("Parents : ", [x.nom for x in self.graphe.noeuds[noeud].parents])

    def peintsPar(self, peintre):
        """Retourne une liste de tableaux peints par le peintre spécifié."""
        l = list(self.tableaux.values())
        res = [x for x in l if x.peintre == peintre]
        return res

    def get_rd_tableau(self):
        """Retourne un tableau au hasard du musée."""
        if not self.tableaux:
            raise ValueError("No tableaux available")
        # Choose a random tableau key
        key = random.choice(list(self.tableaux.keys()))
        tableau = self.tableaux[key]
        return key, tableau
    

