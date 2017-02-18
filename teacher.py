import xlrd
class Teacher:

    def __init__(self, firstname = '', lastname = '', subects = []):
        self.firstname = firstname
        self.lastname = lastname
        self.subects = subects

    def load(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        tea_list = []

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            tea_list.append(Teacher(row[0], row[1], row[2]))
           
        return tea_list
