import numpy as np

def mean(t):
    """
    计算一个序列的均值
    :param t: 数字序列
    :return: mean
    """
    return float(sum(t))/len(t)


def var(t, mu=None):
    if mu is None:
        mu = mean(t)

    dev2 = [(x-mu)**2 for x in t]
    return mean(dev2)

if __name__ == '__main__':
    ng = [1.0, 1.0, 1.0, 3.0, 3.0, 591.0]
    print("Mean of nangua:", mean(ng))
    print("var of nangua", var(ng))
    print("===========================")
    print("mean of nangua by np:", np.mean(ng))
    print("var of nangua by np:", np.var(ng))