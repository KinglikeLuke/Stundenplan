import tkinter as tk
import tkinter.ttk as ttk
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})


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

    def __init__(self, prof=None, subject=None, time=None, day=None, prof_frame=None, subj_frame=None):
        super().__init__(prof, subject, time, day)  # Initialise Period for base info
        self.subj_frame, self.prof_frame = subj_frame, prof_frame   # Forgive me
        self.window = tk.Tk()  # create window
        self.time_input = self.opt_input(3, 0, self.times, "Doppelstunde")
        self.day_input = self.opt_input(4, 0, self.days, "Tag")
        self.pull_info(init=True)   # check if there's something written in the first field
        self.prof_input = self.text_input(0, 0, "Name des Dozierenden", self.prof)
        self.subject_input = self.text_input(1, 0, "Name des Fachs", self.subject)
        self.button(5, 0, "OK", self.get_info)
        self.button(6, 0, "Zusätzliche ähnliche Stunde", self.get_additional_info)
        self.button(7, 0, "Eingabe beenden", self.get_final_info)
        self.additional_period = False
        self.cont_input = True
        self.window.mainloop()

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
        opts = ttk.OptionMenu(frame, var, options[0], *options, command=self.pull_info)
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

    def pull_info(self, *args, init=False):
        """
        Pulls information from given timetable and sets it as the current info. *args has the current option of
        the dropdown used to get here, but as no one knows which dropdown it was, it just gets thrown away.
        :param: bool init: whether this is called before prof_input and subject_input is defined
        :return:
        """
        time = self.time_input.get()
        day = self.day_input.get()
        if self.prof_frame.loc[int(time), day]:
            self.prof = self.prof_frame.loc[int(time), day]
            self.subject = self.subj_frame.loc[int(time), day]
            if not init:
                self.prof_input = self.text_input(0, 0, "Name des Dozierenden", self.prof)
                self.subject_input = self.text_input(1, 0, "Name des Fachs", self.subject)

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
    def __init__(self, timetable_name=None):
        """
        :param: str timetable_name: name of already created timetable
        """
        self.directory = "SavedTimetables"
        if timetable_name:
            self.prof_frame = pd.read_csv(f'./{self.directory}/{timetable_name}_prof_raw', index_col=0,
                                          keep_default_na=False)
            self.subj_frame = pd.read_csv(f'./{self.directory}/{timetable_name}_subj_raw', index_col=0,
                                          keep_default_na=False)

        else:
            self.prof_frame = pd.DataFrame(columns=Period().days, index=Period().times)
            self.subj_frame = pd.DataFrame(columns=Period().days, index=Period().times)
            self.prof_frame[self.prof_frame.isnull()] = ""  # clear out all the NaN entries
            self.subj_frame[self.subj_frame.isnull()] = ""

        self.build_timetable()

    def build_timetable(self):
        cont_input = True
        while cont_input:
            cont_input = self.get_period()  # get user inputs, also check if the input is stopped

    def get_period(self, prof=None, subject=None):
        """
        Gets Period names from Interface class, adds them to periods list
        :param prof:
        :param subject:
        :return: bool cont_input: whether new input should be read in
        """
        entered_period = Interface(prof=prof, subject=subject, prof_frame=self.prof_frame, subj_frame=self.subj_frame)
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
                cont_input = self.get_period(entered_period.prof, entered_period.subject)  # to notice an end to input
            return cont_input

    def save_timetable(self, title, fig):
        try:
            os.makedirs(f'./{self.directory}/')
        except OSError as exc:
            pass
        self.prof_frame.to_csv(f"./{self.directory}/{title}_prof_raw")
        self.subj_frame.to_csv(f"./{self.directory}/{title}_subj_raw")
        fig.savefig(f"./{self.directory}/{title}_Stundenplan.pdf")

    def draw_timetable(self, title):
        """
        Dont ask. Draws a timetable from a latex-formatted string in the worst possible way with pyplot
        :return:
        """
        time_verbose = [r"\begin{tabular}{@{}c@{}} 1. DS \\ 7:30-9:00 \end{tabular}",
                        r"\begin{tabular}{@{}c@{}} 2. DS \\ 9:20-10:50 \end{tabular}",
                        r"\begin{tabular}{@{}c@{}} 3. DS \\ 11:10-12:40 \end{tabular}",
                        r"\begin{tabular}{@{}c@{}} 4. DS \\ 13:00-14:30 \end{tabular}",
                        r"\begin{tabular}{@{}c@{}} 5. DS \\ 14:50-16:20 \end{tabular}",
                        r"\begin{tabular}{@{}c@{}} 6. DS \\ 16:40-18:10 \end{tabular}"]

        latex_string = (r"\begin{table}[] "
                        r"\centering "
                        r"\begin{tabular}{c|c|c|c|c|c} &")
        for i in self.prof_frame.columns:
            latex_string = latex_string + r"%s &" % i
        latex_string = latex_string[:-1] + r"\\ \hline"

        for i in self.prof_frame.index:
            latex_string = latex_string + r"%s &" % time_verbose[int(i) - 1]
            for j in self.prof_frame.columns:
                prof = self.prof_frame.loc[int(i), j]
                subj = self.subj_frame.loc[int(i), j]
                latex_string = latex_string + r"\begin{tabular}{@{}c@{}}%s \\ %s\end{tabular}&" % (prof, subj)
            latex_string = latex_string[:-1] + r"\\ \hline "

        latex_string = latex_string + (r"\end{tabular}"
                                       r"\caption{Stundenplan}"
                                       r"\end{table}"
                                       r"\end{document}")

        fig = plt.figure()
        ax = fig.subplots()
        ax.text(0.15, 0.3, latex_string)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        self.save_timetable(title, fig)

