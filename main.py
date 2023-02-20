from Intp import *

ift = InfixToPostfix("a.a.(a|b)*.(b|a).b.b.b")
result = ift.infix_to_postfix()
print(result)

