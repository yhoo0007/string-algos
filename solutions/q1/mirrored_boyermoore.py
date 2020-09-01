# Ho Yi Ping
# This file contains all the code for question 1 (Mirrored Boyermoore). Run
# the file from commnad line via: python mirrored_boyermoore.py <text_file> <pattern_file> This
# program will write its output to a file named 'output_mirrored_boyermoore.txt' in the same
# directory as the script.


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

            else:  # case 2c : z[k] = remaining, explicit comparisons from r + 1
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


def get_bad_char_lookup(pat):
    '''
    Returns 2D lookup table to be used in the 'bad character' rule of the mirrored Boyer Moore
    algorithm. Looking up a pattern shift will never return a value less than 1 given the lookup
    character is not the same as the character in the pattern at that position (in which case there
    should not be shifting anyway).
        pat:        String of letters representing the pattern to be used in lookup table 
                    generation.
        Time: O(m)
        Space: O(m)
            where:
            m = length of 'pat'
    '''
    lookup_table = [None for _ in range(len(ALPHABET))]
    for index, char in enumerate(reversed(pat)):
        for i in range(len(lookup_table)):
            row = lookup_table[i]
            if i == ord(char):
                if row is None:
                    lookup_table[i] = [len(pat) for _ in range(len(pat))]
                lookup_table[i][- index - 1] = len(pat) - index - 1
            elif row is not None:
                lookup_table[i][- index - 1] = row[- index]
    return lookup_table


def get_good_prefix_lookup(pat):
    '''
    Returns the lookup table to be used in the 'good prefix' rule of the mirrored Boyer Moore
    algorithm. Each value (v) in the lookup table is such that len(pat) - v = rightwards shift of
    pattern possible such that the already matched characters in pat align with those in the text.
        pat:    String of characters to generate lookup table for.
        Time:   O(m)
        Space:  O(m)
            where:
            m = length of 'pat'
    '''
    z_suffix = z_algo(pat)
    m = len(pat)
    good_prefix = [0 for _ in range(m + 1)]
    for p in range(m - 1, 0, -1):
        good_prefix[z_suffix[p]] = m - p
    
    return good_prefix


def get_matched_suffix(pat):
    '''
    Returns the 'matched suffix' lookup table to be used in the mirrored Boyer Moore algorithm.
    Each value (v) in the lookup table represents the length of the longest prefix that matches the
    suffix of pat.
        pat:    String of characters to generate lookup table for.
        Time:   O(m)
        Space:  O(m)
            where:
            m = length of 'pat'
    '''
    m = len(pat)
    z_array = z_algo(reversed(pat))
    matched_suffix = [0 for _ in range(m + 1)]
    for i in range(m):
        matched_suffix[i + 1] = z_array[
            m - i - 1
        ] if z_array[m - i - 1] - i == 1 else matched_suffix[i]

        # limit max value of mp such that m - mp will always be at least 1
        if matched_suffix[i + 1] > m - 1:
            matched_suffix[i + 1] = m - 1
    
    return matched_suffix


def mirrored_boyermoore(pat, text):
    '''
    Finds the starting index of all occurrances of pat in text using mirrored Boyer Moore's
    algorithm.
        pat:    String of characters representing pattern to search for.
        text:   String of characters representing text to search in.
        Time:   O(n + m) worst case
        Space:  O(n + m)
            where:
            n = length of 'text'
            m = length of 'pat'
    '''
    if len(pat) == 0:
        return [0]

    bad_char = get_bad_char_lookup(pat)
    good_prefix = get_good_prefix_lookup(pat)
    matched_suffix = get_matched_suffix(pat)

    occ = []
    j = len(text) - 1  # denotes (right) start of pat relative to text (inclusive)
    m = len(pat)  # denotes length of pat
    i = j - m  # denotes (left) end of pat relative to text (non inclusive)
    k = 0  # denotes current index relative to pat
    galil_br = -1  # denotes breakpoint for Galil's optimization relative to text
    galil_rs = -1  # denotes resume point for Galil's optimization relative to text
    bc_row = None  # cache storage of row of previous bad char lookup
    previous_char = None
    while i >= -1:
        if k >= m:  # full match found
            occ.append(j - m + 1)
            shift = m - matched_suffix[-2]
            j -= shift
            i -= shift
            k = 0
            continue

        global_index = i + k + 1
        if global_index == galil_br:  # galil's optimization
            galil_br = -1  # prevents endless resuming at galil_rs
            k = galil_rs - i - 1
            continue

        current_char = text[global_index]
        if current_char == pat[k]:
            k += 1
        else:
            try:
                if current_char != previous_char:
                    bc_row = bad_char[ord(current_char)]
                    previous_char = current_char
                bc = bc_row[k] - k
            except TypeError:
                bc = m - k  # bad char does not exist in pat, therefore shift entire pat length
            gp = good_prefix[k]
            gp = m - matched_suffix[k - 1] if gp == 0 else m - gp

            # shift by bc or gp depending on which provides a larger shift
            if bc > gp:
                shift = bc
                galil_br = global_index
                galil_rs = global_index
            else:
                shift = gp
                galil_br = i + 1
                galil_rs = global_index

            j -= shift
            i -= shift
            k = 0
    return occ


if __name__ == '__main__':
    text_file, pat_file = sys.argv[1:]

    with open(text_file) as f:
        text = f.read()
    
    with open(pat_file) as f:
        pat = f.read()

    results = mirrored_boyermoore(pat, text)
    with open('output_mirrored_boyermoore.txt', 'w') as f:
        f.writelines(map(lambda res: f'{res + 1}\n', reversed(results)))
