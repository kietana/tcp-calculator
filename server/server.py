from socket import *
import re

# Set of valid operator in an expression
operator = {'+', '-', '/', '*', '%', '^'}

# Valid mathematical symbol
valid_symbol = {'+', '-', '/', '*', '%', '^', '.', '(', ')'}

# Priority of operator: higher value means higher priority
priority = {'(': 0, ')': 0,
            '+': 1, '-': 1,
            '*': 2, '/': 2, '%': 2,
            '^': 3}


# Handles many signs: +++3, +2 , -+2
def handle_sign(expr):
    while any(el in expr for el in ['++', '+-', '-+', '--']):
        expr = expr.replace('++', '+')
        expr = expr.replace('+-', '-')
        expr = expr.replace('-+', '-')
        expr = expr.replace('--', '+')
    return expr


# Function to check whether given expression is valid
def is_valid_expr(expr):

    if expr[0] in {'/', '*', '%', '^'}:  # *1 , ^1+1
        return False
    if expr[-1] in operator or exp[-1] == '.':  # 1+1+ , 1+1.
        return False
    if not any(el.isdigit() for el in expr):  # No digits at all: + , (*)
        return False
    if expr.count('(') != expr.count(')'):  # (1))) , 1+(1+1))
        return False
    if '..' in expr:  # 1...1 , 11+..1
        return False

    expr = handle_sign(expr)

    for i in range(len(expr)):
        if expr[i] not in valid_symbol and not expr[i].isdigit():  # 1+a, 1&2, 1=1
            return False
        if expr[i] in operator and expr[i+1] in operator:  # 11+*/1
            return False
        if expr[i] in {'(', '.'} and expr[i+1] in {'/', '*', '%', '^'}:  # 1+(/2)
            return False

    return True


# Function to convert infix expression -> postfix expression
def to_postfix(infix):
    infix = handle_sign(infix)
    infix = re.findall(r'[*/%()^+-]|[0-9]*[.][0-9]+|[0-9]+', infix)  # Return a list of strings
    postfix = []  # Store postfix expression
    stack = []  # Store operators

    for el in infix:
        if el == '(':
            stack.append(el)
            continue

        elif el == ')':
            next_element = stack.pop()
            while stack and next_element != '(':  # Stack is not empty
                postfix.append(next_element)
                next_element = stack.pop()
            continue

        elif el in operator:
            while stack and priority[stack[-1]] >= priority[el]:
                postfix.append(stack.pop())
            stack.append(el)
            continue

        else:  # Default: put operands into postfix list
            postfix.append(el)
            continue

    while stack:  # Pop remaining operators from the stack
        postfix.append(stack.pop())

    return postfix


def eval_postfix(postfix: list):
    stack = []  # Store the operand

    # Convert number becomes int or float
    for i in range(len(postfix)):
        if postfix[i] not in operator:
            postfix[i] = float(postfix[i]) if '.' in postfix[i] else int(postfix[i])

    # Scan the postfix from left to right
    for el in postfix:
        if el in operator:
            first_value = stack.pop()
            second_value = 0 if not stack else stack.pop()  # Assign 0 to second_value if stack is empty

            if el == '*':
                stack.append(second_value * first_value)
                continue
            elif el == '/':
                try:
                    res = second_value / first_value
                    stack.append(int(res)) if res.is_integer() else stack.append(res)
                except ZeroDivisionError:
                    return "Zero Division Error: division by zero."
                continue
            elif el == '%':
                stack.append(second_value % first_value)
                continue
            elif el == '+':
                stack.append(second_value + first_value)
                continue
            elif el == '-':
                stack.append(second_value - first_value)
                continue
            elif el == '^':
                stack.append(second_value ** first_value)
                continue
        else:
            stack.append(el)
            continue

    return str(round(stack[0], 3)) if isinstance(stack[0], float) else str(stack[0])  # 3 decimal places


serverAddress = ('140.118.145.184', 5000)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(serverAddress)
serverSocket.listen(1)  # Listen to 1 client at most

while True:
    print("\nServer is listening...")
    connectionSocket, clientAddress = serverSocket.accept()
    connectionSocket.send("\nHello, Client!".encode())

    mode = connectionSocket.recv(1024).decode()

    while mode:
        if mode == 'q':
            connectionSocket.send("Bye, Client! Connection Closed.".encode())
            connectionSocket.close()
            print("Client exited.\n")
            break

        print("Mode: " + mode)

        while mode == '1':
            exp = connectionSocket.recv(1024).decode()
            if exp == 'q':
                break
            answer = eval_postfix(to_postfix(exp)) if is_valid_expr(exp) else "Invalid Expression."
            connectionSocket.send(answer.encode())

        ans_file = open("Ans.txt", 'w')
        while mode == '2':
            exp = connectionSocket.recv(1024).decode()
            if exp == 'q':
                break  # Exit the mode

            answer = eval_postfix(to_postfix(exp)) if is_valid_expr(exp) else "Invalid Expression."
            ans_file.write(answer + '\n')
            connectionSocket.send(answer.encode())
        ans_file.close()

        print("-----------------------------------\nExited the mode.\n")
        mode = connectionSocket.recv(1024).decode()
