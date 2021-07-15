import crittografia

text="l'apostrofo rosa"
tt=crittografia.critt_Vigenere(text,"casa")
print(tt)
print(crittografia.decritt_Vigenere(tt,"casa"))