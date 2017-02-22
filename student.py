import xlrd

class Student:
    def __init__(self, firstname = '', lastname = '', roll_no = '', subjects = []):
        self.firstname = firstname
        self.lastname = lastname
        self.roll_no = roll_no
        self.subjects = subjects

    def load(path, subject_list):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        stu_list=[]

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            code_list = row[3].split()
            list_sub = []
            for s in subject_list:
                if s.code in code_list:
                    list_sub.append(s)
            stu_list.append(Student(row[0], row[1], row[2], list_sub))
           
        return stu_list
