from Yalex import *
from Yapar import *
#ejemplo4.yal
#yapa.yalp

#ejemplo5.yal
#yappa2.yalp

input1 = input("Ingrese el archivo yalex a analizar:  ")
input2 = input("Ingrese el archivo yapar a analizar:  ")
yapar = Yapar(input2)
yapar.compile()
yapar.crear_y_escribir_archivo("analizer.py",input1,input2)
