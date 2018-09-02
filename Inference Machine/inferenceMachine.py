from Reading import *
SPACE_SIZE = 3
class colors:
    yellow = "\033[93m"
    green = "\033[92m"
    red = "\033[91m"
    blue = "\033[96m"
    end = "\033[0m"

def buildGraph(rules):
    graph = {}
    for antecedent, consequent in rules:
        if (consequent not in graph): graph[consequent] = []
        graph[consequent] += [antecedent]
    return(graph)

def printResult(depth, result):
    print((depth)*" "*SPACE_SIZE, colors.green if result else colors.red, str(result), colors.end, sep='')

def bottomUp(graph, base, target, depth):
    print(depth*" "*SPACE_SIZE, colors.blue, target, colors.end, sep='')
    if (target in base):
        printResult(depth + 1, True)
        return(True)
    if (target not in graph):
        printResult(depth + 1, False)
        return(False)
    for rule in graph[target]:
        for element in rule:
            if (bottomUp(graph, base, element, depth + 1)):
                base.add(element)
            else: break
        else:
            printResult(depth + 1, True)
            return(True)
    printResult(depth + 1, False)
    return(False)

rules = readRules()
# print(rules)
base = readBase()
# print(base)
target = readTarget()
# print(target)

graph = buildGraph(rules)
print("\nGraph of Inference:", graph)
# printGraph(graph)
result = bottomUp(graph, base, target, 0)
print(end="Verdict: ")
printResult(0, result)