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
    for i in range(1, len(z)):
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


def get_bad_char_lookup(pat):
    '''
    Returns 2D lookup table to be used in the 'bad character' rule of the Boyer Moore algorithm.
    Looking up a pattern shift will never return a value less than 1 if the lookup character is 
    not the same as the character in the pattern at that position (in which case you should
    not be shifting anyway).
        pat:    String of characters representing the pattern to be used in lookup table 
                generation.
        Time:   O(m)
        Space:  O(m)
            where:
            m = length of 'pat'
    '''
    lookup_table = [None for _ in range(len(ALPHABET))]  # O(|alphabet|) time, upper bound of O(|alphabet| * m) space
    for index, char in enumerate(pat):  # O(m) time
        for i in range(len(lookup_table)):  # O(|alphabet|) time
            row = lookup_table[i]
            if chr(i) == char:
                if row is None:
                    lookup_table[i] = [-1 for _ in range(len(pat))]  # O(m) size array created at most |alphabet| times
                lookup_table[i][index] = index
            elif row is not None:
                lookup_table[i][index] = row[index-1]
    return lookup_table


def get_good_suffix_lookup(pat):
    '''
    Returns the lookup table to be used in the 'good suffix' rule of the Boyer Moore algorithm. 
    Each value (v) in the lookup table is such that len(pat) - v = leftwards shift of pattern 
    possible such that the already matched characters in pat align with the text.
        pat:    String of characters to generate lookup table for.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'pat'
    '''
    z_suffix = list(reversed(z_algo(reversed(pat))))
    m = len(pat)
    good_suffix = [0 for _ in range(m + 1)]
    for p in range(m - 1):  # zs[-1] is always len(pat), hence gs[0] is always len(pat) - 1, but gs[0] is never lookup anyway
        good_suffix[m - z_suffix[p]] = p + 1
    
    return good_suffix


def get_matched_prefix(pat):
    '''
    Returns the 'matched prefix' lookup table to be used in the Boyer Moore algorithm. Each value 
    (v) in the lookup table represents the length of the longest suffix that matches the prefix of 
    pat.
        pat:    String of characters to generate lookup table for.
        Time:   O(n)
        Space:  O(n)
            where:
            n = length of 'pat'
    '''
    z_array = z_algo(pat)
    matched_prefix = [0 for _ in range(len(pat) + 1)]
    for i in range(len(pat) - 1, -1, -1):
        matched_prefix[i] = z_array[i] if z_array[i] + i == len(pat) else matched_prefix[i + 1]

        if matched_prefix[i] > len(pat) - 1:  # limit max value of mp such that m - mp will always be at least 1
            matched_prefix[i] = len(pat) - 1
    return matched_prefix


def count():
    '''
    Dummy function used to count the number of times a certain point in code is reached. Intended 
    to be used with CProfile.
    '''
    pass


def boyermoore(pat, text):
    '''
    Finds the starting index of all occurrances of pat in text using Boyer Moore's algorithm.
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
    good_suffix = get_good_suffix_lookup(pat)
    matched_prefix = get_matched_prefix(pat)

    occ = []
    j = 0  # denotes start of pat relative to text (inclusive)
    m = len(pat)  # denotes length of pat
    k = m - 1  # denotes current index relative to pat
    i = m  # denotes end of pat relative to text
    galil_br = -1  # denotes breakpoint for Galil's optimization relative to text
    galil_rs = -1  # denotes resume point for Galil's optimization relative to text
    n = len(text)  # denotes length of text
    bc_row = None
    previous_char = None
    while i <= n:
        # print(text)
        # print(' ' * j + pat)
        # print(' ' * (j + k) + 'k')
        if k < 0:  # full match found
            occ.append(j)
            shift = m - matched_prefix[1]
            j += shift
            i += shift
            k = m - 1  # k resets to m (end of pat)
            continue

        global_index = j + k
        if global_index == galil_br:  # galil's optimization
            galil_br = -1
            k = galil_rs - j
            continue

        current_char = text[global_index]
        if current_char == pat[k]:
            k -= 1
        else:
            try:
                if current_char != previous_char:
                    bc_row = bad_char[ord(current_char)]
                    previous_char = current_char
                bc = k - bc_row[k]
            except TypeError:
                bc = k + 1  # bad char does not exist in pat, therefore shift entire pat length
            gs = good_suffix[k + 1]
            gs = m - matched_prefix[k + 1] if gs == 0 else m - gs

            if bc > gs:  # shifting by bad character
                shift = bc
                galil_br = global_index
                galil_rs = galil_br
            else:  # shifting by good suffix
                shift = gs
                galil_br = i - 1  # break value for Galil's optimization
                galil_rs = global_index  # resume value for Galil's optimization
            
            j += shift
            i += shift
            k = m - 1  # k resets to m (end of pat)

    return occ


if __name__ == '__main__':
    # text_file, pat_file = sys.argv[1:]
    text_file, pat_file = './29352258/q1/txt1.txt', './29352258/q1/pat1.txt'

    with open(text_file) as f:
        text = f.read()
    
    with open(pat_file) as f:
        pat = f.read()

    print('Text:', text)
    print('Pat: ', pat)

    # BM to find all occurrances of pat in text
    print(boyermoore(pat, text))
