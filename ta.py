import xlrd
 
class TA:
    def __init__ (self, firstname = '', lastname = '', roll_no = '', subjects =[]):
        self.firstname = firstname 
        self.lastname = lastname 
        self.roll_no = roll_no 
        self.subjects = subjects 
    
    def load (path, list_subject):
        book = xlrd.open_workbook (path)
        sheet = book.sheet_by_index (0) 
        ta_list =[]
        for i in range (1, sheet.nrows):
            row = sheet.row_values (i)
            code_list = row[3].split()
            sub_list = []
            for s in list_subject:
                if s.code in code_list:
                    sub_list.append(s)
            ta_list.append(TA(row[0], row[1], row[2], sub_list))
        return ta_list 
