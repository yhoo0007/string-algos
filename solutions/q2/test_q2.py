# Ho Yi Ping
# Test suite for question 2 (Wildcard Matching).


import unittest
import re
import random
from wildcard_matching import find_all


def load_test_files():
    with open('./test/reference.txt') as f:
        text = f.read()
    
    with open('./test/pattern1.txt') as f:
        pat1 = f.readlines()
    
    with open('./test/pattern2.txt') as f:
        pat2 = f.readlines()
    return text, pat1, pat2


def insert_random_wildcards(string):
    pattern = list(string.strip())
    for _ in range(random.randint(0, len(pattern)-1)):
        pattern[random.randint(0, len(pattern)-1)] = '?'
    pattern = ''.join(pattern)
    re_pattern = ''.join(['.' if c == '?' else c for c in pattern])
    return pattern, re_pattern


class TestFindAll(unittest.TestCase):
    def subcase(self, n, actual, expected):
        print('Subcase', n)
        self.assertEqual(actual, expected)

    def test_empty(self):
        print('\nTest Empty')
        self.subcase(1, find_all('', ''), [0])

    def test_empty_text(self):
        print('\nTest Empty Text')
        self.subcase(1, find_all('abc', ''), [])
        self.subcase(2, find_all('aaa', ''), [])
        self.subcase(3, find_all('aa?', ''), [])

    def test_empty_pat(self):
        print('\nTest Empty Pat')
        self.subcase(1, find_all('', 'abc'), [0])
        self.subcase(2, find_all('', 'aaa'), [0])

    def test_match_prefix(self):
        print('\nTest Match Prefix')
        self.subcase(1, find_all('aa', 'aab'), [0])
        self.subcase(2, find_all('ab', 'abb'), [0])
        self.subcase(3, find_all('a?', 'abb'), [0])
        self.subcase(4, find_all('??', 'aba'), [0, 1])
        self.subcase(5, find_all('?b', 'aba'), [0])
    
    def test_match_suffix(self):
        print('\nTest Match Suffix')
        self.subcase(1, find_all('ba', 'aba'), [1])
        self.subcase(2, find_all('aa', 'baa'), [1])
        self.subcase(3, find_all('b?', 'aba'), [1])
        self.subcase(4, find_all('??', 'aba'), [0, 1])
        self.subcase(5, find_all('?a', 'aba'), [1])
    
    def test_match_exact(self):
        print('\nTest Match Exact')
        self.subcase(1, find_all('aba', 'aba'), [0])
        self.subcase(2, find_all('aaa', 'aaa'), [0])
        self.subcase(3, find_all('a', 'a'), [0])
        self.subcase(4, find_all('?', 'a'), [0])
        self.subcase(5, find_all('???', 'aba'), [0])
        self.subcase(6, find_all('a?a', 'aba'), [0])

    def test_match_middle(self):
        print('\nTest Match Middle')
        self.subcase(1, find_all('aa', 'aaaaa'), [0, 1, 2, 3])
        self.subcase(2, find_all('aa', 'baab'), [1])
        self.subcase(3, find_all('bac', 'cbacd'), [1])
        self.subcase(4, find_all('b?c', 'cbacd'), [1])
        self.subcase(5, find_all('b??', 'cbacd'), [1])
        self.subcase(6, find_all('??c', 'cbacd'), [1])
        self.subcase(7, find_all('?a?', 'cbacd'), [1])

    def test_pat1(self):
        print('\nTest Pat 1')
        text, pat1, _ = load_test_files()

        # test all patterns in pat1
        for index, pat in enumerate(pat1):
            if index % 10 == 0:
                print(f'{index}/{len(pat1)}')
            expected = [m.start() for m in re.finditer(f'(?={pat.strip()})', text)]

            try:
                actual = find_all(pat.strip(), text)
            except KeyboardInterrupt as e:
                print(index, pat)
                raise e
            
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pat)
                raise e
        print(f'{len(pat1)}/{len(pat1)}')

    def test_pat2(self):
        print('\nTest Pat 2')
        text, _, pat2 = load_test_files()
        
        # test all patterns in pat2
        for index, pat in enumerate(pat2):
            if index % 10 == 0:
                print(f'{index}/{len(pat2)}')
            expected = [m.start() for m in re.finditer(f'(?={pat.strip()})', text)]

            try:
                actual = find_all(pat.strip(), text)
            except KeyboardInterrupt as e:
                print(index, pat)
                raise e
            
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pat)
                raise e
        print(f'{len(pat2)}/{len(pat2)}')

    def test_pat1_wildcard(self):
        print('\nTest Pat 1 Randomized Wildcards')
        random.seed(1)
        
        text, pat1, _ = load_test_files()

        # test all patterns in pat1 with random wildcard(s) inserted
        for index, pat in enumerate(pat1):
            if index % 10 == 0:
                print(f'{index}/{len(pat1)}')
            pattern, re_pattern = insert_random_wildcards(pat)
            expected = [m.start() for m in re.finditer(f'(?={re_pattern})', text)]

            try:
                actual = find_all(pattern, text)
            except KeyboardInterrupt as e:
                print(index, pattern, re_pattern)
                raise e
            
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pattern, re_pattern)
                raise e
        print(f'{len(pat1)}/{len(pat1)}')

    def test_pat2_wildcard(self):
        print('\nTest Pat 2 Randomized Wildcards')
        random.seed(2)
        
        text, _, pat2 = load_test_files()

        # test all patterns in pat1 with random wildcard(s) inserted
        for index, pat in enumerate(pat2):
            if index % 10 == 0:
                print(f'{index}/{len(pat2)}')
            pattern, re_pattern = insert_random_wildcards(pat)
            expected = [m.start() for m in re.finditer(f'(?={re_pattern})', text)]

            try:
                actual = find_all(pattern, text)
            except KeyboardInterrupt as e:
                print(index, pattern, re_pattern)
                raise e
            
            try:
                self.assertEqual(actual, expected)
            except AssertionError as e:
                print(index, pattern, re_pattern)
                raise e
        print(f'{len(pat2)}/{len(pat2)}')


if __name__ == '__main__':
    op = input('1: unit test\n2: profile\n3: time\n4: scalability\n> ')
    text, pat1, pat2 = load_test_files()
    
    if op == '1':
        unittest.main(failfast=True)
        
    elif op == '2':
        import cProfile
        pat = pat1[0].strip()
        pat = '?TT??TAT'
        cProfile.run('find_all(pat, text)')
        
    elif op == '3':
        from timeit import default_timer as timer
        time_taken = timer()
        for pat in pat1:
            find_all(pat.strip(), text)
        time_taken = timer() - time_taken
        print('Time taken:', time_taken)
    
    elif op == '4':
        from timeit import default_timer as timer
        random.seed(0)
        test_text = text * 2
        for len_pat in [4, 8, 12]:
            times = []
            print(f'|pat| = {len_pat}')
            for i in range(100_000, 1_000_000, 100_000):
                print('Testing n =', i)
                t = test_text[:i]
                
                patterns = [insert_random_wildcards(pat)[0] for pat in pat1]
                patterns = [(pat.strip()*2)[:len_pat] for pat in patterns]

                start = timer()
                for pat in patterns:
                    find_all(pat, t)
                times.append((i, (timer() - start)/len(pat1)))
            print('Example pats:', patterns[:5])
            print('Results:')
            for n, t in times:
                print(n, t)
        
    else:
        print('invalid op')

