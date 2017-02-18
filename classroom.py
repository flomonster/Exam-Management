import xlrd
class Classroom:

    def __init__(self, name = '', n_row = 0, n_column = 0):
        self.name = name
        self.teacher = None
        self.tas = []
        self.map_student = [[None for j in range(n_column)] for i in range(n_row)]
        self.n_row = n_row
        self.n_column = n_column

    def load(path):
        book = xlrd.open_workbook(path)
        sheet = book.sheet_by_index(0)
        cr_list = []

        for i in range(1, sheet.nrows):
            row = sheet.row_values(i)
            cr_list.append(Classroom(row[0], int(row[1]), int(row[2])))
           
        return cr_list
   
    def print(self, exam_name, time_slot):
        pass
        
if __name__=='__main__':
    print(Classroom.load("classroom.xlsx"))
