from classroom import *

class Slot:
    def _init_(self, students = [], classrooms = [], teachers = [], tas = [], subjects = [], time_slot = ('', 0, 0)):
        self.students = student
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
            while column < cr.n_column and not empty(student_subject):
                while not student_subject[sub]:
                    sub = (sub + 1) % len(sub)
                for i in range(min(len(student_subject[sub]), cr.n_row)):
                    cr.map_student[column][i] = student_subject[sub].pop()
                if not self.subjects[sub] in sub_in_cr:
                    sub_in_cr.append(self.subjects[sub])
                column += 1
                sub = (sub + 1) % len(sub)
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


    def print(self, examName):
        for c in self.classrooms:
            if not empty(c):
                c.printPdf(examName, self.time_slot)
