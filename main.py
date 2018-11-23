import pysftp
from tkinter import *
import datetime
import os
import win32com.client

class make_ui(Tk):
    date_list = list()
    non_formatted_date_list = list()
    cur_date = datetime.datetime.now()
    for i in range(0, 7):
        date_list.append((cur_date + datetime.timedelta(days=i)).strftime('%B %d, %Y'))
        k = cur_date + datetime.timedelta(days=i)
        rep = k.replace(hour = 6, minute = 0, second = 0, microsecond = 0)
        non_formatted_date_list.append(rep)

        
    def __init__(self):
        Tk.__init__(self)
        self.wm_title("Class Adder")
        self.geometry("300x525")
        frame = Frame(self)
        frame.pack()
        lb_pane = PanedWindow(frame, orient=HORIZONTAL)
        ins_pane = PanedWindow(frame, orient=HORIZONTAL)
        buttons = PanedWindow(frame, orient=HORIZONTAL)
        lb_pane.pack()
        ins_pane.pack()
        buttons.pack()
        lb = Listbox(lb_pane, width=30)
        lbl1 = StringVar()
        lbl2 = StringVar()
        lbl3 = StringVar()
        lbl4 = StringVar()
        lbl_1 = Label(ins_pane, textvariable=lbl1)
        lbl_2 = Label(ins_pane, textvariable=lbl2)
        lbl_3 = Label(ins_pane, textvariable=lbl3)
        lbl_4 = Label(ins_pane, textvariable=lbl4)
        lbl1.set("Insert User ID here (900#)")
        lbl2.set("Insert Password here")
        lbl3.set("Insert Apin here")
        lbl4.set("Insert CRN's here (new line after each, 8 max)")
        self.text = Text(ins_pane, height=1, width=34)
        self.text2 = Text(ins_pane, height=1, width=34)
        self.text3 = Text(ins_pane, height=1, width=34)
        self.text4 = Text(ins_pane, height=10, width=34)
        self.text4.insert("1.0","CRN1\nCRN2\nCRN3\nCRN4")
        lbl_1.pack()
        self.text.pack()
        lbl_2.pack()
        self.text2.pack()
        lbl_3.pack()
        self.text3.pack()
        lbl_4.pack()
        self.text4.pack()
        add_button = Button(buttons, text="Confirm", command=self.setup_scheduler)
        add_button.pack()
        for i in range(len(self.date_list)):
            lb.insert(i, self.date_list[i])
        lb.bind("<<ListboxSelect>>", self.OnDouble)
        lb.pack()
        lb_pane.add(lb)
        if os.getcwd() not in sys.path:
            sys.path.append(os.getcwd())

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        try:
            value = widget.get(selection[0])
        except IndexError:
            return
        self.value = value

    def setup_scheduler(self):
        self.scheduler = win32com.client.Dispatch('Schedule.Service')
        self.scheduler.Connect()
        folder = self.scheduler.GetFolder('\\')
        task_def = self.scheduler.NewTask(0)

        #Create trigger
        start_time = datetime.datetime.now() + datetime.timedelta(seconds = 5)
        TASK_TRIGGER_TIME = 1
        trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
        trigger.StartBoundary = start_time.isoformat()

        #Create action
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.ID = 'DO NOTHING'
        wd = os.getcwd()
        action.Path = wd + r'\register.exe'
        action.WorkingDirectory = wd + r''
        action.Arguments = ''

        #register task
        # If task already exists, it will be updated
        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_NONE = 0
        folder.RegisterTaskDefinition(
        'Registration task',    
        task_def,
        TASK_CREATE_OR_UPDATE,
        '',
        '',
        TASK_LOGON_NONE)
        self.create_files()

    def create_files(self):
        user_id = self.text.get("1.0","end-1c")
        user_pass = self.text2.get("1.0","end-1c")
        apin = self.text3.get("1.0","end-1c")
        crn_list = self.text4.get("1.0","end-1c")
        f = open("user_info.txt", "w")
        f.write(user_id + '\n' + user_pass + '\n' + apin)
        f.close()
        f = open("crn_list.txt", "w")
        l = str(crn_list).split('\n')
        for m in l:
            if str(m).startswith("CRN"):
                continue
            else:
                f.write(m + '\n')
        f.close()


if __name__ == "__main__":
    events_adder = make_ui()
    events_adder.mainloop()