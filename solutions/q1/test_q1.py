# Ho Yi Ping
# Test suite for question 1 (Mirrored Boyermoore).


import unittest
import re
from mirrored_boyermoore import mirrored_boyermoore as find_all


def load_test_files():
    with open('./test/reference.txt') as f:
        text = f.read()
    
    with open('./test/pattern1.txt') as f:
        pat1 = f.readlines()
    
    with open('./test/pattern2.txt') as f:
        pat2 = f.readlines()
    return text, pat1, pat2


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

    def test_empty_pat(self):
        print('\nTest Empty Pat')
        self.subcase(1, find_all('', 'abc'), [0])
        self.subcase(2, find_all('', 'aaa'), [0])

    def test_match_prefix(self):
        print('\nTest Match Prefix')
        self.subcase(1, find_all('aa', 'aab'), [0])
        self.subcase(2, find_all('ab', 'abb'), [0])
    
    def test_match_suffix(self):
        print('\nTest Match Suffix')
        self.subcase(1, find_all('ba', 'aba'), [1])
        self.subcase(2, find_all('aa', 'baa'), [1])
    
    def test_match_exact(self):
        print('\nTest Match Exact')
        self.subcase(1, find_all('aba', 'aba'), [0])
        self.subcase(2, find_all('aaa', 'aaa'), [0])
        self.subcase(3, find_all('a', 'a'), [0])

    def test_match_middle(self):
        print('\nTest Match Middle')
        self.subcase(1, find_all('aa', 'aaaaa'), [3, 2, 1, 0])
        self.subcase(2, find_all('aa', 'baab'), [1])
        self.subcase(3, find_all('bac', 'cbacd'), [1])
    
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
                self.assertEqual(list(reversed(actual)), expected)
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
                self.assertEqual(list(reversed(actual)), expected)
            except AssertionError as e:
                print(index, pat)
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
        cProfile.run('find_all(pat, text)')
        
    elif op == '3':
        from timeit import default_timer as timer
        print(f'Timing {len(pat1)} calls')
        time_taken = timer()
        for pat in pat1:
            find_all(pat.strip(), text)
        time_taken = timer() - time_taken
        print('Time taken:', time_taken)
    
    elif op == '4':
        from timeit import default_timer as timer
        test_text = text * 2
        for len_pat in [4, 8, 12]:
            times = []
            pat1 = [(pat*2)[:len_pat] for pat in pat1]
            print(f'|pat| = {len(pat1[0])}')
            for i in range(100_000, 1_000_000, 100_000):
                print('Testing n =', i)
                t = test_text[:i]
                start = timer()
                for pat in pat1:
                    find_all(pat, t)
                times.append((i, (timer() - start)/len(pat1)))
            print('Results stored in list \'times\'')
            for n, t in times:
                print(n, t)
        
    else:
        print('invalid op')

