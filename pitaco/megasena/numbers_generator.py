from random import sample, uniform
from pitaco.megasena.file_loader import MegasenaFileLoader
from os.path import dirname, join


class MegasenaNumberGenerator(object):

    numbers = None
    result_analyzer = None
    
    
    def __init__(self):
        folder = join(dirname(dirname(dirname(__file__))), "downloads")
        loader = MegasenaFileLoader(folder)
        self.result_analyzer = loader.load_from_csv()

    def calc_frequency(self):
        freq = self.result_analyzer.get_most_frequent()
        highest = float(freq[0][1])
        lowest = float(freq[-1][1])
        delta = float(highest - lowest)
        for (n, f) in freq:
            p = self.numbers[n-1][1]
            new_p = (((f - lowest) / delta) * 4)
            self.numbers[n-1] = (n, p + new_p)
#         print "freq: " 
#         print freq
#         print "numbers: "
#         print sorted(self.numbers, reverse=True, key=lambda x: x[1])
#         print "---"

    def calc_missing_numbers(self):
        missing = self.result_analyzer.get_longest_numbers_missing()
        highest = float(missing[0][1])
        lowest = float(missing[-1][1])
        delta = float(highest - lowest)
        for (n, f) in missing:
            p = self.numbers[n-1][1]
            new_p = (((f - lowest) / delta) * 4)
            self.numbers[n-1] = (n, p + new_p)
#         
#         print missing
#         print "numbers: "
#         print sorted(self.numbers, reverse=True, key=lambda x: x[1])
#         print missing

    def sample(self):
        total = sum([p for n, p in self.numbers])
        r = int(uniform(0, total) * 100) / 100.0
        p_count = 0
        for i, (n, p) in enumerate(self.numbers):
            p_count += p
            if p_count >= r:
                self.numbers.pop(i)
                break
        return n

    def calculate_odds_evens(self, numbers):
        (p_odd, p_even) = self.result_analyzer.calculate_prob_odd_even(numbers)
        
        print "total: %s, evens: %s, odds: %s" % (len(numbers), evens, odds)
        print "p_odd: %s, p_even: %s" % (p_odd, p_even)

    def generate(self):
        self.numbers = zip(range(1, 61), [1]*60)
        self.calc_frequency()
        self.calc_missing_numbers()
        
        numbers = []
        for _ in xrange(6):
            numbers.append(self.sample())
#             self.calculate_odds_evens(numbers)

        numbers = sorted(numbers)
        return numbers

    def _generate(self):
        r = [0] * 60  
        for _ in xrange(5000):
            numbers = self._generate()
            for n in numbers:
                r[n-1] += 1
        print "Sorteados: "
        print sorted([(i+1, n) for (i, n) in enumerate(r)], key=lambda x: x[1], reverse=True)
        return self._generate()
