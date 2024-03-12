from cmu_112_graphics import *
from dataclasses import make_dataclass
import random, string, math, time

def appStarted(app):
    app.display = [] #what the user sees themself input in the calculator
    app.equation = []
    app.functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'x', '', ''] #display
    app.signs = ['+', '-', '*', '÷', '**', '(', ')', 'back', 'clear', 'evaluate'] #display
    app.trig = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']
    app.rules = set()
    app.welcome = True
    app.calculator = False
    app.power = False
    app.product = False
    app.quotient = False
    app.chain = False
    app.rule = False
    app.calculate = False
    app.easy = True
    app.medium = False
    app.hard = False
    app.powerProblem = findPowerProblem(app)
    app.productProblem = findProductProblem(app)
    app.quotientProblem = findQuotientProblem(app)
    app.chainProblem = findChainProblem(app)
    app.showAnswer = False

def welcome(app, x, y):
    if start(app, x, y):
        app.welcome = False
        app.calculator = True

def calculator(app, x, y):
    selection = getKeyIndex(app, x, y)
    if whichRule(app, x, y) == 'Power Rule':
        app.calculator = False
        app.power = True
        app.rule = True
    elif whichRule(app, x, y) == 'Product Rule':
        app.calculator = False
        app.product = True
        app.rule = True
    elif whichRule(app, x, y) == 'Quotient Rule':
        app.calculator = False
        app.quotient = True
        app.rule = True
    elif whichRule(app, x, y) == 'Chain Rule':
        app.calculator = False
        app.chain = True
        app.rule = True
    if selection != None:
        typing(app, x, y)

def clear(app, x, y):
    app.display = [] #what the user sees themself input in the calculator
    app.equation = [] 
    app.functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log', 'x', '', ''] #display
    app.signs = ['+', '-', '*', '÷', '**', '(', ')', 'back', 'clear', 'evaluate'] #display
    app.trig = ['sin', 'cos', 'tan', 'csc', 'sec', 'cot']
    app.rules = set()
    app.welcome = False
    app.calculator = True
    app.calculate = False
    app.powerProblem = findPowerProblem(app)
    app.productProblem = findProductProblem(app)
    app.quotientProblem = findQuotientProblem(app)
    app.chainProblem = findChainProblem(app)
    app.showAnswer = False
    app.easy = True
    app.medium = False
    app.hard = False

def typing(app, x, y):
    selection = getKeyIndex(app, x, y)
    if selection == 'back': #back button
        if app.display != []:
            app.display.pop()
            app.equation.pop()
    elif selection == 'clear':
        clear(app, x, y)
    elif (selection == 'evaluate'): #we want to know the derivative
        makeNumbers(app, app.equation)
        makeMultiplication(app, app.equation)
        findNested(app, app.equation)
        nestNegatives(app, app.equation)
        analyzeDisplay(app, app.equation)
        #to guarantee only one operator in each list
        nestTrig(app, app.equation)
        nestLog(app, app.equation)
        nestExponents(app, app.equation)
        nestMultiplication(app, app.equation)
        nestDivision(app, app.equation)
        nestAddition(app, app.equation)
        nestSubtraction(app, app.equation)
        app.calculate = True #whether or not we display the derivative
    else:
        app.equation.append(str(selection))
        app.display.append(selection)

def changingLevels(app, x, y):
    if level(app, x, y) == 'Easy':
        app.easy = True
        app.medium = False
        app.hard = False
        app.powerProblem = findPowerProblem(app)
        app.productProblem = findProductProblem(app)
        app.quotientProblem = findQuotientProblem(app)
        app.chainProblem = findChainProblem(app)
        app.showAnswer = False
    elif level(app, x, y) == 'Medium':
        app.easy = False
        app.medium = True
        app.hard = False
        app.powerProblem = findPowerProblem(app)
        app.productProblem = findProductProblem(app)
        app.quotientProblem = findQuotientProblem(app)
        app.chainProblem = findChainProblem(app)
        app.showAnswer = False
    elif level(app, x, y) == 'Hard':
        app.easy = False
        app.medium = False
        app.hard = True
        app.powerProblem = findPowerProblem(app)
        app.productProblem = findProductProblem(app)
        app.quotientProblem = findQuotientProblem(app)
        app.chainProblem = findChainProblem(app)
        app.showAnswer = False

def rule(app, x, y):
    if back(app, x, y):
        app.rule = False
        app.calculator = True
        app.showAnswer = False
        app.easy = True
        app.medium = False
        app.hard = False
        if app.power:
            app.power = False
        elif app.product:
            app.product = False
        elif app.quotient:
            app.quotient = False
        elif app.chain:
            app.chain = False
    elif inNewProblem(app, x, y):
        app.powerProblem = findPowerProblem(app)
        app.productProblem = findProductProblem(app)
        app.quotientProblem = findQuotientProblem(app)
        app.chainProblem = findChainProblem(app)
        app.showAnswer = False
    elif inShowAnswer(app, x, y):
        app.showAnswer = not app.showAnswer
    if level(app, x, y) != None:
        changingLevels(app, x, y)

def mousePressed(app, event):
    x, y = event.x, event.y
    selection = getKeyIndex(app, x, y)
    if app.welcome:
        welcome(app, x, y)
    elif app.calculator:
        calculator(app, x, y)
    elif app.rule:
        rule(app, x, y)
    if selection == 'evaluate':
        print(app.equation)
        print(derivative(app, app.equation))

#[3, 3] --> [33]
def makeNumbers(app, equation):
    i = 0
    while i < len(equation) - 1:
        if equation[i].isnumeric():
            if equation[i + 1].isnumeric():
                equation[i] = equation[i] + equation[i + 1]
                equation.pop(i + 1)
                i -= 1
        i += 1
    return equation

#[4, x, **, 2] --> [4, *, x, **, 2]
#[(, 5, x, ), (, 5, x, +, 1, )] --> [(, 5, x, ), *, (, 5, x, +, 1, )]
def makeMultiplication(app, equation):
    i = 0
    while i < len(equation) - 1:
        if equation[i].isnumeric():
            if not equation[i + 1].isnumeric() and equation[i + 1] not in ['+', '-', '*', '÷', ')']:
                equation.insert(i + 1, '*')
        elif equation[i] == ')':
            if equation[i + 1] == '(' or equation[i + 1] not in ['+', '-', '*', '÷', '**', ')']:
                equation.insert(i + 1, '*')
        i += 1
    return equation

#returns a list tuples corresponding to the opening and closing parenthesis indexes.
def findIndexes(app, equation):
    leftIndex = 0
    stack = []
    indexes = []
    for i in range(len(equation)):
        if equation[i] == '(':
            stack.append(i)
        elif equation[i] == ')':
            if len(stack) > 1:
                pass
            else:
                indexes.append((stack[0], i))
            stack.pop()
    return indexes

#slices the equation to include lists for the terms in parenthesis
def findEquation(app, equation, leftIndex, rightIndex):
    lst = equation[leftIndex + 1: rightIndex]
    equation[leftIndex] = lst
    equation[leftIndex + 1 :] = equation[rightIndex + 1:]
    return equation

#accounts for multiple sets of parenthesis
def findMultiple(app, equation):
    indexes = findIndexes(app, equation)
    if indexes == []:
        return equation
    else:
        leftIndex = indexes[0][0]
        rightIndex = indexes[0][1]
        equation = findEquation(app, equation, leftIndex, rightIndex)
        if '(' in equation:
            equation = findMultiple(app, equation)
        return equation

#accounts for nested sets of parenthesis
def findNested(app, equation):
    equation = findMultiple(app, equation)
    indexes = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indexes.append(i)
    for i in indexes:
        equation[i] = findNested(app, equation[i])
    return equation

#accounts for negative numbers
def findNegatives(app, equation):
    if equation[0] != '-':
        return equation
    else:
        equation.insert(0, '0')
        return equation

#accounts for nested negative numbers
def nestNegatives(app, equation):
    equation = findNegatives(app, equation)
    indexes = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indexes.append(i)
    for i in indexes:
        equation[i] = nestNegatives(app, equation[i])
    return equation

#T in PTEMDAS
def groupTrig(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] in app.trig:
            lst = equation[i : i + 2]
            equation[i] = lst
            equation[i + 1 :] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

#accounts for nesting
def nestTrig(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestTrig(app, equation[index])
    return groupTrig(app, equation)

def groupLog(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == 'log':
            lst = equation[i : i + 2]
            equation[i] = lst
            equation[i + 1 :] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestLog(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestLog(app, equation[index])
    return groupLog(app, equation)

def groupExponents(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == '**':
            lst = equation[i - 1 : i + 2]
            equation[i - 1] = lst
            equation[i:] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestExponents(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestExponents(app, equation[index])
    return groupExponents(app, equation)

def groupMultiplication(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == '*':
            lst = equation[i -1 : i + 2]
            equation[i - 1] = lst
            equation[i:] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestMultiplication(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestMultiplication(app, equation[index])
    return groupMultiplication(app, equation)

def groupDivision(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == '/':
            lst = equation[i - 1 : i + 2]
            equation[i - 1] = lst
            equation[i:] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestDivision(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestDivision(app, equation[index])
    return groupDivision(app, equation)

def groupAddition(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == '+':
            lst = equation[i -1 : i + 2]
            equation[i - 1] = lst
            equation[i:] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestAddition(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestAddition(app, equation[index])
    return groupAddition(app, equation)

def groupSubtraction(app, equation):
    i = 0
    while i < len(equation):
        if i < len(equation) - 1 and equation[i] == '-':
            lst = equation[i -1 : i + 2]
            equation[i - 1] = lst
            equation[i:] = equation[i + 2 :]
            i -= 1
        i += 1
    return equation

def nestSubtraction(app, equation):
    i = 0
    indicies = []
    for i in range(len(equation)):
        if isinstance(equation[i], list):
            indicies.append(i)
    for index in indicies:
        equation[index] = nestSubtraction(app, equation[index])
    return groupSubtraction(app, equation)

#call on app.equation
#determines which rules were used
def analyzeDisplay(app, equation):
    if equation == []:
        return
    for term in equation:
        if term == '**':
            app.rules.add('Power Rule')
        if term == '*':
            app.rules.add('Product Rule')
        if term == '÷':
            app.rules.add('Quotient Rule')
        if isinstance(term, list):
            app.rules.add('Chain Rule')
            analyzeDisplay(app, term)

#finds the derivative
def derivative(app, term):
    if not isinstance(term, list):
        if term == 'x':
            return '1'
        else:
            return '0'
    if len(term) == 1:
        return [derivative(app, term[0])]
    if len(term) == 3:
        if term[1] == '+':
            left = derivative(app, term[0])
            right = derivative(app, term[2])
            if left == '0':
                return right
            elif right == '0':
                return left
            return [left, '+', right]
        elif term[1] == '-':
            left = derivative(app, term[0])
            right = derivative(app, term[2])
            if left == '0':
                return ['0', '-', right]
            elif right == '0':
                return left
            return [left, '-', right]
        elif term[1] == '*':
            left = term[0]
            dright = derivative(app, term[2])
            right = term[2]
            dleft = derivative(app, term[0])
            if (dright == '0' and dleft == '0') or (dright == '0' and right == '0') or (left == '0' and dleft == '0') or (right == '0' and left == '0'):
                return '0'
            if left == '0' or dright == '0':
                if not isinstance(right, list) and not isinstance(dleft, list) and right.isnumeric and dleft.isnumeric:
                    return str(int(right) * int(dleft))
                return [right, '*', dleft]
            if right == '0' or dleft == '0':
                if not isinstance(left, list) and not isinstance(dright, list) and left.isnumeric and dright.isnumeric:
                    return str(int(left) * int(dright))
                return [left, '*', dright]
            return [[left, '*', dright], '+', [right, '*', dleft]]
        elif term[1] == '÷':
            high = term[0]
            dhigh = derivative(app, high)
            low = term[2]
            dlow = derivative(app, low)
            return [[[low, '*', dhigh], '-', [high, '*', dlow]], '÷', [low, '*', low]]
        elif term[1] == '**':
            function = term[0]
            exponent = term[2]
            if not isinstance(derivative(app, function), list) and derivative(app, function).isnumeric:
                if str(int(exponent) - 1) == '1':
                    return [str(int(exponent) * int(derivative(app, function))), '*', function]
                return [str(int(exponent) * int(derivative(app, function))), '*', [function, '**', str(int(exponent) - 1)]]
            return [[exponent, '*', derivative(app, function)], '*', [function, '**', str(int(exponent) - 1)]]
    outside = term[0]
    inside = term[1]
    if outside == 'sin':
        if derivative(app, inside) == ['1']:
            return ['cos', inside]
        return [derivative(app, inside), '*', ['cos', inside]]
    if outside == 'cos':
        if derivative(app, inside) == ['1']:
            return [0, '-', ['sin', inside]]
        return [derivative(app, inside), '*', [0, '-', ['sin', inside]]]
    if outside == 'tan':
        if derivative(app, inside) == ['1']:
            return [['sec', inside], '*', ['sec', inside]]
        return [derivative(app, inside), '*', [['sec', inside], '*', ['sec', inside]]]
    if outside == 'csc':
        if derivative(app, inside) == ['1']:
            return [0, '-', [['csc', inside], '*', ['cot', inside]]]
        return [derivative(app, inside), '*', [0, '-', [['csc', inside], '*', ['cot', inside]]]]
    if outside == 'sec':
        if derivative(app, inside) == ['1']:
            return [['sec', inside], '*', ['tan', inside]]
        return [derivative(app, inside), '*', [['sec', inside], '*', ['tan', inside]]]
    if outside == 'cot':
        if derivative(app, inside) == ['1']:
            return [0, '-', [['csc', inside], '*', ['csc', inside]]]
        return [derivative(app, inside), '*', [0, '-', [['csc', inside], '*', ['csc', inside]]]]
    if outside == 'log':
        return [derivative(app, inside), '÷', inside]

#from: https://www.cs.cmu.edu/~112/notes/notes-graphics.html#customColors
def rgbString(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def redrawAll(app, canvas):
    drawBackground(app, canvas)
    if app.welcome:
        drawWelcome(app, canvas)
    elif app.calculator:
        powerRule(app, canvas)
        productRule(app, canvas)
        quotientRule(app, canvas)
        chainRule(app, canvas)
        drawNumbers(app, canvas)
        drawEquation(app, canvas)
        if app.calculate == True:
            drawDerivative(app, canvas)
            drawRules(app, canvas)
    elif app.power:
        drawPower(app, canvas)
        drawLevels(app, canvas)
        drawPowerProblem(app, canvas)
        drawNewProblem(app, canvas)
        drawShowAnswer(app, canvas)
    elif app.product:
        drawProduct(app, canvas)
        drawLevels(app, canvas)
        drawProductProblem(app, canvas)
        drawNewProblem(app, canvas)
        drawShowAnswer(app, canvas)
    elif app.quotient:
        drawQuotient(app, canvas)
        drawLevels(app, canvas)
        drawQuotientProblem(app, canvas)
        drawNewProblem(app, canvas)
        drawShowAnswer(app, canvas)
    elif app.chain:
        drawChain(app, canvas)
        drawLevels(app, canvas)
        drawChainProblem(app, canvas)
        drawNewProblem(app, canvas)
        drawShowAnswer(app, canvas)

#draws the new problem button
def drawNewProblem(app, canvas):
    canvas.create_rectangle(app.width/16, 7*app.height/16, 3*app.width/16, 9*app.height/16, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/16, app.height/2, text='New\nProblem')

#determines if the user wants a new problem
def inNewProblem(app, x, y):
    return x > app.width/16 and y > 7*app.height/16 and x < 3*app.width/16 and y < 9*app.height/16

#draws the show answer button
def drawShowAnswer(app, canvas):
    canvas.create_rectangle(app.width/16, 11*app.height/18, 3*app.width/16, 13*app.height/18, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/16, 2*app.height/3, text='Show\nAnswer')

#determines if the user wants to see the answer
def inShowAnswer(app, x, y):
    return x > app.width/16 and y > 11*app.height/18 and x < 3*app.width/16 and y < 13*app.height/18

#determines if the user clicked the back button
def back(app, x, y):
    return x > app.width/48 and y > app.height/48 and x < 5*app.width/48 and y < 5*app.height/48

def drawLevels(app, canvas):
    if app.easy:
        outline = rgbString(255, 168, 214)
    else:
        outline = 'black'
    canvas.create_rectangle(13*app.width/48, app.height/48, 19*app.width/48, 5*app.height/48, fill=rgbString(210, 206, 239), outline=outline)
    canvas.create_text(16*app.width/48, 3*app.height/48, text = 'Easy')
    if app.medium:
        outline = rgbString(255, 168, 214)
    else:
        outline = 'black'
    canvas.create_rectangle(21*app.width/48, app.height/48, 27*app.width/48, 5*app.height/48, fill=rgbString(171, 194, 254), outline=outline)
    canvas.create_text(24*app.width/48, 3*app.height/48, text = 'Medium')
    if app.hard:
        outline = rgbString(255, 168, 214)
    else:
        outline = 'black'
    canvas.create_rectangle(29*app.width/48, app.height/48, 35*app.width/48, 5*app.height/48, fill=rgbString(160, 224, 222), outline=outline)
    canvas.create_text(32*app.width/48, 3*app.height/48, text = 'Hard')

#determines which level the user selected
def level(app, x, y):
    if (y > app.height/48 and y < 5*app.height/48):
        if (x > 13*app.width/48 and x < 19*app.width/48) or back(app, x, y):
            return 'Easy'
        elif x > 21*app.width/48 and x < 27*app.width/48:
            return 'Medium'
        elif x > 29*app.width/48 and x < 35*app.width/48:
            return 'Hard'

#draws the back button and the power rule definition
def drawPower(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text='exponent * (function ** (exponent - 1)) * dfunction')
    canvas.create_rectangle(app.width/48, app.height/48, 5*app.width/48, 5*app.height/48, fill=rgbString(255, 168, 214))
    canvas.create_text(3*app.width/48, 3*app.height/48, text = 'Back')

#returns a randomly generated power rule practice problem
def findPowerProblem(app):
    if app.easy:
        exp = str(random.randint(2, 10))
        return [['x', '**', exp]]
    elif app.medium:
        coeff = str(random.randint(2, 10))
        exp = str(random.randint(2, 10))
        return [[coeff, '*', ['x', '**', exp]]]
    elif app.hard:
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log']
        outside = random.choice(functions)
        coeff = random.randint(2, 10)
        exp = random.randint(2, 10)
        return [[outside, [[coeff, '*', ['x', '**', exp]]]]]

#draws the problem and its answer
def drawPowerProblem(app, canvas):
    problem = app.powerProblem
    equation = list(displayDerivative(app, problem))
    canvas.create_text(app.width/2, app.height/2, text= cleanSubtraction(app, cleanDisplay(app, equation)))
    if '÷' in problem:
        deriv = derivative(app, problem)
    else:
        deriv = derivative(app, problem)[0]
    newDeriv = derivativeParse(deriv)
    equation = list(displayDerivative(app, newDeriv))
    if app.showAnswer:
        canvas.create_text(app.width/2, 2*app.height/3, text= cleanSubtraction(app, cleanDisplay(app, equation)))

def drawProduct(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text='left * dright + right * dleft')
    canvas.create_rectangle(app.width/48, app.height/48, 5*app.width/48, 5*app.height/48, fill=rgbString(255, 168, 214))
    canvas.create_text(3*app.width/48, 3*app.height/48, text = 'Back')

def findProductProblem(app):
    if app.easy:
        coeff1 = str(random.randint(2, 10))
        exp1 = str(random.randint(2, 10))
        coeff2 = str(random.randint(2, 10))
        exp2 = str(random.randint(2, 10))
        return [[coeff1, '*', ['x', '**', exp1]], '*', [coeff2, '*', ['x', '**', exp2]]]
    elif app.medium:
        functions = ['log', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        term1 = random.choice(functions)
        term2 = random.choice(functions)
        return [[term1, ['x']], '*', [term2, ['x']]]
    elif app.hard:
        functions = ['log', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        term1 = random.choice(functions)
        term2 = random.choice(functions)
        term3 = random.choice(functions)
        return [[[term1, ['x']], '*', [term2, ['x']]], '*', [term3, ['x']]]

def drawProductProblem(app, canvas):
    problem = app.productProblem
    equation = list(displayDerivative(app, problem))
    canvas.create_text(app.width/2, app.height/2, text= cleanSubtraction(app, cleanDisplay(app, equation)))
    if '÷' in problem:
        deriv = derivative(app, problem)
    else:
        deriv = derivative(app, problem)
    newDeriv = derivativeParse(deriv)
    equation = list(displayDerivative(app, newDeriv))
    if app.showAnswer:
        text = cleanSubtraction(app, cleanDisplay(app, equation))
        if len(text) > 60:
            lines = text.split('+')
            canvas.create_text(app.width/2, 2*app.height/3, text= lines[0] + '+')
            canvas.create_text(app.width/2, 13*app.height/18, text= lines[1] + '+')
            canvas.create_text(app.width/2, 14*app.height/18, text= lines[2])
        else:
            canvas.create_text(app.width/2, 2*app.height/3, text= text)

def drawQuotient(app, canvas):
    high = '(low * dhigh) - (high * dlow)'
    line = '___________________________'
    low = 'low * low'
    canvas.create_text(app.width/2, 15*app.height/64, text=high)
    canvas.create_text(app.width/2, app.height/4, text=line)
    canvas.create_text(app.width/2, 9*app.height/32, text=low)
    canvas.create_rectangle(app.width/48, app.height/48, 5*app.width/48, 5*app.height/48, fill=rgbString(255, 168, 214))
    canvas.create_text(3*app.width/48, 3*app.height/48, text = 'Back')

def findQuotientProblem(app):
    if app.easy:
        coeff1 = str(random.randint(2, 10))
        exp1 = str(random.randint(2, 10))
        coeff2 = str(random.randint(2, 10))
        exp2 = str(random.randint(2, 10))
        return [[coeff1, '*', ['x', '**', exp1]], '÷', [coeff2, '*', ['x', '**', exp2]]]
    elif app.medium:
        functions = ['x', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        term1 = random.choice(functions)
        if term1 == 'x':
            term2 = random.choice(functions[1:])
        else:
            term2 = random.choice(functions)
        if term1 == 'x':
            return [term1, '÷', [term2, ['x']]]
        elif term2 == 'x':
            return [[term1, ['x']], '÷', term2]
        return [[term1, ['x']], '÷', [term2, ['x']]]
    elif app.hard:
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot']
        term1 = random.choice(functions)
        term2 = random.choice(functions)
        term3 = random.choice(functions)
        return [[[term1, ['x']], '÷', [term2, ['x']]], '÷', [term3, ['x']]]

def drawQuotientProblem(app, canvas):
    problem = app.quotientProblem
    equation = list(displayDerivative(app, problem))
    canvas.create_text(app.width/2, app.height/2, text= cleanSubtraction(app, cleanDisplay(app, equation)))
    answer = derivative(app, problem)
    newAnswer = derivativeParse(answer)
    equation = list(displayDerivative(app, newAnswer))
    if (app.easy or app.medium) and app.showAnswer:
        answer = cleanSubtraction(app, cleanDisplay(app, equation))
        temp = answer.split('÷')
        high, low = temp[0], temp[1]
        line = '_' * len(high)
        canvas.create_text(app.width/2, 46*app.height/72, text=high)
        canvas.create_text(app.width/2, 2*app.height/3, text=line)
        canvas.create_text(app.width/2, 26*app.height/36, text=low)
    elif app.hard and app.showAnswer:
        answer = cleanSubtraction(app, cleanDisplay(app, equation))
        temp = answer.split('÷')
        high, low = '÷'.join(temp[:3]), temp[3]
        divide = high.split('*')
        ind = findDivisionTerm(divide)
        subhigh, sublow = divide[:ind] + [divide[ind][:divide[ind].index('÷')]], [divide[ind][divide[ind].index('÷') + 1:]] + [divide[ind + 1][:divide[ind + 1].index('-')]]
        line1 = '_' * len(makeString(subhigh))
        remainder = [divide[ind + 1][divide[ind + 1].index('-'):]] + divide[ind + 2:]
        canvas.create_text(app.width/2 + len(line1), 21*app.height/36, text=makeString(subhigh), anchor=E)
        canvas.create_text(app.width/2, 11*app.height/18, text=line1 + makeString(remainder))
        canvas.create_text(app.width/2, 23*app.height/36, text=makeString(sublow), anchor=E)
        line2 = '_' * (len(makeString(subhigh)) + len(makeString(remainder)))
        canvas.create_text(app.width/2, 46*app.height/72, text= '')
        canvas.create_text(app.width/2, 2*app.height/3, text=line2)
        canvas.create_text(app.width/2, 26*app.height/36, text=low)

def findDivisionTerm(L):
    for i in range(len(L)):
        if '÷' in L[i]:
            return i

def makeString(L):
    string = ''
    for term in L:
        string += term
    return string

def drawChain(app, canvas):
    canvas.create_text(app.width/2, app.height/4, text='doutside(inside) * dinside')
    canvas.create_rectangle(app.width/48, app.height/48, 5*app.width/48, 5*app.height/48, fill=rgbString(255, 168, 214))
    canvas.create_text(3*app.width/48, 3*app.height/48, text = 'Back')

def findChainProblem(app):
    if app.easy:
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log']
        outside = random.choice(functions)
        return [[outside, ['x']]]
    elif app.medium:
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log']
        outside = random.choice(functions)
        coeff = random.randint(2, 10)
        exp = random.randint(2, 10)
        return [[outside, [[coeff, '*', ['x', '**', exp]]]]]
    elif app.hard:
        functions = ['sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'log']
        outside1 = random.choice(functions)
        outside2 = random.choice(functions)
        coeff = random.randint(2, 10)
        exp = random.randint(2, 10)
        return [[outside1, [[outside2, [[coeff, '*', ['x', '**', exp]]]]]]]

def drawChainProblem(app, canvas):
    problem = app.chainProblem
    equation = list(displayDerivative(app, problem))
    canvas.create_text(app.width/2, app.height/2, text= cleanSubtraction(app, cleanDisplay(app, equation)))
    if '÷' in problem:
        deriv = derivative(app, problem)
    else:
        deriv = derivative(app, problem)[0]
    newDeriv = derivativeParse(deriv)
    equation = list(displayDerivative(app, newDeriv))
    if app.showAnswer:
        text = cleanSubtraction(app, cleanDisplay(app, equation))
        if len(text) > 60:
            lines = text.split('(')
            for i in range(len(wrap(lines))):
                if i == len(wrap(lines)) - 1:
                    canvas.create_text(app.width/2, (12+i)*app.height/18, text= wrap(lines)[i])
                elif wrap(lines)[i][-1] != '(':
                    canvas.create_text(app.width/2, (12+i)*app.height/18, text= wrap(lines)[i] + '(')
                else:
                    canvas.create_text(app.width/2, (12+i)*app.height/18, text= wrap(lines)[i])
        else:
            canvas.create_text(app.width/2, 2*app.height/3, text= text)

def wrap(L):
    count = 0
    for i in range(0, len(L) -1, 2):
        if len(L[i]) + len(L[i + 1]) <= 60:
            count += 1
    if count == 0:
        return L
    else:
        final = []
        if len(L) % 2 != 0:
            L.append('')
        for i in range(0, len(L)-1, 2):
            if len(L[i]) + len(L[i + 1]) <= 60:
                if L[i + 1] != '':
                    string = L[i] + '(' + L[i + 1]
                    final.append(string)
                else:
                    final.append(L[i])
            else:
                final.append(L[i])
                final.append(L[i + 1])
        return wrap(final)

#draws pink background
def drawBackground(app, canvas):
    canvas.create_rectangle(0, 0, app.width, app.height, fill=rgbString(246, 227, 240))

#draws start button on welcome page
def start(app, x, y):
    return x > 5*app.width/12 and x < 7*app.width/12 and y > 11*app.height/16 and y < 13*app.height/16

#draws welcome page messages
def drawWelcome(app, canvas):
    canvas.create_text(app.width/2, app.height/3, text = 'Welcome to Derivation Nation', font = 'Arial 20 bold')
    #canvas.create_text(app.width/2, 5*app.height/12, text = 'Dedicated to my high school calc teacher, Ms. Phillips', font = 'Arial 12 bold')
    canvas.create_text(app.width/2, app.height/2, text = 'Press start to get deriving', font = 'Arial 15 bold')
    canvas.create_rectangle(5*app.width/12, 11*app.height/16, 7*app.width/12, 13*app.height/16, fill=rgbString(255, 168, 214))
    canvas.create_text(3*app.width/6, 6*app.height/8, text = 'Start')

def getKeyCenterAndRadius(app, index):
    keyWidth = app.width / 10
    keyHeight = ((2/3) * app.height)
    return ((keyWidth/2)+(keyWidth*index), keyHeight, keyWidth/2)

def getKeyIndex(app, x, y):
    for i in range(10):
        (cx, cy, r) = getKeyCenterAndRadius(app, i)
        if x > cx - r and x < cx + r and y > cy - r and y < cy + r:
            return i
        elif x > cx - r and x < cx + r and y > cy + r and y < cy + 3*r:
            return app.functions[i]
        elif x > cx -r and x < cx + r and y > cy + 3*r and y < cy + 5*r:
            return app.signs[i]
    return None

#displays the calculator buttons
def drawNumbers(app, canvas):
    for i in range(10):
        (cx, cy, r) = getKeyCenterAndRadius(app, i)
        canvas.create_rectangle(cx-r, cy-r, cx+r, cy+r, fill=rgbString(210, 206, 239))
        canvas.create_text(cx, cy, text=f'{i}')
        canvas.create_rectangle(cx-r, cy+r, cx+r, cy+3*r, fill=rgbString(171, 194, 254))
        canvas.create_text(cx, cy+2*r, text=f'{app.functions[i]}')
        canvas.create_rectangle(cx-r, cy+3*r, cx+r, cy+5*r, fill=rgbString(160, 224, 222))
        canvas.create_text(cx, cy+4*r, text=f'{app.signs[i]}')

#displays the input
def displayEquation(app):
    display = ''
    for val in app.display:
        display += f'{val}'
    return display

def drawEquation(app, canvas):
    canvas.create_text(app.width/2, app.height/3, text = displayEquation(app))

def displayDerivativeHelper(app, equation, currDisplay):
    display = ''
    for term in equation:
        if isinstance(term, list):
            display += '('
            display += displayDerivativeHelper(app, term, display)
            display += ')'
        else:
            display += str(term)
    return display

#displays the output
def displayDerivative(app, equation):
    return displayDerivativeHelper(app, equation, '')

def cleanDisplayHelper(app, equation):
    leftIndex = 0
    stack = []
    indexes = []
    for i in range(len(equation)):
        if equation[i] == '(':
            stack.append(i)
        elif equation[i] == ')':
            indexes.append((stack[len(stack) - 1], i))
            stack.pop()
    return indexes

#left moves right, right moves left
#gets rid of extra parenthesis
def cleanDisplay(app, equation):
    indexes = cleanDisplayHelper(app, equation)
    if indexes == []:
        return equation
    for (left, right) in indexes:
        if (left + 1, right - 1) in indexes:
            equation.pop(left)
            equation.pop(right - 1)
            return cleanDisplay(app, equation)
    return equation

#call on cleanDisplay
#gets rid of the 0 in 0 - terms
def cleanSubtraction(app, equation):
    i = 0
    while i < len(equation) - 1:
        if equation[i] == '0':
            if i != 0 and not equation[i - 1].isnumeric:
                if equation[i + 1] == '-':
                    equation.pop(i)
                    i -= 1
            else:
                if equation[i + 1] == '-':
                    equation.pop(i)
                    i -= 1
        i += 1
    final = ''
    for c in equation:
        final += c
    return final

#cleans up multiplication in power rule
def derivativeParse(L):
    if not isinstance(L, list) or len(L) < 3:
        return L
    term1 = L[0]
    operator = L[1]
    term2 = L[2]
    if operator == '+':
        term2 = derivativeParse(term2)
    if not isinstance(term1, list) and not isinstance(term2, list) and term1.isnumeric() and term2.isnumeric() and operator == '*':
        return [str(int(term1) * int(term2))]
    if isinstance(term1, list) and isinstance(term2, list) and operator == '*':
        return [derivativeParse(term1), '*', derivativeParse(term2)]
    if isinstance(term1, list) and isinstance(term2, list) and operator == '+':
        return [derivativeParse(term1), '+', term2]
    else:
        if not isinstance(term1, list) and not isinstance(term1, int) and term1.isnumeric() and isinstance(term2, list) and operator == '*':
            if not isinstance(term2[0], list) and term2[0].isnumeric() and term2[1] == '*':
                return derivativeParse([str(int(term1) * int(term2[0]))] + [term2[1]] + [term2[2]])
        elif not isinstance(term1, list) and not isinstance(term1, int) and term1.isnumeric() and isinstance(term2, list) and operator == '+':
            return [term1, '+', term2]
        return L

def drawDerivative(app, canvas):
    if '÷' in app.equation:
        deriv = derivative(app, app.equation)
    else:
        deriv = derivative(app, app.equation)[0]
    newDeriv = derivativeParse(deriv)
    equation = list(displayDerivative(app, newDeriv))
    canvas.create_text(app.width/2, 21*app.height/48, text= cleanSubtraction(app, cleanDisplay(app, equation)))

#draws the rules used
def displayRules(app):
    display = ''
    count = 0
    for rule in app.rules:
        count += 1
        display += rule
        if count <= len(app.rules) - 1:
            display += ', '
    return display

#draws the power rule button
def powerRule(app, canvas):
    canvas.create_rectangle(app.width/24, 2*app.height/24, 3*app.width/24, 4*app.height/24, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/24, 3*app.height/24, text='Power\nRule')

def productRule(app, canvas):
    canvas.create_rectangle(app.width/24, 5*app.height/24, 3*app.width/24, 7*app.height/24, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/24, 6*app.height/24, text='Product\nRule')

def quotientRule(app, canvas):
    canvas.create_rectangle(app.width/24, 8*app.height/24, 3*app.width/24, 10*app.height/24, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/24, 9*app.height/24, text='Quotient\nRule')

def chainRule(app, canvas):
    canvas.create_rectangle(app.width/24, 11*app.height/24, 3*app.width/24, 13*app.height/24, fill=rgbString(255, 168, 214))
    canvas.create_text(2*app.width/24, 12*app.height/24, text='Chain\nRule')

def drawRules(app, canvas):
    canvas.create_text(app.width/2, 25*app.height/48, text = displayRules(app))

#determines which rule the user wants to practice with
def whichRule(app, x, y):
    if x > app.width/24 and x < 3*app.width/24:
        if y > 2*app.height/24 and y < 4*app.height/24:
            return 'Power Rule'
        elif y > 5*app.height/24 and y < 7*app.height/24:
            return 'Product Rule'
        elif y > 8*app.height/24 and y < 10*app.height/24:
            return 'Quotient Rule'
        elif y > 11*app.height/24 and y < 13*app.height/24:
            return 'Chain Rule'

def main():
    runApp(width=650, height=550)

if __name__ == '__main__':
    main()
