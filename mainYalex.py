from Yalex import Yalex

yalexInstance = Yalex('ejemplo2.yal')
res = yalexInstance.getRegexes()

yalexInstance.simulacion_afd(res)