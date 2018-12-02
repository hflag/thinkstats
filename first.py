import survey
import thinkstats


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
    table.mu = thinkstats.mean(table.lengths)

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
    print('Mean gestation in weeks:')
    print('First babies', mu1)
    print('Others', mu2)
    print('Difference in days', (mu1 - mu2) * 7.0)
    print('Difference in hours', (mu1-mu2) * 7 * 24.0)

if __name__ == '__main__':

    summary(data_dir='../data')