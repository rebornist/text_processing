import MeCab
import os
import re
import sys
from outputData import OutputData, OutputTsv
from refineData import DataRefiner


class DataTokenizer:
    def __init__(self, data):
        self.data = data
        self.tokenized = []
        self.mecab = MeCab.Tagger()
        # 우리가 원하는 TOKEN\tPOS의 형태를 추출하는 정규표현식.
        self.pattern = re.compile(".*\t[A-Z]+")

    def dataTokenize(self):
        for i in self.data:
            morph = self.mecabMorphs(i[1])
            cleaningText = self.textCleaning(morph)
            self.tokenized.append([i[0], morph, cleaningText])
        return self.tokenized

    def mecabMorphs(self, text):
        morphs = []

        # 우리가 원하는 TOKEN\tPOS의 형태를 추출하는 정규표현식.
        pattern = re.compile(".*\t[A-Z]+")

        # 패턴에 맞는 문자열을 추출하여 konlpy의 mecab 결과와 같아지도록 수정.
        temp = [tuple(pattern.match(token).group(0).split("\t"))
                for token in MeCab.Tagger().parse(text).splitlines()[:-1]]

        # 추출한 token중에 문자열만 선택.
        for token in temp:
            morphs.append(token[0])

        self.tokenizedText = ' '.join(morphs)
        return self.tokenizedText

    def textCleaning(self, text):
        # 문자와 숫자를 제외한 글자를 제거하는 함수.
        # doc = re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
        items = []
        doc = re.sub("[^0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣 ]", "", text)
        for value in doc.split(' '):
            if value != " " or value != "":
                items.append(value)

        return ' '.join(items)


if __name__ == '__main__':
    filepath = ""
    if sys.argv[1] == "none":
        filepath = r"C:\Users\saint\OneDrive\proj\2021\sen\04.대상자료\all_files_data_210708.xlsx"
    else:
        filepath = sys.argv[1]

    output = OutputData(filepath, int(sys.argv[2]) - 1, int(sys.argv[3]) - 1)
    dataOrg = output.returnData()
    filename = output.returnPath()
    OutputTsv(dataOrg, filename)

    dataRefine = DataRefiner(dataOrg).dataPreprocess()
    refinedFilename = f'{filename}.refined'
    OutputTsv(dataRefine, refinedFilename)

    dataTokenize = DataTokenizer(dataRefine).dataTokenize()
    tokenizedFilename = f'{refinedFilename}.tokenized'
    OutputTsv(dataTokenize, tokenizedFilename)
