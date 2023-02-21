from Intp import *
from node import *
from Thompson import *
ift = InfixToPostfix("a.(a|b)*.b")
result = ift.infix_to_postfix()
print(result)

instanceThompson = Thompson(result)
afnresult = instanceThompson.postfix_to_nfa()
afnresult.printAfn()










