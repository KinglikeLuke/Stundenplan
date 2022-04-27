import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd


class Period:
    def __init__(self, prof=None, subject=None, time=None, day=None):
        self.subject, self.prof, self.time, self.day = subject, prof, time, day


class Interface(Period):
    """
    Erzeugt Eingabefenster. Wenn schon einige Optionen vorgegeben werden, werden diese auch angezeigt
    """
    def __init__(self, prof=None, subject=None, time=None, day=None):
        super().__init__(prof, subject, time, day)
        self.window = tk.Tk()
        self.times = np.arange(1, 7, 1)
        self.days = ["Mo", "Di", "Mi", "Do", "Fr"]
        self.prof_input, self.subject_input, self.time_input, self.day_input = self.setup_input()
        self.button()
        self.window.mainloop()

    def setup_input(self):
        prof_input = self.text_input(0, 0, "Name des Dozierenden", self.prof)
        subject_input = self.text_input(1, 0, "Name des Fachs", self.subject)
        time_input = self.opt_input(3, 0, self.times, "Doppelstunde")
        day_input = self.opt_input(4, 0, self.days, "Tag")
        return prof_input, subject_input, time_input, day_input


    def text_input(self, row, column, text, filled_text):
        """
        Erzeugt ein Texteingabefeld
        :param int row: y-Position im Fenster
        :param int column: x-Position im Fenster
        :param str text: Beschreibung der Eingabe
        :param str filled_text: Text der schon vor User-Eingabe im Feld steht
        :return: Eingabefeld name
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
        Erzeugt eine Dropdownliste aus options
        :param int row: y-Position im Fenster
        :param int column: x-Position im Fenster
        :param list options: Optionen in der Dropdown-Liste
        :param str text: Beschreibung der Eingabe
        :return: gewählte Option var
        """
        frame = tk.Frame(master=self.window, relief=tk.RAISED)
        frame.grid(row=row, column=column, padx=1, pady=1)
        lbl = tk.Label(text=text + ":",
                       master=frame)
        lbl.grid(row=0, column=0)
        var = tk.StringVar(self.window)                         # Rückgabevariable erzeugen
        opts = ttk.OptionMenu(frame, var, options[0], *options)
        opts.grid(row=0, column=1)
        return var

    def button(self):
        """Confirms setup_input"""
        frame_ok = ttk.Frame(master=self.window, relief=tk.RAISED)
        frame_ok.grid(row=5, column=0, padx=1, pady=1)
        button = ttk.Button(text="OK", master=frame_ok, command=self.get_info)
        button.pack()

    def get_info(self):
        """
        Sets the values of the container "Period" to the values written in the respective Field at button push.
        Closes window after
        """
        self.prof = self.prof_input.get()
        self.subject = self.subject_input.get()
        self.time = self.time_input.get()
        self.day = self.day_input.get()
        self.window.destroy()
