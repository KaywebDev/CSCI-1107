
from stack_array import Stack, EmptyStack
import operator

# dict mapping operator tokens to actual arithmetic
# functions, for use in eval_postfix
OPERATORS = {"+": operator.add,
             "-": operator.sub,
             "*": operator.mul,
             "/": operator.floordiv}


# dict mapping operator tokens to relative precedence
# (PEMDAS), for use in infix_to_postfix
OP_PRECEDENCE = {"+": 1,
                 "-": 1,
                 "*": 2,
                 "/": 2}

def infix_to_postfix(infix_expr):

    input_tokens = infix_expr.split()
    output_tokens = []
    operator_stack = Stack()

    # for each token in the infix expression, left to right
    for token in input_tokens:

        # if the next token is an operator, move all operators
        # of equal or lesser precedence from the top of the stack
        # to the end of the postfix expression
        if token in OP_PRECEDENCE:
            new_preced = OP_PRECEDENCE[token]
            # while the stack isn't empty
            # ... and the top value on the stack is an operator
            # ... and the operator is of equal or higher precedence
            while len(operator_stack) > 0 and \
                  operator_stack.peek() in OP_PRECEDENCE and \
                  OP_PRECEDENCE[operator_stack.peek()] >= new_preced:
                output_tokens.append(operator_stack.pop())
            operator_stack.push(token)
        # if the next token is a left paren, push it onto the stack
        elif token == "(":
            operator_stack.push(token)
        # if the next token is a right paren, move values from the
        # top of the stack to the end of the postfix expression
        # until the matching left paren is found
        elif token == ")":
            stack_top = operator_stack.pop()
            while stack_top != "(":
                output_tokens.append(stack_top)
                stack_top = operator_stack.pop()
        # if the next token is operand, append it to the postfix
        # expression
        else:
            output_tokens.append(token)

    # move all remaining values from the top of the operator stack to the
    # end of the postfix expression
    while not operator_stack.is_empty():
        output_tokens.append(operator_stack.pop())

    # convert the list of output tokens to a proper postfix string
    return " ".join(output_tokens)

def eval_postfix(postfix_expr):

        eval_stack = Stack()
        tokens = postfix_expr.split()

        for token in tokens:

            # if next token is an operator, evaluate it by popping
            # two values from the operand stack
            if token in OPERATORS:
                try:
                    right_op = eval_stack.pop()
                    left_op = eval_stack.pop()
                    ans = OPERATORS[token](left_op,right_op)
                    eval_stack.push(ans)
                except EmptyStack:
                    raise ValueError(f"Invalid expression: {token} has insufficient operands.")
            # if next token is an operand, push it onto the
            # operand stack
            else:
                eval_stack.push(int(token))


        # stack must contain exactly 1 value at end if the expression was valid
        if len(eval_stack) == 1:
            return eval_stack.pop()
        else:
            raise ValueError(f"Invalid expression: {len(eval_stack)} operands remain unevaluated")


if __name__ == "__main__":

    infix_expression = "2 + 3 * 4 + 2 * ( 2 + 3 )"
    postfix_expression = infix_to_postfix(infix_expression)
    answer = eval_postfix(postfix_expression)
    print(infix_expression)
    print(postfix_expression)
    print(answer)
    
    
