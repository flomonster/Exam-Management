from classroom import *
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class Slot:
    def __init__(self, students = [], classrooms = [], teachers = [], tas = [], subjects = [], time_slot = ('', 0, 0)):
        self.students = students
        self.classrooms = classrooms
        self.teachers = teachers
        self.tas = tas
        self.subjects = subjects
        self.time_slot = time_slot
        self.manage()

    def empty(ll):
        if not ll:
            return True
        for l in ll:
            if l:
                return False
        return True

    def manage(self):
        student_subject = [[] for i in range(len(self.subjects))] 
        teachers = self.teachers[:]
        teachers = self.tas[:]
        tas = self.tas[:]
        for i, sub in enumerate(self.subjects):
            for s in self.students:
                if sub in s.subjects:
                    student_subject[i].append(s)

        for cr in self.classrooms:
            sub_in_cr = []
            column = 0
            sub = 0
            while column < cr.n_column and not Slot.empty(student_subject):
                while not student_subject[sub]:
                    sub = (sub + 1) % len(self.subjects)
                for i in range(min(len(student_subject[sub]), cr.n_row)):
                    cr.map_student[i][column] = student_subject[sub].pop()
                if not self.subjects[sub] in sub_in_cr:
                    sub_in_cr.append(self.subjects[sub])
                column += 1
                sub = (sub + 1) % len(self.subjects)
            if sub_in_cr:
                for i, t in enumerate(teachers):
                    for s in t.subjects:
                        if s in sub_in_cr:
                            cr.teacher = t
                            del teachers[i]
                            break
                    if cr.teacher:
                        break
                for i, t in enumerate(tas):
                    for s in t.subjects:
                        if s in sub_in_cr:
                            cr.tas.append(t)
                            break
                    if len(cr.tas) > 1:
                        break
                for t in cr.tas:
                    tas.remove(t)


    def printPdf(self, examName):
        for c in self.classrooms:
            if not c.empty():
                c.printPdf(examName, self.time_slot)

        # Teacher table
        filename = examName + '_' + self.time_slot[0] + '-' + str(self.time_slot[1]) + '_teacher' + '.pdf'
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = portrait(A4)

        data = [[examName, ''], ['','']]
        data[1][0] = self.time_slot[0] + ' ' + str(self.time_slot[1] // 100) + ':' +\
                str(self.time_slot[1] % 100) + ' to ' + str(self.time_slot[2] // 100) +\
                ':' + str(self.time_slot[2] % 100)
        
        style = [('SPAN', (0, 0), (-1, 0)),
                 ('SPAN', (0, 1), (-1, 1)),
                 ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                 ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                 ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                 ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                ]

        for c in self.classrooms:
            if not c.empty() and c.teacher:
                data.append(["Classroom : " + c.name, ""])
                style.append(('SPAN', (0, len(data)-1), (-1, len(data)-1)))
                data.append(["TEACHER", c.teacher.lastname + ' ' + c.teacher.firstname])
                for t in c.tas:
                    data.append(['TA', t.lastname + ' ' + t.firstname + '\n(' + t.roll_no + ')'])
                if len(c.tas) > 1:
                    style.append(('SPAN', (0, len(data) - len(c.tas)), (0, len(data) - 1)))
        table = Table(data)
        table.setStyle(TableStyle(style))
        doc.multiBuild([table])
