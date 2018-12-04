import survey
import thinkstats
import Pmf

def partitionRecords(table):
    """
    将记录划分成两个列表：头一个孩子，其他情况。只统计存活的婴儿
    :param table:  怀孕者表
    :return:
    """
    firsts = survey.Pregnancies()
    others = survey.Pregnancies()

    for p in table.records:
        # 忽略死亡的婴儿
        if p.outcome != 1:
            continue
        if p.birthord == 1:
            firsts.addRecord(p)
        else:
            others.addRecord(p)
    return firsts, others

def process(table):
    """
    分析给定的表，求解不同出生顺序的婴儿怀孕周几的均值
    :param table:
    :return:
    """
    table.lengths = [p.prglength for p in table.records]
    table.n = len(table.lengths)

    # 计算均值和方差
    table.mu = thinkstats.mean(table.lengths)
    table.var = thinkstats.var(table.lengths)

def processTables(*tables):
    for table in tables:
        process(table)


def makeTables(data_dir):
    table = survey.Pregnancies()
    table.readRecords(data_dir)
    firsts, others = partitionRecords(table)

    return table, firsts, others

def summary(data_dir):
    table, firsts, others = makeTables(data_dir='data')

    processTables(firsts, others)
    print('Number of first babies:', firsts.n)
    print('Number of others:', others.n)
    mu1, mu2 = firsts.mu, others.mu

    # 计算方差
    var1, var2 = firsts.var, others.var
    # print('Mean gestation in weeks:')
    print("The first babies' mean is {} and var is {}".format(mu1, var1))
    print("The other babies' mean is {} and var is {}".format(mu2, var2))
    print('Difference in days', (mu1 - mu2) * 7.0)
    print('Difference in hours', (mu1-mu2) * 7 * 24.0)

    firsts_prglength = [r.prglength for r in firsts.records]
    others_prglength = [r.prglength for r in others.records]

    firsts_hist = {}
    others_hist = {}
    for x in firsts_prglength:
        firsts_hist[x] = firsts_hist.get(x, 0) + 1
    for y in others_prglength:
        others_hist[y] = others_hist.get(y, 0) + 1
    print(firsts_hist)

if __name__ == '__main__':

    summary(data_dir='data')
    print('done')