import sys
import gzip
import os


class Record():
    """
    代表一条记录
    """


class Respondent(Record):
    """代表一个调查者"""


class Pregnancy(Record):
    """
    代表一个怀孕者
    """


class Table():
    """
    代表一张表，是一个对象的列表
    """
    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def readFile(self, data_dir, filename, fields, constructor, n=None):
        """
        从一个压缩文件中读出数据，每一条记录构建一个对象

        :param data_dir: 字符串目录名
        :param filename: 待读入的文件名
        :param fields: （name, start, end, cast)元组序列指定要提取的域
        :param constructor:创建对象的类型
        :param n:
        :return:
        """
        filename = os.path.join(data_dir, filename)

        if filename.endswith('gz'):
            fp = gzip.open(filename)
        else:
            fp = open(filename)

        for i, line in enumerate(fp):
            if i == n:
                break
            record = self.makeRecord(line, fields, constructor)
            self.addRecord(record)
        fp.close()

    def makeRecord(self, line, fields, constructor):
        """
        扫描文件中的一行内容，使用合适的域来构建一个对象
        :param line: 文件中一行数据
        :param fields: 指定提取域的一个（name, start, end, cast)元组序列
        :param constructor:构建一个对象记录的函数
        :return: 带有合适域的记录
        """
        obj = constructor()
        for (field, start, end, cast) in fields:
            try:
                s = line[start-1: end]
                val = cast(s)
            except ValueError:
                val = 'NA'
            setattr(obj, field, val)
        return obj

    def addRecord(self, record):
        """
        向表中添加一条记录
        :param record: 待添加的记录
        :return:
        """
        self.records.append(record)

    def extendRecords(self, records):
        """
        添加多条记录到表中
        :param records: 记录对象的序列
        :return:
        """
        self.records.extend(records)

    def recode(self):
        pass


class Respondents(Table):
    """
    代表调查者的表
    """
    def readRecords(self, data_dir='.', n=None):
        filename = self.getFileName()
        self.readFile(data_dir, filename, self.getFields(), Respondent, n)
        self.recode()

    def getFileName(self):
        return '2002FemResp.dat.gz'

    def getFields(self):
        """
        返回一个元组指定要提取的域。

        元组的元素是field， start， end，cast。
            field 是变量的名字
            start和end 是NSFG文档中指定的切片
            cast是一个可调用对象，也难怪了转换结果为int, float等。
        """
        return [('caseid', 1, 12, int)]


class Pregnancies(Table):
    """
    包含有关怀孕的调查数据
    """
    def readRecords(self, data_dir='.', n=None):
        filename=self.getFileName()
        self.readFile(data_dir, filename, self.getFields(), Pregnancy, n)
        self.recode()

    def getFileName(self):
        return '2002FemPreg.dat.gz'


    def getFields(self):
        """
        从调查数据中提取的域的信息
        :return: 元组（name, start, end, type)的序列
        """
        return [
            ('caseid', 1, 12, int),
            ('nbrnaliv', 22, 22, int),
            ('babysex', 56, 56, int),
            ('birthwgt_lb', 57, 58, int),
            ('birthwgt_oz', 59, 60, int),
            ('prglength', 275, 276, int),
            ('outcome', 277, 277, int),
            ('birthord', 278, 279, int),
            ('agepreg', 284, 287, int),
            ('finalwgt', 423, 440, float),
        ]

    def recode(self):
        for rec in self.records:

            # 母亲的年龄除以100
            try:
                if rec.agepreg != 'NA':
                    rec.agepreg /= 100.0
            except AttributeError:
                pass

            # 将出生时的体重从lbs / oz转换为总盎司
            # 注意：有些出生体重很小，几乎可以肯定是错误数据
            # 但是目前不打算过滤它们
            try:
                if(rec.birthwgt_lb != 'NA' and rec.birthwgt_lb < 20 and
                   rec.birthwgt_oz != 'NA' and rec.birthwgt_oz <= 16):
                    rec.totalwgt_oz = rec.birthwgt_lb * 16 + rec.birthwgt_oz
                else:
                    rec.totalwgt_oz = 'NA'
            except AttributeError:
                pass


if __name__ == '__main__':
    resp = Respondents()
    resp.readRecords(data_dir='data')
    print('Number of rewpondents', len(resp.records))


    preg = Pregnancies()
    preg.readRecords(data_dir='data')
    print('Number of pregnancies', len(preg.records))

