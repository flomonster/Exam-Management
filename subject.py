import xlrd

class Subject:

    def __init__(self, name = '', code = ''):
        self.name = name
        self.code = code

    def load(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        sub_list=[]

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            sub_list.append(Subject(row[1], row[0]))
           
        return sub_list
