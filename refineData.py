import re
import sys
from outputData import OutputTsv


class DataRefiner:
    def __init__(self, data):
        self.data = data
        self.regexs = []
        self.replaceData = []
        self.readRegex()

    def readRegex(self):

        f = open(f'./refine.regex.txt', 'r', encoding='utf-8')

        for line in f:
            tokens = line.split('\t')

            if len(tokens) == 1:
                tokens += [' ']

            tokens[0] = tokens[0][:-
                                  1] if tokens[0].endswith('\n') else tokens[0]
            tokens[1] = tokens[1][:-
                                  1] if tokens[1].endswith('\n') else tokens[1]

            self.regexs += [(tokens[0], tokens[1])]

        f.close()

    def dataPreprocess(self):
        for value in self.data:
            for r in self.regexs:
                replaceData = re.sub(
                    r'%s' % r[0], r[1], value[1].strip())
            self.replaceData.append([value[0], replaceData])

        return self.replaceData
