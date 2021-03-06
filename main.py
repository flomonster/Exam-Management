from tkinter import *
from subject import *
from exam import *

class ExamUI(Frame):

    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.time_slots = []
        self.duration = None
        self.name = None
        self.add = None
        self.remove = None
        self.schedule = None
        self.message = None
        self.launch()

    def launch(self):
        Label(self, text="Exam name : ").grid(row=0, column=0)
        self.name = Entry(self)
        self.name.grid(row=0, column=1)
        Label(self, text="Duration of slots (min) : ").grid(row=0, column=2)
        self.duration = Entry(self)
        self.duration.grid(row=0, column=3)
        Label(self, text='Date (Ex: 1 May)').grid(row=1, column=1)
        Label(self, text='Time (Ex: 1230)').grid(row=1, column=3)
        self.time_slots = [(Entry(self), Entry(self))]
        for i in range(len(self.time_slots[0])):
            self.time_slots[0][i].grid(row=2, column=i * 2 + 1)
        self.add = Button(self, text='ADD', command=self.addSlot)
        self.add.grid(row=3, column=0)
        self.remove = Button(self, text='REMOVE', command=self.removeSlot)
        self.remove.grid(row=3, column=1)
        self.schedule = Button(self, text='SCHEDULE', command=self.scheduleExam)
        self.schedule.grid(row=3, column=2, columnspan=2)

    def scheduleExam(self):
        if self.message:
            self.message.destroy()
        self.name.configure(bg='white')
        self.duration.configure(bg='white')
        for i in range(len(self.time_slots)):
            for j in range(2):
                self.time_slots[i][j].configure(bg='white')

        if not self.name.get():
            self.message = Label(self, text='You have to choose a name !', bg='red')
            self.message.grid(row=len(self.time_slots) + 3, column=0, columnspan=4)
            self.name.configure(bg='red')
            return None
        sub = Subject.load('subject_list.xlsx')
        ts, dure = [], 0

        try:
            dure = int(self.duration.get())
        except:
            self.message = Label(self, text='You have to choose a duration !', bg='red')
            self.message.grid(row=len(self.time_slots) + 3, column=0, columnspan=4)
            self.duration.configure(bg='red')
            return None

        for i in range(len(self.time_slots)):
            try:
                if not self.time_slots[i][0]:
                    raise Exception('No day')
                start = int(self.time_slots[i][1].get())
                for j in range(len(ts)):
                    if (self.time_slots[i][0].get() == ts[j][0] and start == ts[j][1]):
                        raise Exception('Twice date')
                hh = (start // 100) + (start % 100 + dure) // 60
                mm = (start % 100 + dure) % 60
                end = hh * 100 + mm
                ts.append((self.time_slots[i][0].get(), start, end))
            except:
                for j in range(2):
                    self.time_slots[i][j].configure(bg='red')
                self.message = Label(self, text='This slot is not valid !', bg='red')
                self.message.grid(row=len(self.time_slots) + 3, column=0, columnspan=4)
                return None
        exam = Exam(self.name.get(), sub, ts)
        try:
            exam.schedule()
        except:
            self.message = Label(self, text='There is not enougth slots !', bg='red')
            self.message.grid(row=len(self.time_slots) + 3, column=0, columnspan=4)
            return None
        exam.printClassroomPdf()
        exam.printPdf()
        self.message = Label(self, text='Done !', bg='green')
        self.message.grid(row=len(self.time_slots) + 3, column=0, columnspan=4)

    def addSlot(self):
        self.time_slots.append((Entry(self), Entry(self)))
        for i in range(len(self.time_slots[-1])):
            self.time_slots[-1][i].grid(row=len(self.time_slots) + 1, column=i*2+1)
        self.update()

    def removeSlot(self):
        if len(self.time_slots) > 1:
            for i in range(len(self.time_slots[-1])):
                self.time_slots[-1][i].destroy()
            del self.time_slots[-1]
            self.update()

    def update(self):
        if self.message:
            self.message.destroy()
        self.add.grid(row=len(self.time_slots) + 2, column=0)
        self.remove.grid(row=len(self.time_slots) + 2, column=1)
        self.schedule.grid(row=len(self.time_slots) + 2, column=2, columnspan=2)

if __name__ == '__main__':
    root = Tk()
    root.title('Exam Manager')
    app = ExamUI(root)
    app.mainloop()
