import argparse

alphabet=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',' ']

def critt_Vigenere(message,key):
    """
    message è una stringa e key una stringa senza spazi (parola)
    """
    message_list=list(message)
    new_message=[]
    key_list=list(key)
    nspace=0
    for i, item in enumerate(message):
        
        index_message_element=alphabet.index(item)
        index_key_element=alphabet.index(key_list[(i-nspace)%len(key_list)])
        new_message.append(alphabet[(index_key_element+index_message_element)%len(alphabet)])
                #prendo la lettera nel messaggio index_message_element la sommo alla lettera della chiave corrispondente index_key_element
                # togliendo gli spazi a cui non corrisponde elemento della chiave
            
    return "".join(new_message)

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
        else:
            if i<len(message_list)-1:
                
                if item!="'" and item!="’" and message_list[i+1]!=' ' : # l'apostrofo viene ignorato es Luigi's -> Luigis
                    new_message_list.append(' ')
    
    while new_message_list[-1]==" ":
        #print("we")
        new_message_list.pop( )
    
    mess="".join(new_message_list)
    new_mess=mess.replace("  "," ")

   
    print( new_message_list[-1])
    return new_mess


parser = argparse.ArgumentParser(description= "Programma di decrittazione tramite algoritmi genetici")
parser.add_argument('file_name', help="Inserire il nome del file da decrittare", type=str)
parser.add_argument('--key', help="chiave: se si passa l'argomento key il programma codifica tramite cifrario di Vigenere e tenta di decrittare il messaggio", type=str, default=None)



args = parser.parse_args()

file_name = args.file_name
key=args.key

text = open(file_name)
message = text.read()
text.close()
message=txt_set(message)
print("Testo nel file:\n")
print(message)
print()

critt_message=critt_Vigenere(message,key)
print ("Testo criptato:\n")
print(critt_message)
name='cript_file.txt'
file = open(name,'w') 
 
file.write(critt_message) 


 
file.close() 