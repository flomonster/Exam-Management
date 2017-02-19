import xlrd
from reportlab.lib import colors
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

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
   
    def printPdf(self, exam_name, time_slot):
        filename = exam_name + '_' + time_slot[0] + '-' + str(time_slot[1]) + '_' + self.name + '.pdf'
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = landscape(A4)

        # Classroom table
        data = [[''] * self.n_column for i in range(self.n_row + 3)]
        data[0][0] = exam_name
        data[1][0] = 'Classroom: ' + self.name + ' ' + time_slot[0] + ' ' + \
                str(time_slot[1] // 100) + ':' + str(time_slot[1] % 100) + ' to ' +\
                str(time_slot[2] // 100) + ':' + str(time_slot[2] % 100)
        for i in range (self.n_column):
            data[2][i] = 'C' + str(i + 1)

        for i in range(self.n_row):
            for j in range(self.n_column):
                data[i+3][j] = self.map_student[i][j].roll_no

        style = TableStyle([('SPAN', (0, 0), (-1, 0)),
                            ('SPAN', (0, 1), (-1, 1)),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                            ])
        table = Table(data)
        table.setStyle(style)

        # Teacher table
        data2 = [[''] for i in range(3 + len(self.tas))]
        data2[0][0] = exam_name
        data2[1][0] = 'Classroom: ' + self.name + ' ' + time_slot[0] + ' ' + \
                str(time_slot[1] // 100) + ':' + str(time_slot[1] % 100) + ' to ' +\
                str(time_slot[2] // 100) + ':' + str(time_slot[2] % 100)
        data2[2][0] = self.teacher.lastname + ' ' + self.teacher.firstname
        for i, t in enumerate(self.tas):
            data2[3 + i][0] = t.lastname + ' ' + t.firstname + '\n' + t.roll_no
        table2 = Table(data2)
        table2.setStyle(style)

        doc.multiBuild([table, PageBreak(), table2])
