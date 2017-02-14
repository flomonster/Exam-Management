class Classroom:

    def __init__(self, name = '', teacher = None, tas = [], no_row = 0, no_column = 0):
        self.name = name
        self.teacher = teacher
        self.tas = tas
        self.map_student = [[None for j in range(no_row)] for i in range(no_column)]

    def load(path):
        pass
    
    def print(self, subjects_name, exam_name, time_slot):
        pass
