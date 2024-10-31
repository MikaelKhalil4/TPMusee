

class Noeud : 

  def __init__(self, nom, data, graphe):
    self.nom     = nom
    self.gr      = graphe
    self.niveau  = 1
    self.interet = 1.0
    self.parents = []
    self.enfants = []

  def charger(self, concepts, inventaire):
    pass
     
  def ajouterParent(self, noeud):
    self.parents.append(noeud)
    
  def ajouterEnfant(self, noeud):
    self.enfants.append(noeud)
    
  def consulterParents(self):
    return self.parents
    
  def consulterEnfants(self):
    return self.enfants
    
  def modifierInteret(self,interet):
    self.interet = interet
    
  def ajouterInteret(self, dInteret):
    self.interet += dInteret
    
  def consulterInteret(self):
    return self.interet
    
  def arc(self, noeud1, noeud2):
    return self.gr.arcs.get((noeud1.nom, noeud2.nom), None)
    
  def calculNiveau(self):
    if self.enfants == [] :
      return 0
    else:
      l = [noeud.calculNiveau() for noeud in self.enfants]
      self.niveau = 1 + max(l)
     # print(self.niveau)
      return self.niveau
      

      

class Objet(Noeud):
  def __init__(self, nom, tags, gr):
    Noeud.__init__(self,nom, tags, gr)
    self.tags     = tags
    self.niveau   = 0

  def calculInteret(self):
    if self.parents != [] : 
      self.interet = sum([p.consulterInteret() for p in self.consulterParent()])    

# ========================================================

class Graphe :

  def __init__(self):
    self.noeuds  = {}
    self.arcs    = {}
    self.root    = None
    self.niveaux = []

  def calculerObjetsLesPlusInteressants(self,tableaux,n_elements):
    resultat = []
    dico_interest = {}

    for tab in tableaux : 
      self.calculerInteretObjet(tab)
      dico_interest[tab.nom] = tab.interet

    dict_tri = dict(sorted(dico_interest.items(), key=lambda item:item[1],reverse=True))
       
    # Au lieu d'en renvoyer tout le temps 5, on renvoie soit les 5 premiers, soit les N premiers qui ont le meme interet
    first_interet = None
    for key,value in dict_tri.items():
        # On sauvegarde l'interet le plus haut
        if first_interet == None:
            first_interet = value
        # Condition d'arret
        if len(resultat)>=n_elements and value != first_interet:
            break
        resultat.append(key)
    
    return resultat 


  def calculerInteretObjet(self ):
    pass

  def obtenirNoeudConnaissantNom(self,nom):
    return self.noeuds.get(nom, None)

  def consulterObjets(self):
    return self.niveaux[0]

  def consulterTags(self):
    return self.niveaux[1]

  def consulterNiveau(self,i):
    return self.niveaux[i]
    
  def montrerDoiNiveau(self,i):
    return dict((n.nom,n.doi) for n in self.niveaux[i])


  def ajouterNoeud(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Noeud(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]

  def ajouterObjet(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Objet(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]
  def ajouterArc(self, noeud1, noeud2, w):
    self.arcs[(noeud1.nom, noeud2.nom)] = w 	  
    noeud1.ajouterParent(noeud2)
    noeud2.ajouterEnfant(noeud1)
    
  def calculNiveau(self):
    n = self.root.calculNiveau() + 1
    

    self.niveaux = [[] for i in range(n+1)]
    for noeud in self.noeuds.values() : 
      #print(">>>> ", noeud.nom, " > ", noeud.niveau)
      self.niveaux[noeud.niveau].append(noeud)

  def interetObjets(self):
    pass

   # Question 3.
  def asynchrone(self,o):

    if not isinstance(o, Noeud):
      return
  
    tagsTab = o.tags
    
    allTags = self.consulterTags()

#    print(tagsTab)

    # Variables
    tau = 0.5
    C = 0
    Vo = 0

    for tag in allTags :
      C += tau * tag.interet


    for tag in tagsTab :
    #  print("tag :" + tag + " interet : " + str(self.obtenirNoeudConnaissantNom(tag).interet))
      Vo += self.obtenirNoeudConnaissantNom(tag).interet

    if Vo == 0 :
      R = 0
    else :
      R = C / abs(Vo)

    #Variation interet tag du tableau
    for t in tagsTab :
      #Delta_I(w) = R - tau * I(w)
      noeud_t = self.obtenirNoeudConnaissantNom(t)
      noeud_t.modifierInteret(noeud_t.interet + (R - tau *  noeud_t.interet))

    #Variation interet des autres tag
    for t in allTags :
      if t.nom not in tagsTab :
        noeud_t = t
        noeud_t.modifierInteret(noeud_t.interet + (-tau *  noeud_t.interet))

    #for t in allTags :
     # print(t.nom + " : " + str(t.interet))


  def synchrone(self):
    omega = 0.5

    # Calcul de Iavg
    Iavg = 0
    quantiteRecup = 0
    nbInf = 0

    allTags = self.consulterTags()
    for t in allTags : 
      Iavg += t.interet

    Iavg = Iavg / len(allTags)
    
    # On recupre les tags avec interet suprieur  Iavg
    for t in allTags : 
      if t.interet > Iavg :
        quantiteRecup += omega*(t.interet - Iavg)
        t.modifierInteret(t.interet - omega*(t.interet - Iavg))

    # On rcupre les tags avec interet infrieur  Iavg
    for t in allTags :
      if t.interet < Iavg :
        nbInf += 1

    for t in allTags :
      if t.interet < Iavg :
        t.modifierInteret(t.interet + quantiteRecup/nbInf)

   # for t in allTags :
    #  print(t.nom)
     # print(t.interet)
      
  def calculInteretMax(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    return max(l)
    
  def normalisationInteret(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    interetMax = max(l)
    for noeud in self.noeuds.values():
      noeud.interet = noeud.interet / doiMax
      
  def calculUpInteret(self):
    pass
        
  def calculDownInteret(self):
    pass
