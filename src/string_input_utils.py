funcs = ('log', 'exp', 'sin', 'cos', 'sh', 'ch', 'tan', 'ctg', 'arctan', 'sqrt')  # add more
signs = ('+', '-', '*', '/', '^', '%')
relationals = ('=', '<', '>')  # '<=' and '>=' are considered in the logic
parentheses = ('(', ')', '[', ']', '{', '}')
separators = (',', '&', ';')
operands = ('\'', '`')
specials = ('_', '.') + operands + separators + parentheses

# TODO: define code errors to let the user know his mistake

"""
    Round parentheses ()
        order of operations
        specify argument of a function - user defined or predefined funcs
    Square brackets []
        define vectors, matrices, vector valued functions
    Curly brackets {}
        specify conditions for an expression
    _ subscript
    , separate equations, separate elements of vectors, separate variables for multivariable calc
    . float numbers
    ; separate equations, new row in matrix
    ' derivatives
    ` derivatives
    & separate equations 
"""


def remove_whitespaces(s: str) -> str:
    return s.replace(' ', '')


def parenthesis_levels(s: str, left: str, right: str) -> str:
    """see /doc/parenthesis_levels.png
    Creates a string that keeps all the parentheses of a string, specified by left and right;
    Replace all non-parenthesis characters with the current level;
    Level starts as zero, increments for left parenthesis, decrements for right parenthesis.
    After every parenthesis, the level is appended to the string, in order to catch invalid cases like ')('.

    :param s: input string
    :param left: left parenthesis
    :param right: right parenthesis
    :return: the newly created string as described above
    """
    level = 0
    s_out = ""
    for c in s:
        if c == left:
            level += 1
            s_out += left
        elif c == right:
            level -= 1
            s_out += right
        s_out += str(level)
    return s_out


def consecutive_signs(s: str) -> bool:
    """
    ensures the only allowed sequence of consecutive signs is '+-'.

    :param s: input string
    :return: bool value indicating whether the input string is valid from signs point of view
    """
    for i in range(len(s) - 1):
        if s[i] in signs and s[i + 1] in signs:
            if s[i] == '+' and s[i + 1] == '-':
                continue
            else:
                return True
    return False


def consecutive_relationals(s: str) -> bool:
    """
    ensures the only 2 sequences of relational operators allowed are '<=' and '>='.

    :param s: input string
    :return: bool value indicating whether the input string is valid from relational operators point of view
    """
    for i in range(len(s) - 1):
        if s[i] in relationals and s[i + 1] in relationals:
            if s[i] == '<' and s[i + 1] == '=' or s[i] == '>' and s[i + 1] == '=':
                continue
            else:
                return True
    return False


def invalid_alpha_group(s: str) -> bool:
    """
    search for sequences of consecutive alpha characters that exceed the limit;
    if such a sequence is not a predefined function, the input string is invalidated.
    Note: the limit is not imposed for the global number of variables, but for a sequence.

    :param s: input string
    :return: bool value indicating an alpha sequence which exceeds the limit
    """
    # prevent smashing your head on the keyboard :)
    consecutive_alpha_lim = 4
    tmp_str = ""
    cnt = 0
    for i in range(len(s)):
        if s[i].isalpha():
            tmp_str += s[i]
            cnt += 1
        else:
            if cnt > consecutive_alpha_lim and not [func for func in funcs if tmp_str.find(func) != -1]:
                # check if any of the functions in funcs appears in tmp_str
                return True
            cnt = 0
            tmp_str = ""
    else:
        if cnt > consecutive_alpha_lim and tmp_str not in funcs:  # branch in case the string ends with an invalid group
            return True

    return False


def bad_placement_of_specials(s: str) -> bool:
    """
    specials are ('_', ',', '.', ';', '\'', '`', '&') and parentheses;

    Conditions:

    separators ',' ';' '&' should be at level zero from round and square parentheses' perspective;
    '_' placement (alpha to left, digit to right);
    '.' placement (allow '3.' or '.3' - at least one digit neighbor, not allow specials or alphas before);
    duplicates for '_' and '.' are not allowed ;
    derivative operators placement (left neighbor - right parenthesis, alpha, digit, point);

    :param s: input string
    """

    p_levels_round = parenthesis_levels(s, '(', ')')
    p_levels_square = parenthesis_levels(s, '[', ']')
    p_levels_curly = parenthesis_levels(s, '{', '}')

    s_round = s.replace("(", "( ")
    s_round = s_round.replace(")", ") ")
    s_square = s.replace("[", "[ ")
    s_square = s_square.replace("]", "] ")

    if (p_levels_round.count('(') != p_levels_round.count(')')
            or p_levels_square.count('[') != p_levels_square.count(']')
            or p_levels_curly.count('{') != p_levels_curly.count('}')):
        # numbers of parentheses do not match (left with right)
        return True

    if p_levels_round.find('-') != -1 or p_levels_square.find('-') != -1 or p_levels_curly.find('-') != -1:
        # parentheses levels become negative (you close more than you open)
        return True

    # nested curly brackets not allowed
    if [c for c in p_levels_curly if c not in ('0', '1', '{', '}')]:
        return True

    # the following line of code should be False if the execution reached here
    # (uncomment for debug)
    # len(p_levels_round) != len(s_round) or len(p_levels_square) != len(s_square):

    # specials that are not allowed within round parentheses
    for i in range(len(s_round)):
        if s_round[i] in (';', '&', '{', '}') and p_levels_round[i] != '0':
            return True
    # specials that are not allowed within square parentheses
    for i in range(len(s_square)):
        if s_square[i] in ('&', '{', '}') and p_levels_square[i] != '0':
            return True

    # wrong placements of '_', '.', '\'' or '`'
    if len(s) == 0:
        return False
    if len(s) == 1 and not s[0].isalnum(): # edge case
        return True
    if len(s) >= 2:
        if s[0] == '_' or s[-1] == '_':  # edge case for '_' near bounds
            return True
        if s[0] == '.' and not s[1].isdigit():  # edge case for string starting with '.'
            return True
        if s[-1] == '.' and not s[-2].isdigit():  # edge case for string ending with '.'
            return True
        if s[0] in operands:
            return True
    for i in range(1, len(s) - 1):
        if s[i] == '_':
            if not s[i - 1].isalpha() or not s[i + 1].isdigit():  # format {alpha}_{digit} not respected
                return True
        if s[i] == '.':
            if not s[i - 1].isdigit() and not s[i + 1].isdigit():
                # allow '3.' and '.3', both have implicit 0, but not ' . '
                return True
            if s[i - 1].isalpha() or s[i - 1] in ('.', '_', '\'', '`', ')', ']', '}'):
                # not allow strings like 'x.3' or duplicates of specials
                return True
        if s[i] in operands:  # the derivative operator can pe preceded by certain characters
            if not s[i - 1].isalnum() and s[i - 1] not in ('.', ')', ']', ' ') + operands:
                return True
    if s[-1] in operands and not s[-2].isalnum() and s[-2] not in ('.', ')', ']', ' ') + operands:
        # check the last character if in operands
        return True
    return False


def incorrect_character_order(s:str) -> bool:
    """
    Detection of undesired order of characters.

    Case 1: interruption of alpha sequence by at least 2 consecutive digits(e.g. 'x23y');
    Note 1: one digit is required for handling subscripts (e.g. 'x1' instead of 'x_1');

    Case 2:

    #TODO continue
    :param s: input string
    :return: boolean value specified in doc
    """
    # include alpha_group_interrupted functionality here
    # together with the 3 edge cases already found
    # think of others, use permutations with classes of chars

    # TODO integrate:
    # code for alpha sequence interrupted

    # if len(s) <= 2:
    #     return False
    # for i in range(len(s) - 2):
    #     if s[i].isalpha():
    #         if s[i + 1].isdigit() and s[i + 2].isdigit():
    #             return True
    # return False

    pass


def invalid_func_args(s: str) -> bool:
    """
    search for functions in the input string and check whether content is valid;
    the string inside the function must be an expression i.e. it cannot contain
    separators, relational operators, square or curly brackets.

    :param s: input string
    :return: boolean value specified in doc
    """

    p_levels_round = parenthesis_levels(s, '(', ')')
    s_round = s.replace("(", "( ")
    s_round = s_round.replace(")", ") ")

    tmp_str = ''
    for i in range(len(s_round) - 1):
        if s_round[i].isalpha():
            tmp_str += s_round[i]
            if tmp_str in funcs:  # search for functions in the string
                if s_round[i + 1] != '(':  # make sure the functions have their arguments within parentheses
                    return True
                # get argument string by searching for the corresponding right parenthesis
                end_index = i + 1 + p_levels_round[(i + 1):].index(p_levels_round[i]) - 1  # right parenthesis index
                argument = s_round[(i + 2):end_index]
                for ch in argument:
                    if ch in separators + relationals + ('[', ']', '{', '}'):
                        return True
        else:
            tmp_str = ''
    return False


def valid_string_input(s: str) -> bool:
    """
    takes the raw input string and checks all validity conditions;
    in case of nonvalidity, the string will not reach processing phase.

    :param s: input string
    :return: bool value indicating whether the input string is valid
    """

    s_stripped = remove_whitespaces(s)

    if len(s_stripped) == 0:
        return False

    if s_stripped[-1] in signs:  # expression ends with a sign
        return False

    if consecutive_signs(s_stripped):  # 2 consecutive signs (except +-)
        return False

    if s_stripped[0] in relationals or s_stripped[-1] in relationals: # incomplete equality/inequality
        return False

    if consecutive_relationals(s_stripped):  # 2 forbidden consecutive relational operators
        return False

    if [ch for ch in s_stripped if not ch.isalnum() and ch not in specials + signs + relationals]:
        # non-supported characters
        return False

    if invalid_alpha_group(s_stripped):  # limit exceeded for consecutive letters not in funcs
        return False

    if bad_placement_of_specials(s_stripped):
        # any sort of bad placement of characters ('_', ',', '.', ';', '\'', '`', '&')
        return False

    if invalid_func_args(s_stripped):
        return False

    return True


def split_expression(s: str) -> list[str]:
    # the goal is to split the expressions into a dynamic array of strings

    if not valid_string_input(s):
        # fill in with desired behaviour
        return []

    # Rule: coeff * variable

    # handles

    # specials duplicates (reduce to 1 or invalidate string)
    # handle inverses of funcs
    # handle subscripts like x_1
    # find the string '()' inside the expression ->  maybe x can be implicit
    # exponent not written using ^ -> not in ascii
    # string ends with (except '=') relational operators -> remove them
    # separators like ',' ';' 'and' for multiple expressions
    # {} conditions, replace all [] with ()
    # handle float coeffs
    # handle d/dx()
    # int/integral keyword
    # curly brackets placement define rule?
    # check redundant parentheses
    # xysqrt(xy) vs xy sqrt(xy)
    # negative powers

    # 1. define variables, can you define variables?, validate the sanity of the expression(?)
    # 2. separators () {} , ; & and => multiple expressions
    # 3. logic in case of relationals

# def number_of_variables(s):
# #returns the number of different letters found in input s
#     my_set=set()
#     for c in s:
#         if isalpha(c):
#             my_set.add(c)
#     return len(my_set)
