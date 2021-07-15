import csv
import openpyxl
import sys
import time


class ExcelReader:
    def __init__(self):
        self.readExcel()
        self.getData()

    def readExcel(self):
        self.wb = openpyxl.load_workbook(self.filename)
        self.ws = self.wb.active

    def getData(self):
        cnt = 0
        for data in self.ws.rows:
            if cnt > 0 and data[self.outputNumber].value:
                self.outputData.append([
                    data[self.indexNumber].value, data[self.outputNumber].value])
            cnt += 1
        else:
            self.wb.close()


class OutputData(ExcelReader):
    def __init__(self, filename, indexNumber, outputNumber):
        self.filename = filename
        self.indexNumber = indexNumber
        self.outputNumber = outputNumber
        self.outputData = []
        self.outputName = f'output/output_{int(time.time())}'
        ExcelReader.__init__(self)

    def returnData(self):
        return self.outputData

    def returnPath(self):
        return self.outputName


class OutputTsv:
    def __init__(self, data, filename):
        self.data = data
        self.filename = filename
        self.dataOutput()
        self.resetData()
        print(f'{filename}`s create complate | total length is {len(data)}')

    def dataOutput(self):
        self.outFile = open(
            f'./{self.filename}.tsv', 'w', newline='', encoding='utf-8')
        writer = csv.writer(self.outFile, delimiter='\t')
        writer.writerows([value for value in self.data])
        self.outFile.close()

    def resetData(self):
        self.data = []
        self.filename = ""
