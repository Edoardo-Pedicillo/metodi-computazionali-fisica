from random import randint
import random
import crittografia 
import argparse
import string

#Prendo argomenti passati da comando
parser = argparse.ArgumentParser(description= "Programma di decrittazione tramite algoritmi genetici")
parser.add_argument('file_name', help="Inserire il nome del file da decrittare. Il file non deve contenere righe vuote (paragrafi)", type=str)
parser.add_argument('len_key', help="Lunghezza della chiave", type=int)
parser.add_argument('--key', help="chiave: se si passa l'argomento key il programma codifica tramite cifrario di Vigenere e tenta di decrittare il messaggio. Se omesso key = None", type=str, default=None)
parser.add_argument('--ngen', help="numero di generazioni. Se omesso ngen = 200", type=int,default=200)
parser.add_argument('--mut_prob', help="probabilità di mutazione. Se omesso mut_prob = 0.1", type=float,default=0.1)
parser.add_argument('--npop', help="numero di individui nella popolazione. Se omesso npop = 400", type=int,default=400)
args = parser.parse_args()

file_name = args.file_name
len_key = args.len_key
ngen = args.ngen
mut_prob = args.mut_prob
key_true=args.key
npop=args.npop


alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

#salva info frequenze 
#digraph e trigraph sono liste di liste (matrici): ad ogni riga corrispone una lista 
# di caratteri che formano una coppia o un tripletto di caratteri ferquenti

letters=open("letters.txt").read().split( )# viene letto il file, salvato con read() e separato in list di coppie con split()

digraphs= open("digraphs.txt").read().split() 
                                                                
trigraphs= open("trigraphs.txt").read().split()

two_words=open("two_words.txt").read().split()

three_words=open("three_words.txt").read().split()

four_words=open("four_words.txt").read().split()

one_words= open("one_words.txt").read().split()


def txt_set(message):
    """
       elimina dal testo tutto ciò che non sono caratteri e rende tutte le lettere minuscole.
       Restituisce una lista
    """
    message_list=list(message.lower())
    new_message_list=[]
   
    for item in message_list: # devo usare liste perchè stringhe immuatbili
        
        if item in alphabet:
          new_message_list.append(item)
        
    
    
    mess="".join(new_message_list)
    new_mess=mess.replace("  "," ")

    while new_message_list[-1]==" ": # elimina gli spazi alla fine del testo
        
        new_message_list.pop( )
    
    return new_mess


class Individual(list):
    
    
    def __init__(self,key,fitness=None): # la fitness è inizializzata a None 
        
        self.fitness=fitness
        self.key=key 

    def set_fitness(self,message):
        
        fitness=0
        key=self.key
        new_message=crittografia.decritt_Vigenere(message,"".join(key)) # decritto il messaggio
        
        words = new_message.split(' ')

        max_len=len( max(words, key = lambda k: len(k)))
              
        
        for i,item in enumerate(digraphs):
            fitness+=new_message.count(item)*1
        
        for i,item in enumerate(trigraphs):
            fitness+=new_message.count(item)*1
        
        
        for i in words:
            if len(i)==1:
                if i in one_words:
                    fitness+=1
                else:
                    fitness-=2 # vengono inserite delle penalità

            if len(i)==2:
                if i in two_words:
                    fitness+=1
                else:
                    fitness-=0

            if len(i)==3:
                if i in three_words:
                   fitness+=1
                else:
                    fitness-=0

            if len(i)==4:
                if i in four_words:
                    fitness+=4
                else:
                    fitness-=0
           
        if max_len>25:
                
            fitness-=200
                        

        if "  " in new_message:
            fitness-=10
        
        fitness=max(fitness,1)

        
        
        self.fitness=fitness
        return fitness
        

    def get_fitness(self): 
            return self.fitness

    def get_key(self):
        return self.key

    def mate(self, other, crossover=None): # viene eseguito crossover classico 
        if crossover == None:
            crossover = random.randint(0, len(self.key) -1 )

        return [Individual(self.key[:crossover] + other.key[crossover:]),
                Individual(other.key[:crossover] + self.key[crossover:])]

    def mutate(self, mut_prob, rnd=None):
        if rnd == None:
            rnd = random.random()
        if rnd < mut_prob:
            pos = random.randint(0, len(self.key) -1 )
            self.key[pos] = random.choice(alphabet)#sostiuisce una lettera con una random
    

def generate_population(npop,lenght):
    
    return [Individual([random.choice(alphabet) for j in range (lenght)]) for i in range (npop)]

def weighted_sample(in_pop, in_scores, n):
    """
        Vengono scelti n elementi che non si ripetono dalla popolazione 
    """

    chosen = []

    pop = in_pop[:]
    scores = in_scores[:]

    for i in range(n):
        totscore = sum(scores)
        r = random.random()
        tot = 0
        j=0
        for s in scores:
            tot += s / float(totscore)
            if tot > r:
                break
            j+=1
        try:
            chosen.append(pop.pop(j))
        except IndexError: # se non si può rimuovere l'elemento viene restituito None 
            return None
        scores.pop(j)
        
    return chosen

def generate_new_population(pop,message):
    """
        Genera una nuova popolazione mantenendo l'individuo con fitness più alta.
        Non è stato implementato il metodo con i primi n individui perchè avrebbe richiesto un sort 
        con la fitness che avrebbe rallentato molto l'algoritmo.
    """
    new_pop = []
    new_pop.append(max(pop,key= lambda i: i.get_fitness())) #l'elemento con fitness massima della popolazione viene salvato nella nuova 
                                                            # popolazione 
    for i in range(int((len(pop)-1)/2)):
        parent1, parent2 = weighted_sample(pop, [ind.get_fitness() for ind in pop], 2) # scelgo gli individui 
        new_pop.extend(parent1.mate(parent2))
    
    return new_pop

def mutate_population(pop, mut_prob):

    new_pop = []
    for i in pop:
        i.mutate(mut_prob)
        new_pop.append(i)

    return new_pop

def match_key(key1,key2):
    """
    confronta due chiavi e restituisce quante lettere hanno in comune
    """
    app=0

    for i in range(len(key1)):
        if key1[i]==key2[i]:
            app+=1
    
    return app


#Carica il testo e lo sistema
text = open(file_name)
message = text.read()
text.close()
print("Testo nel file:\n")
print(message)
print()

if (key_true!=None):
    #codifico il testo
    message=txt_set(message) # se message è il messaggio criptato non va pulito perchè ha doppi spazi che andrebbero eliminati
    critt_message=crittografia.critt_Vigenere(message,key_true)
    print ("Testo criptato:\n")
    print(critt_message)
    print()
    Ind=Individual(list(key_true))
    Ind.set_fitness(critt_message)
    print("fitness soluzione: " ,Ind.get_fitness( ))

    # salvo il testo criptato nel file "cript_file.txt"

    name='cript_file.txt'  
    file = open(name,'w') 
    file.write(critt_message) 
    file.close() 


else:
    critt_message=message
    
# generazione popolazione

pop=generate_population(npop,len_key) 


for i in pop:
    # calcolo fitness
    i.set_fitness(critt_message)

# output sotto forma di tabella 

format_string = "{:^15}{:^30}{:^15}"
header=[f'#run','Key','fitness']
print()
print(format_string.format(*header))






for i in range (ngen):

    #generazione nuova popolazione     
    pop = generate_new_population(pop,critt_message )
       
    # mutazione     
    pop = mutate_population(pop, mut_prob)
    
    for k in pop:
        # calcolo fitness
        k.set_fitness(critt_message)


    


    if i%2==0:
        #cerco l'individuo con fitness massima 
             
        max_pop=max(pop, key= lambda i: i.get_fitness())
        
        print(format_string.format(*[f"{i} / {ngen} " , "".join(max_pop.get_key()) , max_pop.get_fitness() ]))

# Salvo dati su file 
file1 = open("develope.txt", "a")

if (key_true!=None):
            max_pop=max(pop, key= lambda i: i.get_fitness())
            file1.write(f"{match_key(key_true,max_pop.get_key())}")
            file1.write(f"\n")

print()
print ("Testo decrittato\n")
print( crittografia.decritt_Vigenere(critt_message,max_pop.get_key()))


