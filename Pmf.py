from collections import Counter
import operator

class _Wrapper:
    def __init__(self, d=None):
        if d is None:
            self.d = Counter()
        else:
            # if isinstance(d, (list, tuple)):
            #     temp = {}
            #     for x in d:
            #         temp[x] = temp.get(x, 0) + 1
            #     self.d = temp
            # elif isinstance(d, dict):
            #     self.d = d
            self.d = Counter(d)


class Hist(_Wrapper):
    def __init__(self, d=None):
        super().__init__(d)

    def freq(self, x):
        return self.d.get(x, 0)

    def most_freqs(self, n=3):
        return self.d.most_common(n)

    def freqs(self):
        return self.d.values()

    def sorted_freqs(self):
        return sorted(self.d.items(), key=operator.itemgetter(1))


class Pmf(_Wrapper):
    def __init__(self, d=None):
        super().__init__(d)
        p = {}
        for x, value in self.d.items():
            p[x] = float(value)/sum(self.d.values())
        self.p = p

    def prob(self, x):
        return self.p.get(x, 0)

    def probs(self):
        return self.p.values()

    def mean(self):
        mu = 0.0
        for x, prob in self.p.items():
            mu += x*prob
        return mu

    def var(self, mu=None):
        if mu is None:
            mu = self.mean()
        var1 = 0.0
        for x, prob in self.p.items():
            var1 += prob*(x-mu)**2
        return var1



if __name__ == '__main__':
    h1=Hist([1,2,3,3,3,4,4, 5,5, 5, 1, 5])
    # i = 0
    # max=0
    # for x, fre in h1.d.items():
    #     if fre > max:
    #         max =fre
    #         i= x
    # print('{} 出先多次: {}'.format(x, max))
    print(h1.sorted_freqs())
    p = Pmf([1,2,2,3])
    print(p.prob(2))




