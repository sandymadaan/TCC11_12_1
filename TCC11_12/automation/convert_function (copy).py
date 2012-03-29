#!/usr/bin/env python
'''Convert number to English words
$./num2eng.py 1411893848129211
one quadrillion, four hundred and eleven trillion, eight hundred and ninety
three billion, eight hundred and forty eight million, one hundred and twenty
nine thousand, two hundred and eleven
$
 
Algorithm from http://mini.net/tcl/591
'''
 
# modified to exclude the "and" between hundreds and tens - mld
 
__author__ = 'Miki Tebeka <tebeka@cs.bgu.ac.il>'
__version__ = '$Revision: 7281 $'
 
# $Source$
 
import math
 
# Tokens from 1000 and up
_PRONOUNCE = [
    'vigintillion',
    'novemdecillion',
    'octodecillion',
    'septendecillion',
    'sexdecillion',
    'quindecillion',
    'quattuordecillion',
    'tredecillion',
    'duodecillion',
    'undecillion',
    'decillion',
    'nonillion',
    'octillion',
    'septillion',
    'sextillion',
    'quintillion',
    'quadrillion',
    'trillion',
    'billion',
    'Million ',
    'Thousand ',
    ''
]
 
# Tokens up to 90
_SMALL = {
    '0' : '',
    '1' : 'One',
    '2' : 'Two',
    '3' : 'Three',
    '4' : 'Four',
    '5' : 'Five',
    '6' : 'Six',
    '7' : 'Seven',
    '8' : 'Eight',
    '9' : 'Nine',
    '10' : 'Ten',
    '11' : 'Eleven',
    '12' : 'Twelve',
    '13' : 'Thirteen',
    '14' : 'Fourteen',
    '15' : 'Fifteen',
    '16' : 'Sixteen',
    '17' : 'Seventeen',
    '18' : 'Eighteen',
    '19' : 'Nineteen',
    '20' : 'Twenty',
    '30' : 'Thirty',
    '40' : 'Forty',
    '50' : 'Fifty',
    '60' : 'Sixty',
    '70' : 'Seventy',
    '80' : 'Eighty',
    '90' : 'Ninety'
}
 
def get_num(num):
    '''Get token <= 90, return '' if not matched'''
    return _SMALL.get(num, '')
 
def triplets(l):
    '''Split list to triplets. Pad last one with '' if needed'''
    res = []
    for i in range(int(math.ceil(len(l) / 3.0))):
        sect = l[i * 3 : (i + 1) * 3]
        if len(sect) < 3: # Pad last section
            sect += [''] * (3 - len(sect))
        res.append(sect)
    return res
 
def norm_num(num):
    """Normelize number (remove 0's prefix). Return number and string"""
    n = int(num)
    return n, str(n)
 
def small2eng(num):
    '''English representation of a number <= 999'''
    n, num = norm_num(num)
    hundred = ''
    ten = ''
    if len(num) == 3: # Got hundreds
        hundred = get_num(num[0]) + ' hundred'
        num = num[1:]
        n, num = norm_num(num)
    if (n > 20) and (n != (n / 10 * 10)): # Got ones
        tens = get_num(num[0] + '0')
        ones = get_num(num[1])
        ten = tens + ' ' + ones
    else:
        ten = get_num(num)
    if hundred and ten:
        return hundred + ' ' + ten
        #return hundred + ' and ' + ten
    else: # One of the below is empty
        return hundred + ten
 
#FIXME: Currently num2eng(1012) -> 'one thousand, twelve'
# do we want to add last 'and'?
def num2eng(num):
    '''English representation of a number'''
    num = str(long(num)) # Convert to string, throw if bad number
    if (len(num) / 3 >= len(_PRONOUNCE)): # Sanity check
        raise ValueError('Number too big')
 
    if num == '0': # Zero is a special case
        return 'zero'
 
    # Create reversed list
    x = list(num)
    x.reverse()
    pron = [] # Result accumolator
    ct = len(_PRONOUNCE) - 1 # Current index
    for a, b, c in triplets(x): # Work on triplets
        p = small2eng(c + b + a)
        if p:
            pron.append(p + ' ' + _PRONOUNCE[ct])
        ct -= 1
    # Create result
    pron.reverse()
    return ', '.join(pron)
 
