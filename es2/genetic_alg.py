from random import randint
import random
import crittografia 
import argparse
import crossover
import string
import multiprocessing
import numpy as np
import math 
#Prendo argomenti passati da comando

parser = argparse.ArgumentParser(description= "Programma di decrittazione tramite algoritmi genetici")
parser.add_argument('file_name', help="Inserire il nome del file da decrittare. Il file non deve contenere righe vuote (paragrafi)", type=str) 
parser.add_argument('--ngen', help="numero di generazioni. Se omesso ngen = 200", type=int,default=200)
parser.add_argument('--mut_prob', help="probabilità di mutazione. Se omesso mut_prob = 0.1", type=float,default=0.1)
parser.add_argument('--npop', help="numero di individui nella popolazione. Se omesso npop = 1100", type=int,default=1100)
parser.add_argument('--crypt', help="se True cripta il testo con una permutazione dell'alfabeto scelta dal programma. Se omesso crypt = False", type=bool, default=False)

args = parser.parse_args()

file_name = args.file_name
ngen = args.ngen
mut_prob = args.mut_prob
crypt=args.crypt
remain=5
npop=args.npop
alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

#salva info frequenze 
#digraph e trigraph sono liste di liste (matrici): ad ogni riga corrispone una lista 
# di caratteri che formano una coppia o un tripletto di caratteri ferquenti


digraphs= open("digraphs.txt").read().split() # viene letto il file, salvato con read() e separato in list di coppie con split()
                                                                
trigraphs= open("trigraphs.txt").read().split()

quadrigram=open("quadrigram.txt").read().split()

one_words= open("one_words.txt").read().split()

two_words=open("two_words.txt").read().split()

three_words=open("three_words.txt").read().split()

four_words=open("four_words.txt").read().split()

letters = np.loadtxt("letters_freq.txt", dtype=np.str, usecols=[0])
perc_letters = np.loadtxt("letters_freq.txt", dtype=np.float64, usecols=[1])

def txt_set(message):
    """
       elimina dal testo tutto ciò che non sono caratteri e rende tutte le lettere minuscole.
       Restituisce una lista
    """
    message_list=list(message.lower())
    new_message_list=[]
    
    for i,item in enumerate(message_list): # devo usare liste perchè stringhe immuatbili
        
        if item in alphabet:
          new_message_list.append(item)
        
    while new_message_list[-1]==" ": # elimina gli spazi alla fine del testo
        new_message_list.pop( )
    
    mess="".join(new_message_list)
    new_mess=mess.replace("  "," ")

   
    
    
    return new_mess
    

class Individual(list):
    """
    Individual sono le permutazioni dell'alfabeto
    """
    
    def __init__(self,key,fitness=None): # la fitness è inizializzata a None 
        
        self.fitness=fitness
        self.key=key
    
    def set_fitness(self,message):
        
        fitness=0
        
        key=self.key
        new_message=crittografia.decritt_permutation(message,"".join(key)) # decritto il messaggio
       
        words = new_message.split(' ')
        
        max_len=len( max(words, key = lambda k: len(k)))
         
        # le chiavi che danno parole con lunghezza superiore a 25 lettere oppure contengono 
        # "  " nel testo decrittato

        if max_len>25 or "  " in new_message: 
            
            fitness=1
            self.fitness=fitness
            return fitness

        
       
        

        for i,item in enumerate(digraphs):
            fitness+=new_message.count(item)*1
        
        for i,item in enumerate(trigraphs):
            fitness+=new_message.count(item)*1
        
        for i, item in enumerate(quadrigram):
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
                    fitness-=-1

            if len(i)==3:
                if i in three_words:
                   fitness+=2
                else:
                    fitness-=-1

            if len(i)==4:
                if i in four_words:
                    fitness+=4
                else:
                    fitness-=0
           
        
            
            
        self.fitness=fitness
        return fitness

    def get_fitness(self):
            return self.fitness

    def get_key(self):
        return self.key

    def mate(self,other):

            # viene usato il cycle crossover 

            son1=crossover.cycle_crossover (self.key,other.key)
            son2=crossover.cycle_crossover (other.key,self.key)
            
            return Individual(son1),Individual(son2)

    def mutate(self, mut_prob, rnd=None): 
        """
            scambia due elementi della chiave 

        """
        if rnd == None:
            rnd = random.random()
        if rnd < mut_prob:
            pos1 = random.randint(0, len(self.key)-1 )

            pos2 = random.randint(0, len(self.key)-1 )
            self.key[pos1],self.key[pos2] = self.key[pos2], self.key[pos1]
        
        return None
    
def max_word_legth(message):
    """
    trova la parola con lunghezza maggiore 
    """
    
    
    words = message.split(' ')
    max_len=len( max(words, key = lambda k: len(k)))
               
    return max_len

def generate_population(npop,critt_message):
    """
    npop=numero individui
    """
    # Aggiungo ' ' alla lista dei caratteri in ordine di frequenza 
    
    freq_letters=[' '] #caratteri in ordine di frequenza in inglese 
    for i in letters:
        freq_letters.append(i)

    freq_message=[critt_message.count(i) for i in alphabet]# frequenza delle lettere nel testo criptato
    
    freq_letters_cript=[] # list in ordine di frequenza dei simboli che compaiono di più nel critt_message 
    for i in freq_message:
        m=max(freq_message)
        freq_letters_cript.append( alphabet[freq_message.index(m)])
        freq_message[freq_message.index(m)]=-1
    
    pop=[]
    new_alphabet=[]
    for i in range (npop):
        '''
        La popolazione è costituita da individui che si ottengono scambiando di un posto due elementi 
        di freq_letters_list[] e da individui che si ottengono facendo permutazioni tra posti vicini senza
        poi riportare freq_letters_list al suo stato iniziale 
        '''
        r=random.randint(0,len(freq_letters_cript)-2)
        
        freq_letters_cript [r], freq_letters_cript [r+1]=  freq_letters_cript [r+1],freq_letters_cript [r] #scambio due lettere vicine 
        new_alphabet=[freq_letters_cript[ freq_letters.index(i)] for i in alphabet]
        if i<len(alphabet):
            freq_letters_cript [r+1],freq_letters_cript [r] =   freq_letters_cript [r], freq_letters_cript [r+1]
        pop.append(Individual(new_alphabet))
   
    return pop

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
        for j, s in enumerate(scores):
            tot += s / float(totscore)
            if tot > r:
                break
        
        chosen.append(pop.pop(j))
        scores.pop(j)

    return chosen

def generate_new_population(pop,message,remain):
    """
        genera una nuova popolazione mantenendo l'individuo con fitness più alta.
        "remain" è il numero di individui con fitness maggiore che rimangono nella nuova 
        generazione
    """
    

    new_pop = []
    pop.sort(key = lambda i: i.get_fitness(),reverse=True)
    
    for i in range(remain):
        new_pop.append(pop[i])
    for i in range(int((len(pop)-remain)/2)):
        
        parent1, parent2 = weighted_sample(pop, [ind.get_fitness() for ind in pop], 2)
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

#Carica il testo
text = open(file_name)
message = text.read()
text.close()

print()
print("Testo nel file:\n")
print(message)
print()

if (crypt):
    #codifico il testo con chiave scelta random

    message=txt_set(message)  # se message è il messaggio criptato non va pulito perchè ha doppi spazi che andrebbero eliminati
    new_alphabet=[i for i in alphabet]
    random.shuffle(new_alphabet)
    
    cript_key=[i for i in new_alphabet]

    print("chiave",cript_key)
    critt_message=crittografia.critt_permutation(message,cript_key)
    print()
    print ("Testo criptato:\n")
    print(critt_message)
    print()

    Ind=Individual(cript_key)
    Ind.set_fitness(critt_message)
    
    print("fitness soluzione: " ,Ind.get_fitness())
    print()
    # salvo il testo criptato nel file "cript_file.txt"

    name='cript_file.txt'  
    file = open(name,'w') 
    file.write(critt_message) 
    file.close() 

else:
    critt_message=message




pop=generate_population(npop,critt_message)

for i in pop:
    # calcolo fitness
    i.set_fitness(critt_message)



# output sotto forma di tabella 
if (crypt):
    format_string = "{:^15}{:^30}{:^15}{:^5}"
    header=[f'#run','Key','fitness','match']
else:
    format_string = "{:^15}{:^30}{:^15}"
    header=[f'#run','Key','fitness']

print(format_string.format(*header))

max_pop=max(pop,key= lambda i: i.get_fitness())

# salvataggio dati nel file 
file1 = open("develope.txt", "a")

for i in range (ngen):
   
    pop = generate_new_population(pop,critt_message,remain)
    
    pop = mutate_population(pop, mut_prob)

    for j in pop:
        # calcolo fitness
        j.set_fitness(critt_message)

    max_pop1=max(pop,key= lambda i: i.get_fitness())

   
    if max_pop.get_fitness()>max_pop1.get_fitness():# tra la generazione padre e la generazione figlio prende il migliore 
        
        pop.remove(pop[0])
        pop.append(max_pop)
    else:
        max_pop=max_pop1

    if crypt:
        
        max_pop=max(pop, key= lambda i: i.get_fitness())

        file1.write(f"{i} {max_pop.get_fitness()} {Ind.get_fitness( )} {match_key(cript_key,max_pop.get_key())} ")
        file1.write(f"\n")
    
    if i%2==0:
        max_pop=max(pop,key= lambda i: i.get_fitness())
        
        if (crypt):
            print(format_string.format(*[f"{i} / {ngen} " , "".join(max_pop.get_key()) , max_pop.get_fitness() , match_key(cript_key,max_pop.get_key())]))
        else:
             print(format_string.format(*[f"{i} / {ngen} " , "".join(max_pop.get_key()) , max_pop.get_fitness() ]))
    


max_pop=max(pop,key= lambda i: i.get_fitness())
print()
print(f"{ngen} / {ngen} chiave con maggiore fitness:  ","".join(max_pop),max_pop.get_fitness())
print()

print ("Testo decrittato\n")
print( crittografia.decritt_permutation(critt_message,max_pop.get_key()))

