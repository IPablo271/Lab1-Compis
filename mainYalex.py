from Yalex import Yalex

yalexInstance = Yalex('ejemplo3.yal')
res = yalexInstance.getRegexes()

yalexInstance.simulacion_afd(res)