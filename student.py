import xlrd

class Student:
    def __init__(self, firstname = '', lastname = '', roll_no = '', subjects = []):
        self.firstname = firstname
        self.lastname = lastname
        self.roll_no = roll_no
        self.subjects = subjects

    def load(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        stu_list=[]

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            stu_list.append(Student(row[0],row[1],row[2],row[3]))
           
        return stu_list
