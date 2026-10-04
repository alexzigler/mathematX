from itertools import product
from src.string_input_utils import parenthesis_levels


def generate_round_robin_tests(r: int):
    if r == 2:
        test_signs = ('+', '-', '*')
        test_relationals = ('=', '<=')
        test_alphas = ('a', 'A')
        test_nums = ('5', '555555555555', '5.2', '-5', '-5.2')
        test_specials = ('_', '.', "'", ',', '(', ')')
    elif r == 3 or r == 4 or r == 5:
        test_signs = ('+', '-', '*')
        test_relationals = ('=', '<=')
        test_alphas = ('a',)
        test_nums = ('3', '5.2', '-5.2')
        test_specials = ('_', '.', "'", ',', '(', ')')
    else:
        return None

    tests = test_signs + test_relationals + test_alphas + test_nums + test_specials
    return tuple(product(tests, repeat=r))


def main():
    rr = generate_round_robin_tests(3)
    try:
        with open("round_robin.txt", 'w') as f:
            for pair in rr:

                elem = ''.join(pair)
                p_levels_round = parenthesis_levels(elem, '(', ')')
                # remove all entries with unmatching parentheses
                if p_levels_round.count('(') == p_levels_round.count(')') and p_levels_round.find('-') == -1:
                    f.write('assert valid_string_input("')
                    f.write(elem)
                    f.write('") == False')
                    f.write('\n')
                else:
                    continue

    except IOError:
        pass


if __name__ == '__main__':
    main()
