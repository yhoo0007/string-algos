# Ho Yi Ping
# This file contains all the code for question 3 (Modified KMP). Run the
# file from commnad line via: python modified_kmp.py <text_file> <pattern_file> This program will
# write its output to a file named 'output_kmp.txt' in the same directory as the script.


import sys


ALPHABET = [chr(i) for i in range(128)]  # all ascii characters


def z_algo(string):
    '''
    Performs Gusfield's Z-algorithm on the given string and returns the resulting Z-array.
        string: String of characters as input to the Z-algorithm.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'string'
    '''
    if not hasattr(string, '__len__'):
        string = list(string)

    n = len(string)
    if n == 0:
        return []

    z = [0 for _ in range(n)]
    z[0] = n

    l, r = 0, 0
    for i in range(1, n):
        if i > r:  # case 1 : i not in zbox, explicit comparisons until mismatch is found
            j = i
            while j < n and string[j] == string[j - i]:
                z[i] += 1
                j += 1

            if z[i] > 0:  # form zbox if number of matches > 0
                l, r = i, j - 1
        else:
            k = i - l
            remaining = r - i + 1
            if z[k] < remaining:  # case 2a : z[k] < remaining
                z[i] = z[k]

            elif z[k] > remaining:  # case 2b : z[k] > remaining
                z[i] = remaining

            else:  # case 2c : z[k] = remaining, explicit comparisons from r + 1 until mismatch is found
                z[i] = z[k]
                matches = 0
                j = r + 1
                k = z[i]
                while j < n and string[j] == string[k]:
                    z[i] += 1
                    matches += 1
                    j += 1
                    k += 1

                if matches > 0:  # form new zbox if number of matches > 0
                    l, r = i, j - 1
    return z


def get_spx(pat):
    '''
    Returns a 2D spix lookup table to be used in the KMP algorithm. Lookup table is computed
    running z algorithm on the given string and placing the z values into a 2D lookup table such
    that they can be looked up by the mismatched character.
        pat:    String of characters representing pattern to be processed
    '''
    m = len(pat)
    spx = [None for _ in range(len(ALPHABET))]
    z_array = z_algo(pat)
    for j in range(m - 1, 0, -1):
        if z_array[j] > 0:
            i = j + z_array[j] - 1
            char_idx = ord(pat[z_array[j]])
            if spx[char_idx] is None:  # only allocate array of necessary letters
                spx[char_idx] = [-1 for _ in range(len(pat) + 1)]
            spx[char_idx][i] = z_array[j]
    return spx


def kmp(pat, text):
    '''
    Returns a list of starting indices of all occurrences of pat in text. Search is performed using
    the KMP algorithm with spix lookup table.
        pat:    String of characters representing pattern to search for
        text:   String of characters representing text to search in
        Time:   O(n + m)
        Space:  O(n + m)
            where:
                n = |text|
                m = |pat|
    '''
    if len(pat) == 0:
        return [0]
    
    n = len(text)
    m = len(pat)
    spx = get_spx(pat)
    i = 0  # denotes start of pattern
    j = m  # denotes end of pattern
    k = 0
    occ = []
    while j <= n:  # compare chars left to right
        global_index = i + k
        if k >= m:  # full match found
            occ.append(i)
            if global_index < n:  # not at end of text
                global_char = text[global_index]
                try:  # lookup shift value from spix table
                    spi = spx[ord(global_char)][-2]
                except TypeError:
                    spi = -1
                if spi == -1 and global_char == pat[0]:  # special case
                    spi = 0
                shift = k - spi
                k -= shift + 1
                i += shift
                j += shift
                continue
            else:
                break

        if pat[k] != text[global_index]:
            global_char = text[global_index]
            try:  # lookup shift value from spix table
                spi = spx[ord(global_char)][k - 1]
            except TypeError:
                spi = -1
            if spi == -1 and global_char == pat[0]:  # special case
                spi = 0
            shift = k - spi
            k = k - shift + 1
            i += shift
            j += shift
            continue
        k += 1
    return occ


if __name__ == '__main__':
    text_file, pat_file = sys.argv[1:]
    # text_file, pat_file = './29352258/q3/txt1.txt', './29352258/q3/pat1.txt'

    with open(text_file) as f:
        text = f.read()
    
    with open(pat_file) as f:
        pat = f.read()

    results = kmp(pat, text)
    with open('output_kmp.txt', 'w') as f:
        f.writelines(map(lambda res: f'{res + 1}\n', results))
