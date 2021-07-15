from random import randint
import random
import crittografia 
import argparse
import string

#Prendo argomenti passati da comando
parser = argparse.ArgumentParser(description= "Programma di decrittazione tramite algoritmi genetici")
parser.add_argument('file_name', help="Inserire il nome del file da decrittare.Il file non deve contenere righe vuote (paragrafi)", type=str)
parser.add_argument('--ngen', help="numero di generazioni. Se omesso ngen = 200", type=int,default=200)
parser.add_argument('--mut_prob', help="probabilità di mutazione. Se omesso mut_prob = 0.1", type=float,default=0.1)
parser.add_argument('--npop', help="numero di individui nella popolazione. Se omesso npop = 100", type=int,default=100)
parser.add_argument('--key', help="chiave: se si passa l'argomento key il programma codifica tramite cifrario di Vigenere e tenta di decrittare il messaggio", type=str, default=None)

args = parser.parse_args()

file_name = args.file_name

ngen = args.ngen
mut_prob = args.mut_prob
key_true=args.key
len_max_key = 15
len_min_key=4
npop=args.npop

alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

#salva info frequenze 


digraphs= open("digraphs.txt").read().split() # viene letto il file, salvato con read() e separato in list di coppie con split()
                                                                
trigraphs= open("trigraphs.txt").read().split()

two_words=open("two_words.txt").read().split()

three_words=open("three_words.txt").read().split()

four_words=open("four_words.txt").read().split()

one_words= open("one_words.txt").read().split()



def txt_set(message):
    """
       elimina dal testo tutto ciò che non sono caratteri presenti nell'alfabeto e rende tutte le lettere minuscole.
       Restituisce una stringa.
    """
    message_list=list(message.lower())
    new_message_list=[]
   
    for i,item in enumerate(message_list): # devo usare liste perchè stringhe immuatbili
        
        if item in alphabet:
          new_message_list.append(item)
            
    mess="".join(new_message_list)
    new_mess=mess.replace("  "," ")

    while new_message_list[-1]==" ":  # elimina gli spazi alla fine del testo
        
        new_message_list.pop( )
    
    return new_mess


class Individual(list):
     

    def __init__(self,key,fitness=None): # la fitness è inizializzata a None 
        
        self.fitness=fitness
        self.key=key 

    def set_fitness(self,message):
        
        fitness=0
        key=self.key
        new_message=crittografia.decritt_Vigenere(message,"".join(key)) #decrittazione
        
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
                    fitness-=2

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

    def mate(self, other, crossover=None):
        if crossover == None:
            crossover = random.randint(0, len(self.key) -1 )

        return [Individual(self.key[:crossover] + other.key[crossover:]),
                Individual(other.key[:crossover] + self.key[crossover:])]

    def mutate(self, mut_prob, rnd=None):
        if rnd == None:
            rnd = random.random()
        if rnd < mut_prob:
            pos = random.randint(0, len(self.key) -1 )
            self.key[pos] = random.choice(alphabet) #sostiuisce una lettera con una random
    

def generate_population(npop,lenght,critt_message):
    """
    npop=numero individui per singola sottopopolazione, lenght = lunghezza chiave.
    Viene restituita una sottopopolazione (lista di individui)
    """
    
    return [Individual([random.choice(alphabet) for j in range (lenght)]) for i in range (npop)]

def weighted_sample(in_pop, in_scores, n):
    """
        Vengono scelti n elementi dalla popolazione che non si ripetono 
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
        genera una nuova poplazione mantenendo l'individuo con fitness più alta per ogni sotto-popolazione.
        
    """
    new_pop = [[] for i in pop]
    sum_fit=[] # somma dei fit per ciascuna sottopopolazione 

    for i in pop:
                
        fit=[]
        for j in i:
            fit.append(j.get_fitness())
          
        sum_fit.append(sum(fit))
        
    
    for i in range(len(new_pop)):
        new_pop[i].append(max(pop[i],key= lambda i: i.get_fitness( ))) # salva l'elemento con maggiore fitness per qualsiasi sotto-popolazione 
    
    for i in range(int((npop*(len_max_key-len_min_key)-len(new_pop))/2)):

        choose=weighted_sample(pop,sum_fit,1)#viene scelta una sotto-popolazione sulla base della somme delle fitness 
        
        while(choose==None or len(choose[0])==1): # se la scelta ricade su una sottopopolazione con un solo elemento ne sceglie un'altra
            
            choose=weighted_sample(pop,sum_fit,1)
       
        parent1, parent2 = weighted_sample(choose[0], [ind.get_fitness( ) for ind in choose[0]], 2)
        
        new_pop[len(choose[0][0].get_key())-len_min_key].extend(parent1.mate(parent2))
       
    

    return new_pop


def mutate_population(pop, mut_prob):

    new_pop = []
    for i in pop:
        i.mutate(mut_prob)
        new_pop.append(i)

    return new_pop




#Carica il testo
text = open(file_name)
message = text.read()
text.close()

print("Testo nel file:\n")
print(message)
print()

if (key_true!=None):
    #codifico il testo
    message=txt_set(message)
    critt_message=crittografia.critt_Vigenere(message,key_true)
    
    print ("Testo criptato:\n")
    print(critt_message)
    print()
    
    Ind=Individual(list(key_true))
    Ind.set_fitness(critt_message)
    
    print("fitness soluzione: " ,Ind.get_fitness( ))
    
    name='cript_file.txt'  
    file = open(name,'w') 
    
    file.write(critt_message) 

    file.close() 


else:
    critt_message=message
    

pop=[generate_population(npop,i,critt_message) for i in range(len_min_key,len_max_key+1)]


for i in pop:

    for j in i:
        j.set_fitness(critt_message)



#calcolo fitness

# output sotto forma di tabella 

format_string = "{:^15}{:^30}{:^15}"
header=[f'#run','Key','fitness']

print(format_string.format(*header))

for i in range (ngen):
    
    pop = generate_new_population(pop,critt_message )

    for j in pop:
        
        j = mutate_population(j, mut_prob)
        for k in j:
            k.set_fitness(critt_message)
    
    if i%2==0:
        '''     
        for k in pop:
            print(len(k[0].get_key()),"n. individui",len(k))
        '''
        #cerco l'individuo con fitness massima 
        
        max_list=[max(i,key= lambda i: i.get_fitness()) for i in pop] # lista di individui con maggiore fitness per ogni sottopopolazione
        max_pop=max(max_list, key= lambda i: i.get_fitness()) # individuo con maggiore fitness
       
        print(format_string.format(*[f"{i} / {ngen} " , "".join(max_pop.get_key()) , max_pop.get_fitness() ]))

print()
print ("Testo decrittato\n")
print( crittografia.decritt_Vigenere(critt_message,max_pop.get_key()))
