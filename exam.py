from slot import *
from math import ceil
from reportlab.lib import colors
from reportlab.platypus import PageBreak
from reportlab.lib.pagesizes import A4, inch, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

class Exam:
    def _init_(self, name = '', subjects=[], time_slots=[]):
        self.name = name
        self.students = []
        self.classrooms = []
        self.teachers = []
        self.tas = []
        self.subjects = subjects
        self.time_slots = time_slots
        self.slots = []

    def conflict(self, subject, slot):
        if not slot:
            return False

        for student in self.students:
            if subject in student.subjects:
                for sub in slot:
                    if sub in student.subjects:
                        return True
        return False

    def schedule(self):
        if not self.time_slots:
            raise Exception("No timeslots")

        ratio = ceil(len(self.subjects) / len(self.time_slots))
        allocation = [[] for j in range(len(self.time_slots))] 

        for s in self.subjects:
            i = 0
            while i < len(allocation) and \
            (len(allocation[i]) >= ratio or self.conflict(s, allocation[i])):
                i += 1
            if i == len(allocation):
                i = 0
                allocation = sorted(allocation, key=lambda l: len(l))
                while i < len(allocation) and self.conflict(s, allocation[i]):
                    i += 1
                if i == len(allocation):
                    raise Exception("Impossible to schedule")
            allocation[i].append(s)

        self.slots = []
        day = []
        self.time_slots = sorted(self.time_slots, key = itemgetter(0,1))
        for i, slot in enumerate(allocation):
            if day and day[0].time_slot[0] != slot[0]:
                self.slots.append(day)
                day = []
            day.append(Slot(self.students, self.classrooms, self.teachers, self.tas, \
                    slot, self.time_slots[i]))
        self.slots.append(day)

    def printPdf(self):
        filename = self.name + '_timetable.pdf'
        doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        doc.pagesize = landscape(A4)
        story = []
        
        for i, day in enumerate(self.slots):
            data = [[''] * 5 for i in range(3)]
            data[0][0] = self.name
            data[1] = ['Date', 'Time', 'Course Code', 'Course Name', 'No. of\nStudents']
            data[2][0] = 'Day ' + str(i + 1)
            style = [('SPAN', (0, 0), (-1, 0)),
                     ('SPAN', (0, 2), (-1, 2)),
                     ('ALIGN', (0,0), (-1, 1), 'CENTER'),
                     ('VALIGN', (0,0), (-1, 1), 'MIDDLE'),
                     ('ALIGN', (0,3), (-1, -1), 'CENTER'),
                     ('VALIGN', (0,3), (-1, -1), 'MIDDLE'),
                     ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                     ('BOX', (0,0), (-1,-1), 0.25, colors.black)]

            for i, slot in enumerate(day):
                for sub in slot.subjects:
                    day = slot.time_slot[0]
                    time = str((slot.time_slot[1] // 100) % 12) + ':' + str(slot.time_slot[1] % 100)
                    time += 'PM' if (slot.time[1] // 100) % 12 else 'AM'
                    data.append([day, time, sub.code, sub.name, sub.nbStudent(self.students)])
                start, end = len(data) - len(slot.subjects), len(data) - 1
                style.append(('SPAN', (0, start), (0, end)))
                style.append(('SPAN', (1, start), (1, end)))
                if i + 1 != len(day):
                    style.append(('SPAN', (0, end + 1), (-1, end + 1)))
                    data.append([''] * 5)
            table = Table(data)
            table.setStyle(TableStyle(style))
            story.append(table)
            story.append(PageBreak())
