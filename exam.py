from slot import *
from math import ceil

class Exam:
    def _init_(self, subjects=[], time_slots=[]):
        self.students = []
        self.classrooms = []
        self.teachers = []
        self.tas = []
        self.subjects = subjects
        self.time_slots = time_slots

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

        slots = []
        for i, slot in enumerate(allocation):
            slots.append(Slot(self.students, self.classrooms, self.teachers, self.tas, \
                    slot, self.time_slots[i]))

    def print(self):
        pass
