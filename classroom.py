class Classroom:

    def __init__(self, name = '', row = 0, n_column = 0):
        self.name = name
        self.teacher = None
        self.tas = []
        self.map_student = [[None for j in range(n_column)] for i in range(n_row)]
        self.n_row = n_row
        self.n_column = n_column

    def load(path):
        pass
    
    def print(self, exam_name, time_slot):
        pass
