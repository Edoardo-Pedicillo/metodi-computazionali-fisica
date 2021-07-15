import random

def based_ordered_crossover(p1,p2, ncities=None,selected_cities=None):
    """
        Prende gli elementi di selected_cities in p2 e le modifica nell'ordine dato 
        da come compaiono in p1

    """

    if ncities==None and selected_cities==None:
         ncities=random.randint(0,len(p1))
        

    if selected_cities==None:
        selected_cities=random.sample(p1,k=ncities)
        ncities=len(selected_cities)

    son=[i for i in p2]
    
    sel_cities_p1=[i for i in p1 if i in selected_cities]# salva le città selezionate nell'ordine 
                                                        #in cui compaiono in p1
    
    app=0
    for i,item in enumerate( son):
        if item in selected_cities:# Ogni volta che trovo una città selezionata in son (copia di p2)
                                    #la sostituisco con una in sel_citites_p1 e ne aumento il contatore app di 1
            
            son[i]=sel_cities_p1[app]
            
            app+=1

   
    return son

def modified_ordered_crossover(p1,p2,position=None):
    """
        Come based_ordered_crossover ma gli elementi in selected_cities sono quelle che compaiono
        a destra di p1[position-1] 
    """
    if (position==None):
        position=random.randint(0,len(p1))
    
    selected_cities=p1[position: : ]
   
    return based_ordered_crossover(p1,p2,selected_cities=selected_cities)

def partially_mapped_crossover (p1,p2,position1=None,position2=None):
    """
        Il primo punto di crossover è subito dopo position1.
        Il secondo punto di crossover è subito dopo position2. 

    """
    if position1==None:
        position1=random.randint(0,len(p1))

    if position2==None:
        position2=random.randint(position1,len(p1))
    
    map1=p1[position1:position2:]
    map2=p2[position1:position2:]

    son=p1[:position1:]+map2+p1[position2::] # Scambio le due liste di mappa
    
    for i,item in enumerate(son[:position1:]): # Controllo se nella prima parte di son[]
                                            #ci sono elementi che si ripetono
       
        if item in map2:
            son[i]=map1[map2.index(item)]
            

    for i,item in enumerate(son[position2::]): # Controllo se nella seconda parte di son[]
                                            #ci sono elementi che si ripetono
        if item in map2:
            son[position2+i]=map1[map2.index(item)]
            
    return son

def cycle_crossover(p1,p2,begin_parent=None,verbose=False):
    """
        begin_parent indica quale genitore verrà scelto per primo all'inizio o quando 
        un ciclo termina (0 per p1 e 1 per p2 ). In caso contrario la scelta è random.
        Verbose=True permette di stampare le varie fasi di cycle_crossover.
    """
    son= [None for i in p1]
    parents=[p1,p2]
    while None in son:#Fino a quando son[] non è totalmente riempito
        if begin_parent==None:
            nparent=random.randint(0,1)#Scelgo il genitore con cui iniziare 
        else:
            nparent=begin_parent

        app=son.index(None)
        #print(parents)
        son[app]=parents[nparent][app]#Cerco primo elemento None e lo sostituisco con l'elemento
                                    # con stesso indice di uno dei genitori scelto random 
         
        if verbose==True:
                print(son)
                

        nparent=(nparent+1)%2 # mi sposto nell'altro genitore       

        app = parents[nparent].index(son[app])#cerco indice dell'elemento son[app] e lo salvo in app                        
           
        while son[app]==None: # Se quell'indice app corrisponde ad un elemento vuoto di son[]
                
            nparent=(nparent+1)%2 
            son[app]=parents[nparent][app]
            nparent=(nparent+1)%2 
            app = parents[nparent].index(son[app])
            if verbose==True:
                print(son)
    return son 