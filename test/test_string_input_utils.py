import pytest
from src.string_input_utils import *


def test_parenthesis_levels():
    assert parenthesis_levels('a', '(', ')') == '0'
    assert parenthesis_levels('qwertyuiop', '(', ')') == '0000000000'
    assert parenthesis_levels('alex(alex((alex*7)))', '(', ')') == '0000(11111(2(3333333)2)1)0'
    assert parenthesis_levels('0', '(', ')') == '0'
    assert parenthesis_levels('()', '(', ')') == '(1)0'
    assert parenthesis_levels('(', '(', ')') == '(1'
    assert parenthesis_levels(')', '(', ')') == ')-1'
    assert parenthesis_levels('qw)(qw', '(', ')') == '00)-1(000'
    assert parenthesis_levels(')qw)qw)qw(qw(q', '(', ')') == ')-1-1-1)-2-2-2)-3-3-3(-2-2-2(-1-1'


def test_remove_whitespaces():
    assert remove_whitespaces('    straw      berry     ') == 'strawberry'
    assert remove_whitespaces('strawberry') == 'strawberry'
    assert remove_whitespaces('x^3 + x^2 + x +1 = 0') == 'x^3+x^2+x+1=0'
    assert remove_whitespaces('') == ''
    assert remove_whitespaces(' ') == ''
    assert remove_whitespaces('        ') == ''


def test_consecutive_signs():
    assert consecutive_signs('') == False
    assert consecutive_signs('x123y123z123') == False
    assert consecutive_signs('x+123y+123z+123') == False
    assert consecutive_signs('x+    123y+ 123 z+ 123') == False
    assert consecutive_signs('x+3') == False
    assert consecutive_signs('x^2+2x+3') == False
    assert consecutive_signs('+-2') == False
    assert consecutive_signs('x+-2') == False  # +- is the only exception

    assert consecutive_signs('x++3') == True
    assert consecutive_signs('x**3') == True
    assert consecutive_signs('x^^3') == True
    assert consecutive_signs('x//3') == True
    assert consecutive_signs('x--3') == True
    assert consecutive_signs('x^%3') == True


def test_consecutive_relationals():
    assert consecutive_relationals('') == False
    assert consecutive_relationals('<') == False
    assert consecutive_relationals('=') == False
    assert consecutive_relationals('=strawberry') == False
    assert consecutive_relationals('=straw>berry<') == False
    assert consecutive_relationals('<=straw>=berry<exp>') == False

    assert consecutive_relationals('><') == True
    assert consecutive_relationals('==') == True
    assert consecutive_relationals('pancake<>x') == True
    assert consecutive_relationals('cake<==x') == True
    assert consecutive_relationals('cake<==>x') == True
    assert consecutive_relationals('cake=>x') == True
    assert consecutive_relationals('cake=<x') == True


def test_invalid_alpha_group():
    assert invalid_alpha_group('') == False
    assert invalid_alpha_group('198+125x') == False
    assert invalid_alpha_group('198+125x + 983 y + 189 z + x^2 + (xy)^2 * sqrt(yzw)') == False
    assert invalid_alpha_group('123xyzt+8x^3') == False
    assert invalid_alpha_group('55x_1x_2x_3x_4x_5x_6x_7 + 11') == False
    assert invalid_alpha_group('3 + arctan(761x^3+sqrt(x/y))') == False

    assert invalid_alpha_group('123xyzt+ 88abcde +8x^3') == True
    assert invalid_alpha_group('strawberry') == True
    assert invalid_alpha_group('(x+y+z+w)^4 + logxyzw') == True

    assert invalid_alpha_group('123xyzt+ 88abc de +8x^3') == False  # function does not clear whitespaces on its own
    assert invalid_alpha_group('xysqrt(xy)') == False


def test_bad_placement_of_specials():

    # numbers of parentheses do not match (left with right)
    assert bad_placement_of_specials('()') == False
    assert bad_placement_of_specials('exp()') == False
    assert bad_placement_of_specials('3(x+y)^(7sqrt(xy))') == False

    assert bad_placement_of_specials('[]') == False
    assert bad_placement_of_specials('exp[]') == False
    assert bad_placement_of_specials('3[x+y]^[7sqrt[xy]]') == False

    assert bad_placement_of_specials('{}') == False
    assert bad_placement_of_specials('exp{}') == False

    assert bad_placement_of_specials('3(x+y)^(7sqrt(xy)') == True
    assert bad_placement_of_specials('3(x+y^(7sqrt(xy)') == True
    assert bad_placement_of_specials('3((((x+y^(7sqrt(xy)') == True
    assert bad_placement_of_specials('3( (  (  (x+y^(7sqrt(xy)') == True

    assert bad_placement_of_specials('3[x+y]^[7sqrt[xy]') == True
    assert bad_placement_of_specials('3[x+y^[7sqrt[xy]') == True
    assert bad_placement_of_specials('3[[[[x+y^[7sqrt[xy]') == True
    assert bad_placement_of_specials('3[ [  [  [x+y^[7sqrt[xy]') == True

    # parentheses levels become negative (you close more than you open)
    assert bad_placement_of_specials('3(x+y)))^(7sqrt(xy)') == True
    assert bad_placement_of_specials('3(x+y) ) )^(7sqrt(xy)') == True

    assert bad_placement_of_specials('3[x+y]]]^[7sqrt[xy]') == True
    assert bad_placement_of_specials('3[x+y] ] ]^[7sqrt[xy]') == True

    assert bad_placement_of_specials('exp)(') == True
    assert bad_placement_of_specials('exp][') == True
    assert bad_placement_of_specials('exp}{') == True
    assert bad_placement_of_specials('exp}log{xyz') == True

    # nested curly brackets not allowed
    assert bad_placement_of_specials('x=5 {x < 3 {y=5} }') == True
    assert bad_placement_of_specials('{{}}') == True
    assert bad_placement_of_specials('{x<5}{y<5}') == False

    # specials that are not allowed within round parentheses
    assert bad_placement_of_specials('f(x,y)=3') == False
    assert bad_placement_of_specials('f(x;y)=3') == True

    assert bad_placement_of_specials('exp(x,y)') == False
    assert bad_placement_of_specials('exp(3 & 5)') == True
    assert bad_placement_of_specials('exp(35) & log(21)') == False
    assert bad_placement_of_specials('exp(x;y)') == True
    assert bad_placement_of_specials('exp(xy) & log (x+y)') == False
    assert bad_placement_of_specials('exp(x ; y)') == True
    assert bad_placement_of_specials('exp(x{x<5})') == True
    assert bad_placement_of_specials('exp(x){x<5}') == False
    assert bad_placement_of_specials('exp(x{y})') == True

    # specials that are not allowed within square parentheses
    assert bad_placement_of_specials('log([1,2,3])') == False
    assert bad_placement_of_specials('log([1,2,3 & 5])') == True
    assert bad_placement_of_specials('log([1,2,3, 5]) & exp([1])') == False
    assert bad_placement_of_specials('[1,2,3;4,5,6;7,8,9]') == False
    assert bad_placement_of_specials('[3x,3y,x^{y+3}]') == True
    assert bad_placement_of_specials('[3x,3y,x^(y+3)]') == False
    assert bad_placement_of_specials('[3x,3y,x^(y+3)]{xy<3,x%3=2}') == False

    # wrong placements of '_', '.', '\'' or '`'
    assert bad_placement_of_specials('xyz.w') == True
    assert bad_placement_of_specials('xyzw.') == True
    assert bad_placement_of_specials('3._') == True
    assert bad_placement_of_specials('3..') == True
    assert bad_placement_of_specials('x.+') == True
    assert bad_placement_of_specials('x.3') == True
    assert bad_placement_of_specials('(x+1).3') == True

    assert bad_placement_of_specials('3.') == False
    assert bad_placement_of_specials('.3') == False
    assert bad_placement_of_specials('3.(x)') == False
    assert bad_placement_of_specials('(x+1)*.3') == False
    assert bad_placement_of_specials('x+(.3y)') == False
    assert bad_placement_of_specials('.1*33.x+.3y+4.7*4.') == False

    assert bad_placement_of_specials('_help') == True
    assert bad_placement_of_specials('_3help') == True
    assert bad_placement_of_specials('xy_') == True
    assert bad_placement_of_specials('x+3_3') == True
    assert bad_placement_of_specials('x+3_y') == True
    assert bad_placement_of_specials('x_x') == True
    assert bad_placement_of_specials('3_3') == True
    assert bad_placement_of_specials('x_.') == True
    assert bad_placement_of_specials('x_)') == True
    assert bad_placement_of_specials('x_(') == True

    assert bad_placement_of_specials('x_3') == False
    assert bad_placement_of_specials('exp(x_3)') == False
    assert bad_placement_of_specials('a_1b_2c_3d_4') == False

    assert bad_placement_of_specials('x`') == False
    assert bad_placement_of_specials('3`') == False
    assert bad_placement_of_specials('3`+3`+3`x`') == False
    assert bad_placement_of_specials('(1/sqrt(exp(3x)))`') == False
    assert bad_placement_of_specials('(1/sqrt(exp(3x)))``') == False

    assert bad_placement_of_specials('`') == True
    assert bad_placement_of_specials('`x') == True
    assert bad_placement_of_specials('x+_`') == True
    assert bad_placement_of_specials('x+.`') == True
    assert bad_placement_of_specials('x+`') == True
    assert bad_placement_of_specials('x%`') == True

    assert bad_placement_of_specials('x\'') == False
    assert bad_placement_of_specials('3\'') == False
    assert bad_placement_of_specials('3\'+3\'+3\'x\'') == False
    assert bad_placement_of_specials('(1/sqrt(exp(3x)))\'') == False
    assert bad_placement_of_specials('(1/sqrt(exp(3x)))\'\'') == False

    assert bad_placement_of_specials('\'') == True
    assert bad_placement_of_specials('\'x') == True
    assert bad_placement_of_specials('x+_\'') == True
    assert bad_placement_of_specials('x+.\'') == True
    assert bad_placement_of_specials('x+\'') == True
    assert bad_placement_of_specials('x%\'') == True

    # general
    assert bad_placement_of_specials('exp(x_1)+log[y_1]{x<3.7}{y<3.8},(sqrt(a))\';(x_3^2)`=0 & a=7') == False

def test_invalid_func_arguments():
    assert invalid_func_args('log(3)') == False
    assert invalid_func_args('log[3]') == True
    assert invalid_func_args('log{3}') == True
    assert invalid_func_args('log([3])') == True
    assert invalid_func_args('log([1,2,3])') == True
    assert invalid_func_args('log3(5)') == True
    assert invalid_func_args('log(x<5)') == True
    assert invalid_func_args('log(x)<5') == False
    assert invalid_func_args('log(x)=5') == False
    assert invalid_func_args('log(x,y)') == True
    assert invalid_func_args('log(x;y)') == True
    assert invalid_func_args('log(x&y)') == True
    assert invalid_func_args('exp(x + 3y {x<y})') == True
    assert invalid_func_args('log(exp(sqrt(sin(cos(x)))))') == False
    assert invalid_func_args('1+log(1+exp(1+sqrt(1+sin(1+cos(x)))))') == False
    assert invalid_func_args(' 1 + log( 1 + exp( 1 + sqrt( 1 + sin( 1 + cos( x )))))') == False

def test_incorrect_character_order():

    # alpha group interrupted by more than or 2 digits
    assert incorrect_character_order('') == False
    assert incorrect_character_order('xyz') == False
    assert incorrect_character_order('xyz w+') == False
    assert incorrect_character_order('xyz w  %') == False
    assert incorrect_character_order('x / y / z /  w  %') == False
    assert incorrect_character_order('x+2yw^3zw') == False
    assert incorrect_character_order('a2') == False
    assert incorrect_character_order('a 2 + a 3') == False
    assert incorrect_character_order('x1y1z1w1') == False
    assert incorrect_character_order('3.7x+y/3.7') == False
    assert incorrect_character_order('x1+x2+x3+x4+x5') == False
    assert incorrect_character_order('x23yz') == True
    assert incorrect_character_order('xyzw1234') == True
    assert incorrect_character_order('xy 23 5 w') == False  # function does not clear whitespaces on its own

    # 'x+=3'

    # 'x+(=3)'

    # 'x(=2)'

def test_valid_string_input():
    # general equations
    assert valid_string_input('') == False
    assert valid_string_input('       ') == False
    assert valid_string_input('x+3') == True
    assert valid_string_input('mx+n') == True
    assert valid_string_input('x^3+x^2+x+1') == True
    assert valid_string_input('ax^3+bx^2+cx+d') == True
    assert valid_string_input('0 <= ax^3+bx^2+cx+d <= (log(x) + exp(x) + sqrt(x))^(x^x)') == True
    assert valid_string_input('0 <= ax^3+bx^2+cx+d <= (log(x) + exp(x) + sqrt(x))^(x^x)'.upper()) == True
    assert valid_string_input('13x_1x_2x_3x_4x_5x_6+19x^4+x_3%11') == True

    """
    ------------group by functionality------------
    """

    # expression ends with a sign
    assert valid_string_input('+') == False
    assert valid_string_input('x+') == False
    assert valid_string_input('xyz +') == False
    assert valid_string_input('xyz + t%') == False

    assert valid_string_input('xyz^3 + t%3') == True

    # 2 consecutive signs (except +-)
    assert valid_string_input('a-+b') == False
    assert valid_string_input('a*/b') == False
    assert valid_string_input('a% ^b') == False

    assert valid_string_input('1+3') == True
    assert valid_string_input('x+-3') == True
    assert valid_string_input('xyz+-xyz') == True

    # 2 forbidden consecutive relational operators
    assert valid_string_input('x<<3') == False
    assert valid_string_input('x >>3') == False
    assert valid_string_input('x  >>3') == False
    assert valid_string_input('x  =<3') == False
    assert valid_string_input('x  =>3') == False
    assert valid_string_input('x  ==3') == False

    assert valid_string_input('x<=3') == True
    assert valid_string_input('x   >=3') == True
    assert valid_string_input('0<1<2<3<4') == True
    assert valid_string_input('x>=y>=z>=w>=t') == True

    # non-supported special characters
    assert valid_string_input('$$ x<3 $$ @! ') == False

    # too many consecutive letters not in funcs
    assert valid_string_input('paper straw') == False
    assert valid_string_input('1+straw') == False
    assert valid_string_input('xyzwt = 0') == False
    assert valid_string_input('1+xyzwt') == False
    assert valid_string_input('1+xyzwt ') == False
    assert valid_string_input('1+arctan(77)') == True

    # alpha groups are interrupted  (e.g. 'x23y' )
    assert valid_string_input('xyz') == True
    assert valid_string_input('xyz w+3') == True
    assert valid_string_input('xyz w  %3') == True
    assert valid_string_input('x / y / z /  w  % 3') == True
    assert valid_string_input('x+2yw^3zw') == True
    assert valid_string_input('a2') == True
    assert valid_string_input('a 2 + a 3') == True
    assert valid_string_input('x1y1z1w1') == True
    assert valid_string_input('3.7x+y/3.7') == True
    assert valid_string_input('x1+x2+x3+x4+x5') == True

    assert valid_string_input('x23yz') == False
    assert valid_string_input('xyzw1234') == False
    assert valid_string_input('xy 23 5 w') == False

    """
    ------------group by character order------------
    """

    # signs
    assert valid_string_input('+') == False
    assert valid_string_input('    +') == False
    assert valid_string_input('+     ') == False
    assert valid_string_input('-') == False
    assert valid_string_input('*') == False
    assert valid_string_input('/') == False
    assert valid_string_input('^') == False
    assert valid_string_input('%') == False

    # relationals
    assert valid_string_input('<') == False
    assert valid_string_input('>') == False
    assert valid_string_input('=') == False
    assert valid_string_input('<=') == False
    assert valid_string_input('>=') == False

    # alphas

    # nums

    # specials

    # parentheses

    # round-robin

    assert valid_string_input('x+=3') == False
    assert valid_string_input('x+(=3)') == False
    assert valid_string_input('x(=2)') == False


if __name__ == '__main__':
    pass
    # test_parenthesis_levels()
    # test_remove_whitespaces()
    # test_consecutive_signs()
    # test_consecutive_relationals()
    # test_alpa_group_interrupted()
    # test_invalid_alpha_group()
    # test_valid_string_input()
