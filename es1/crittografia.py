alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

def critt_Cesare (message,key):
    """
        message è una stringa e key un numero intero che dice di quanto traslare
    """
    message_list=list(message)
    new_message=[]

    for i in message:
        if i==' ':
            new_message.append(' ')
        else:
            new_message.append(alphabet[(alphabet.index(i)+key)%len(alphabet)])
            # trovo la lettera in alphabet e traslo di quanto indicato da key
    return "".join(new_message)
    
def decritt_Cesare(message,key):
    return critt_Cesare(message,(-1)*key)
    # la decrittazione si ottiene riapplicando il metodo di Cesare ma con una trasalazione 
    # opposta 

def critt_permutation(message,key):
    """
        message è una stringa e key una permuatazione dell'alfabeto
    """
    message_list=list(message)
    new_message=[]

    for i in message_list:
        if i in alphabet:# trasforma solo i caratteri presenti nell'alfabeto
            new_message.append(key[alphabet.index(i)])
            # sostituisce la lettera dell'alfabeto con quella che si trova nella stessa 
            #posizione nella chiave
    return "".join(new_message)

def decritt_permutation(message,key):
    message_list=list(message)
    new_message=[]

    for i in message_list:
        #print(i)
        #print("prova",key.index(i))
        if i in alphabet:#trasforma solo i caratteri presenti nell'alfabeto
            try:
                new_message.append(alphabet[key.index(i)])#Rispetto alla funzione critt_permutation ho invertito alphabet <-> key
            except ValueError:
                print(i)
                print(key)
    return "".join(new_message)

def critt_Vigenere(message,key):
    """
    message è una stringa e key una stringa senza spazi (parola)
    """
    message_list=list(message)
    new_message=[]
    key_list=list(key)
    
    app=0
    for item in message:
        if item in alphabet:
            index_message_element=alphabet.index(item)
            index_key_element=alphabet.index(key_list[(app)%len(key_list)])
            new_message.append(alphabet[(index_key_element+index_message_element+1)%len(alphabet)])
            app+=1
            
        else:
            new_message.append(item)
            #print(item)
                #prendo la lettera nel messaggio index_message_element la sommo alla lettera della chiave corrispondente index_key_element
                # togliendo gli spazi a cui non corrisponde elemento della chiave
                
    return "".join(new_message)

def decritt_Vigenere(message,key):
    """
    message è una stringa e key una stringa senza spazi (parola)
    """
    message_list=list(message)
    new_message=[]
    key_list=list(key)
    nspace=0
    app=0
    for i, item in enumerate(message):
        
        if item in alphabet:
            index_message_element=alphabet.index(item)
            index_key_element=alphabet.index(key_list[(app-nspace)%len(key_list)])
            
            new_message.append(alphabet[(index_message_element-index_key_element-1)%len(alphabet)])
            app+=1
        else:
            new_message.append(item)
           #prendo la lettera nel messaggio index_message_element la sottraggo alla lettera della chiave corrispondente index_key_element
           # togliendo gli spazi a cui non corrisponde elemento della chiave
            
    return "".join(new_message)
