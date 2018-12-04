import Pmf
import survey


def probRange(pmf, low, high):
    total = 0.0
    for week in range(low, high+1):
        total += pmf.prob(week)
    return total

def probEarly(pmf):
    return probRange(pmf, 0, 37)

def probOnTime(pmf):
    return probRange(pmf, 38, 40)

def probLate(pmf):
    return probRange(pmf, 41, 50)



if __name__ == '__main__':
    # 读取数据
    table = survey.Pregnancies()
    table.readRecords(data_dir='data')

    # 过滤死去的婴儿，分组为第一胎和其他
    firsts = survey.Pregnancies()
    others = survey.Pregnancies()

    for r in table.records:
        if r.outcome != 1:
            continue
        if r.birthord == 1:
            firsts.addRecord(r)
        else:
            others.addRecord(r)
    firsts_prglengths = [r.prglength for r in firsts.records]
    others_prglengths = [r.prglength for r in others.records]
    firsts_pmf = Pmf.Pmf(firsts_prglengths)
    others_pmf = Pmf.Pmf(others_prglengths)

    # print("The first babies' early prob , ontime prob and later prob are {}, {}, {}".format(probEarly(firsts_pmf), probOnTime(firsts_pmf), probLate(firsts_pmf)))
    # print("The others babies' early prob , ontime prob and later prob are {}, {}, {}".format(probEarly(others_pmf),
    #                                                                                         probOnTime(others_pmf),
    print('Risks:')
    funcs = [probEarly, probOnTime, probLate]
    firsts_probs = {}
    for func in funcs:
        prob = func(firsts_pmf)
        firsts_probs[func.__name__] = prob
    others_probs = {}
    for func in funcs:
        prob = func(others_pmf)
        others_probs[func.__name__] = prob
    print('Risk ratios (first babies /others):')
    for k in firsts_probs.keys():
        print(k, ':', firsts_probs[k]/others_probs[k])



