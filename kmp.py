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



def kmp(pat, text):
    if len(pat) == 0:
        return [0]
    
    n = len(text)
    m = len(pat)

    sp = [0 for _ in range(m + 1)]
    sp[-1] = -1
    z_array = z_algo(pat)
    for j in range(m - 1, 0, -1):
        i = j + z_array[j] - 1
        sp[i] = z_array[j]

    i = 0  # denotes start of pattern
    j = m  # denotes end of pattern
    k = 0
    occ = []
    while j <= n:  # compare chars left to right
        if k >= m:  # full match found
            occ.append(i)
            shift = k - sp[-2]
            k -= shift + 1
        elif pat[k] != text[i + k]:
            shift = k - sp[k - 1]
            if k > 0:
                k -= shift
        else:
            k += 1
            continue
        i += shift
        j += shift

    return occ


if __name__ == '__main__':
    # text_file, pat_file = sys.argv[1:]
    text_file, pat_file = './29352258/q3/txt1.txt', './29352258/q3/pat1.txt'

    with open(text_file) as f:
        text = f.read()
    
    with open(pat_file) as f:
        pat = f.read()

    print('Text:', text)
    print('Pat: ', pat)

    # BM to find all occurrances of pat in text
    print(kmp(pat, text))
