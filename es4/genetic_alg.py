from random import randint
import random
import crittografia 
import crossover
import argparse
import string
import numpy as np

#Prendo argomenti passati da comando
parser = argparse.ArgumentParser(description= "Programma di decrittazione tramite algoritmi genetici")
parser.add_argument('file_name', help="Inserire il nome del file da decrittare.Il file non deve contenere righe vuote (paragrafi)", type=str)
parser.add_argument('--ngen', help="numero di generazioni. Se omesso ngen = 200", type=int,default=200)
parser.add_argument('--mut_prob', help="probabilità di mutazione. Se omesso mut_prob = 0.1", type=float,default=0.1)
parser.add_argument('--npop', help="numero di individui nella popolazione. Se omesso npop = 80", type=int,default=80)

args = parser.parse_args()

file_name = args.file_name

ngen = args.ngen
mut_prob = args.mut_prob

len_max_key = 15
len_min_key=4
npop=args.npop

alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

#salva info frequenze 
#digraph e trigraph sono liste di liste (matrici): ad ogni riga corrispone una lista 
# di caratteri che formano una coppia o un tripletto di caratteri ferquenti

letters=open("letters.txt").read().split( )

digraphs= open("digraphs.txt").read().split() # viene letto il file, salvato con read() e separato in list di coppie con split()
                                                                
trigraphs= open("trigraphs.txt").read().split()

two_words=open("two_words.txt").read().split()

three_words=open("three_words.txt").read().split()

four_words=open("four_words.txt").read().split()

one_words= open("one_words.txt").read().split()

letters = np.loadtxt("letters_freq.txt", dtype=np.str, usecols=[0])
perc_letters = np.loadtxt("letters_freq.txt", dtype=np.float64, usecols=[1])

quadrigram=open("quadrigram.txt").read().split()


def txt_set(message):

    """
       elimina dal testo tutto ciò che non sono caratteri e rende tutte le lettere minuscole.
       Restituisce una lista
    """
    
    message_list=list(message.lower())
    new_message_list=[]
   
    for i,item in enumerate(message_list): 
        
        if item in alphabet:
          new_message_list.append(item)
           
    
    mess="".join(new_message_list)
    new_mess=mess.replace("  "," ")

    while new_message_list[-1]==" ":
        
        new_message_list.pop( )
    
    return new_mess


class Individual(list):# gli individui sono le chiavi 
    
    #la key è una lista     

    def __init__(self,key,decritt,fitness=None):
        '''
        se decritt = 0 si usa decritt_Vigenere()
        altrimenti si usa decritt_permutation()
        '''
        self.fitness=fitness
        self.key=key 
        self.decritt=decritt

    def set_fitness(self,message):
        
        fitness=0
        key=self.key

        if self.decritt==0:
            new_message=crittografia.decritt_Vigenere(message,"".join(key))
        else:
            new_message=crittografia.decritt_permutation(message,"".join(key))

        
        words = new_message.split(' ')
        max_len=len( max(words, key = lambda k: len(k)))
      
        
        if self.decritt!=0:
            for i, item in enumerate(quadrigram):
                fitness+=new_message.count(item)*1 

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
        if self.decritt!=0: 
            
            if max_len>25:
                
                fitness=1
                        

            if "  " in new_message:
                fitness=1
        
        
        fitness=max(fitness,1)

        self.fitness=fitness
        return fitness
        

    def get_fitness(self):
        return self.fitness

    def get_key(self):
        return self.key
    
    def get_decritt(self):
        return self.decritt

    def mate(self, other, cross=None):

        if self.decritt==0:
            if cross == None:
                cross = random.randint(0, len(self.key) -1 )

            return [Individual(self.key[:cross] + other.key[cross:],decritt=0),
                    Individual(other.key[:cross] + self.key[cross:],decritt=0)]

        else:
                       
            son1=crossover.cycle_crossover(self.key,other.key)
            son2=crossover.cycle_crossover(other.key,self.key)
            
            return Individual(son1,decritt=1),Individual(son2,decritt=1)


    def mutate(self, mut_prob, rnd=None):
        if rnd == None:
            rnd = random.random()
        if rnd < mut_prob:
            if self.decritt==0:
                pos = random.randint(0, len(self.key) -1 )
                self.key[pos] = random.choice(alphabet)#sostiuisce una lettera con una random
            
            else:
                pos1 = random.randint(0, len(self.key)-1 )
                pos2 = random.randint(0, len(self.key)-1 )
                self.key[pos1],self.key[pos2] = self.key[pos2], self.key[pos1]
    
        return None

def generate_sub_population(npop,lenght,critt_message):
    """
    npop=numero individui per singola sottopopolazione, lenght = lunghezza chiave.
    Viene restituita una sottopopolazione (liste di individui)
    """
    
    return [Individual([random.choice(alphabet) for j in range (lenght)],decritt=0) for i in range (npop)]

def generate_population(npop,critt_message):
    """
    npop=numero individui.
    Genera la sottopolazione della crittografia mono-alfabetica
    """
    # Aggiungo ' ' alla lista dei caratteri in ordine di frequenza 
    freq_letters=[' ']
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
        pop.append(Individual(new_alphabet,decritt=1))
    
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
        genera una nuova poplazione mantenendo l'individuo con fitness più alta.
        
    """
    new_pop = [[] for i in pop]
    sum_fit=[] # somma dei fit per ciascuna sottopopolazione 

    for i in pop:
        
        fit=[]
        for j in i:
            fit.append(j.get_fitness())
            
        sum_fit.append(sum(fit))

    if (pop[len(pop)-1][0].get_decritt!=0): # la somma dei fit della sotto-popolazione con permutazioni dell'alfabeto 
                                            #viene divisa per 2 altrimenti si ha valore troppo alto.
        sum_fit[len(pop)-1]/=2 
    
    for i in range(len(new_pop)):
        new_pop[i].append(max(pop[i],key= lambda i: i.get_fitness( ))) # salva l'elemento con maggiore fitness per qualsiasi sotto-popolazione 
    
    for i in range(int((npop*len(pop)-len(new_pop))/2)):

        choose=weighted_sample(pop,sum_fit,1)#viene scelta una sotto-popolazione sulla base della somme delle fitness 
        
        while(choose==None or len(choose[0])==1):
        
            choose=weighted_sample(pop,sum_fit,1)
        
        parent1, parent2 = weighted_sample(choose[0], [ind.get_fitness( ) for ind in choose[0]], 2)
        
        # viene fatta una suddivisione tra mono e poli-alfabetica per inserire le nuove sottopopolazioni
        #nel posto giusto
        if len(choose[0][0].get_key())==len(alphabet):
            
            new_pop[len_max_key-len_min_key+1].extend(parent1.mate(parent2))
        else:
            
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
critt_message = text.read()
text.close()


print("Testo nel file:\n")
print(critt_message)
print()

# generazione popolazione
print("generazione popolazione")
pop=[generate_sub_population(npop,i,critt_message) for i in range(len_min_key,len_max_key+1)]
pop1=generate_population(npop,critt_message)
pop.append(pop1)

#calcolo fitness

for i in pop:
    for j in i:
        j.set_fitness(critt_message)
        


max_pop_alf=max(pop[len(pop)-1],key= lambda i: i.get_fitness())# individuo con massimo fitness della sottopopolazione della permutazione alfabeto

for i in range (ngen):
    
    pop = generate_new_population(pop,critt_message )

    for j in pop:
        
        j = mutate_population(j, mut_prob)
        for k in j:
            k.set_fitness(critt_message)
    
    if (pop[len(pop)-1][0].get_decritt!=0): # nella sottopopolazione con algoritmo mono-alfabetico 
                                            # si sceglie l'individuo con fitness massima tra la nuova e la vecchia generazione e 
                                            #nel caso lo si inserisce nella nuova popolazione 

        max_pop1=max(pop[len(pop)-1],key= lambda i: i.get_fitness())
        
        if max_pop_alf.get_fitness()>max_pop1.get_fitness():# tra la generazione padre e la generazione figlio prende il migliore 
            pop[len(pop)-1].remove(pop[len(pop)-1][0])
            pop[len(pop)-1].append(max_pop)
        else:
            max_pop_alf=max_pop1
            
        
    if i%2==0:
        #cerco l'individuo con fitness massima 
        '''
        for k in pop:
            print(len(k[0].get_key()),"n. individui",len(k))
        '''
        max_list=[max(i,key= lambda i: i.get_fitness()) for i in pop] # lista di individui con maggiore fitness per ogni sottopopolazione
        max_pop=max(max_list, key= lambda i: i.get_fitness())
        print(f"{i} / {ngen} chiave con maggiore fitness:  ","".join(max_pop.get_key()),max_pop.get_fitness())


print()
print ("Testo decrittato\n")
if max_pop.get_decritt==0:
    print( crittografia.decritt_Vigenere(critt_message,max_pop.get_key()))
else:
    print( crittografia.decritt_permutation(critt_message,max_pop.get_key()))
