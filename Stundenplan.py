import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd
import numpy as np


class Period:
    def __init__(self, prof=None, subject=None, time=None, day=None):
        self.subject, self.prof, self.time = subject, prof, time
        self.times = list((np.arange(1, 7, 1)))
        self.days = ["Mo", "Di", "Mi", "Do", "Fr"]
        if day and day not in self.days:
            raise TypeError("Ungültiger Wochentag!")
        self.day = day


class Interface(Period):
    """
    Erzeugt Eingabefenster. Wenn schon einige Optionen vorgegeben werden, werden diese auch angezeigt
    """

    def __init__(self, prof=None, subject=None, time=None, day=None):
        super().__init__(prof, subject, time, day)  # Initialise Period for base info
        self.window = tk.Tk()  # create window
        self.prof_input, self.subject_input, self.time_input, self.day_input = self.setup_input()  # create input fields
        self.button(5, 0, "OK", self.get_info)
        self.button(6, 0, "Zusätzliche ähnliche Stunde", self.get_additional_info)
        self.button(7, 0, "Eingabe beenden", self.get_final_info)
        self.additional_period = False
        self.cont_input = True
        self.window.mainloop()

    def setup_input(self):
        prof_input = self.text_input(0, 0, "Name des Dozierenden", self.prof)
        subject_input = self.text_input(1, 0, "Name des Fachs", self.subject)
        time_input = self.opt_input(3, 0, self.times, "Doppelstunde")
        day_input = self.opt_input(4, 0, self.days, "Tag")
        return prof_input, subject_input, time_input, day_input

    def text_input(self, row, column, text, filled_text):
        """
        Creates a field for text entry
        :param int row: y-Position in Window
        :param int column: x-Position in Window
        :param str text: Description for User Input
        :param str filled_text: Text that is to be entered into entry field at creation
        :return: Entry name
        """
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=row, column=column, padx=1, pady=1)  # Frame positionieren
        label_prompt = tk.Label(master=frame,
                                text=text + ":",
                                width=20,
                                height=2)
        label_prompt.pack()  # Label im Frame Positionieren
        name = tk.Entry(master=frame)
        if filled_text:
            name.insert(0, filled_text)
        name.pack()
        return name

    def opt_input(self, row, column, options, text):
        """
        Creats dropdown list with options
        :param int row: y-Position in Window
        :param int column: x-Position in Window
        :param list options: Options in  Dropdown-List
        :param str text: Description for User Input
        :return: chosen option var
        """
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=row, column=column, padx=1, pady=1)
        lbl = tk.Label(text=text + ":",
                       master=frame)
        lbl.grid(row=0, column=0)
        var = tk.StringVar(self.window)  # Rückgabevariable erzeugen
        opts = ttk.OptionMenu(frame, var, options[0], *options)
        opts.grid(row=0, column=1)
        return var

    def button(self, row, column, text, command):
        """
        Creates a button assigned to the specified command
        :param int row: Position
        :param int column: Position
        :param str text: Text on the button
        :param function command: Command to be executed on buttonpress
        :return:
        """
        frame = ttk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=row, column=column, padx=1, pady=1)
        button = ttk.Button(text=text, master=frame, command=command)
        button.pack()

    def get_info(self):
        """
        Sets the values of the container "Period" to the values written in the respective Field at confirmation_button
        push.
        Closes window after
        """
        self.prof = self.prof_input.get()
        self.subject = self.subject_input.get()
        self.time = self.time_input.get()
        self.day = self.day_input.get()
        self.window.destroy()

    def get_additional_info(self):
        """
        In case an additional Period with somewhat similar information is wished to be created. Changes a flag which
        can be tested in the Interface() calling function to determine if new interface is to be created
        :return:
        """
        self.additional_period = True
        self.get_info()

    def get_final_info(self):
        self.cont_input = False
        self.get_info()


class Timetable:
    def __init__(self):
        self.prof_frame = pd.DataFrame(columns=Period().days, index=Period().times)
        self.subj_frame = pd.DataFrame(columns=Period().days, index=Period().times)
        self.build_timetable()

    def build_timetable(self):
        cont_input = True
        while cont_input:
            cont_input = self.get_period()       # get user inputs, also check if the input is stopped
        return self.prof_frame, self.subj_frame

    def get_period(self, prof=None, subject=None):
        """
        Gets Period names from Interface class, adds them to periods list
        :param prof:
        :param subject:
        :return: bool cont_input: whether new input should be read in
        """

        entered_period = Interface(prof, subject)
        cont_input = entered_period.cont_input
        # check if there is a subject to write. If not, check if they want to. If they do, let them try again
        if not entered_period.subject:
            if not cont_input:
                return cont_input
            else:
                print("Zum Beenden 'Eingabe beenden' drücken!")
                self.get_period(entered_period.prof)

        else:
            # add a Periods class item to the stundenplan frame. The row indices are created as int, so the str from
            # Period() has to be converted...
            self.prof_frame.loc[int(entered_period.time), entered_period.day] = entered_period.prof
            self.subj_frame.loc[int(entered_period.time), entered_period.day] = entered_period.subject
            if entered_period.additional_period:
                cont_input = self.get_period(entered_period.prof, entered_period.subject)   # to notice an end to input
            return cont_input

    def draw_timetable(self):
        prof_table = self.prof_frame
        prof_table[prof_table.isnull()] = " "
        subj_table = self.subj_frame
        subj_table[subj_table.isnull()] = " "
        latex_string = ""
        for i in self.prof_frame.columns:
            for j in self.prof_frame.index:
                prof = prof_table.loc[int(j), i]
                subj = subj_table.loc[int(j), i]
                latex_string = latex_string + r"\multicolumn{1}{p{4cm}|}{%s \newline %s} &" % (prof, subj)
            latex_string = latex_string + r"\\ "
        print(latex_string)