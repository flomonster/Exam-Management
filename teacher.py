import xlrd
class Teacher:

    def __init__(self, firstname = '', lastname = '', subjects = []):
        self.firstname = firstname
        self.lastname = lastname
        self.subjects = subjects

    def load(path, list_subject):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        tea_list = []

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            code_list = row[2].split()
            list_sub = []
            for s in list_subject:
                if s.code in code_list:
                    list_sub.append(s)
            tea_list.append(Teacher(row[0], row[1], list_sub))
           
        return tea_list
