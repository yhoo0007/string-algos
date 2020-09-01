# Ho Yi Ping
# This file contains all the code for question 2 (Wildcard Matching). Run
# the file from commnad line via: python wildcard_matching.py <text_file> <pattern_file> This
# program will write its output to a file named 'output_wildcard_matching.txt' in the same
# directory as the script.


import sys


def z_algo_special(sections, text, max_section_len, total_len):
    '''
    Returns a z array of a pattern $ text where the pattern is comprised of the strings and the
    wildcard lengths in the 'sections' parameter.
        sections:           Iterable of (wildcard_length, section) pairs that make up the pattern
        text:               Text to search in
        max_section_len:    Length of the longest section
        total_len:          Length of the longest section + length of text + 1
        Time:   O(nm/2)
        Space:  O(n + m)
            where:
                n = |text|
                m = |pattern|
                x = |sections| <= m/2 e.g. a?a?a?a
    '''
    # initialize arrays and variables
    z_final = [0] * total_len
    max_section_sep_len = max_section_len + 1
    search_string = ['$'] * (max_section_sep_len) + list(text)

    # run z algo on every <section> + <text>
    for wildcard_len, section in sections:
        # swap current section into search string
        section_len = len(section)
        search_string[:max_section_len] = section + ['$'] * (max_section_len - section_len)
        
        # reset z array
        z = [0] * total_len

        # reset 0:max_section_length of z_final so that z values for section are computed
        z_final[:max_section_sep_len] = [0] * (max_section_sep_len)

        # calculate z values of all required indices
        l, r = 0, 0
        for idx, val in enumerate(z_final):
            i = val + idx  # index of z value needed
            if i == 0:  # don't need to calculate z value at index 0
                continue
            if i >= total_len:  # or if out of range
                break
            if i > r:  # case 1: not in zbox
                j = i
                while j < total_len and search_string[j] == search_string[j - i]:
                    z[i] += 1
                    j += 1
                if z[i] > 0:  # form new zbox if number of matches > 0
                    l, r = i, j - 1
            else:
                k = i - l
                remaining = r - i + 1
                if z[k] < remaining:  # case 2a
                    z[i] = z[k]
                elif z[k] > remaining:  # case 2b
                    z[i] = remaining
                else:  # case 2c
                    z[i] = z[k]
                    matches = 0
                    j = r + 1
                    k = z[i]
                    while j < total_len and search_string[j] == search_string[k]:
                        z[i] += 1
                        j += 1
                        k += 1
                        matches += 1
                    if matches > 0:  # form new zbox if number of matches > 0
                        l, r = i, j - 1
            # z value for index i has been computed, add it to z_final with wildcard_len
            z_final[idx] = val + z[i] + wildcard_len
    return z_final


def get_sections(pat):
    '''
    Processes the given pattern and splits it into sections based on wildcards. Also pairs each
    section with the number of wildcards after it.
        pat:    String of characters
        Time:   O(m) (with list.append as O(1) amortized time complexity)
        Space:  O(m)
        where:
            m = |pat|
    '''
    sections = []
    current_len = 0
    current_str = []
    prev_char = None
    for c in pat:
        if c != '?':  # split pattern
            if prev_char == '?':
                sections.append((current_len, current_str))
                current_len = 0
                current_str = []
            current_str.append(c)
        elif c == '?':  # count stretch of wildcards
            current_len += 1
        prev_char = c
    sections.append((current_len, current_str))
    return sections


def get_max_section_len(sections):
    '''
    Returns the length of the longest section among the given sections.
        sections: Iterable of (wildcard_length, section) pairs
        Time:   O(m)
        Space:  O(1)
            where:
                m = |pattern|
    '''
    max_section_len = 0
    for _, section in sections:
        len_ = len(section)
        if len_ > max_section_len:
            max_section_len = len_
    return max_section_len


def find_all(pat, text):
    '''
    Returns a list of starting indices of all occurrences of pat in text. '?' can be used to denote
    a wildcard character. A wildcard character will match any character. Search is performed using
    Z algorithm.
        pat:    String of characters representing pattern to search for
        text:   String of characters representing text to search in
        Time:   O(nm/2)
        Space:  O(n + m)
            where:
                n = |text|
                m = |pat|
    '''
    if len(pat) == 0:
        return [0]
    
    if len(text) == 0:
        return []

    # split pattern into sections based on wildcards
    sections = get_sections(pat)

    # initialize required variables
    max_section_len = get_max_section_len(sections)
    n = max_section_len + 1 + len(text)

    # run z algorithm on every <section> + <text> and combine z values to find occurrences
    z_arr = z_algo_special(sections, text, max_section_len, n)

    # identify indices at which matches occur
    pat_len = len(pat)
    occ = [i - max_section_len - 1 for i in range(n) if z_arr[i] == pat_len and i + z_arr[i] <= n]
    return occ


if __name__ == '__main__':
    text_file, pat_file = sys.argv[1:]

    with open(text_file) as f:
        text = f.read()
    
    with open(pat_file) as f:
        pat = f.read()

    results = find_all(pat, text)
    with open('output_wildcard_matching.txt', 'w') as f:
        f.writelines(map(lambda res: f'{res + 1}\n', results))
