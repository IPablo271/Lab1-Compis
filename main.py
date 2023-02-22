from Intp import *
from node import *
from Thompson import *



ift = InfixToPostfix("a(b*|a)b?c+(a|b)*")
ift.formatearExpresionRegular()

print(ift.expression)

result = ift.infix_to_postfix()
print(result)

instanceThompson = Thompson(result)

afnresult = instanceThompson.postfix_to_nfa()
afnresult.transicionesToNum()
afnresult.printAfn()


print("  ")
print(afnresult.transicionesNum)
afnresult.draw_graph()












