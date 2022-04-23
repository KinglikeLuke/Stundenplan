import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd


class Period:
    def __init__(self, subject=None, prof=None, time=None, day=None):
        self.subject, self.prof, self.time, self.day = subject, prof, time, day


class Interface():
    def __init__(self):
        self.window = tk.Tk()
        self.prof_input = self.get_prof()
        self.subject_input = self.get_subject()
        self.time_input = self.get_time()
        self.day_input = self.get_day()
        self.Period = Period()
        self.button()
        self.window.mainloop()

    def get_prof(self):
        frame_prof = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_prof.grid(row=0, column=0, padx=1, pady=1)        # Frame positionieren
        label_prompt = tk.Label(master=frame_prof,
                                text='Name des Dozierenden:',
                                width=20,
                                height=2)
        label_prompt.pack()                                     # Label im Frame Positionieren
        name_prof = tk.Entry(master=frame_prof)
        name_prof.pack()
        return name_prof

    def get_subject(self):
        frame_subject = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_subject.grid(row=1, column=0, padx=1, pady=1)
        label_prompt = tk.Label(master=frame_subject,
                                text='Name des Fachs:',
                                width=20,
                                height=2)
        label_prompt.pack()
        name_subject = tk.Entry(master=frame_subject)
        name_subject.pack()
        return name_subject

    def get_time(self):
        frame_time = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_time.grid(row=3, column=0, padx=1, pady=1)
        lbl_time = tk.Label(text='Doppelstunde:',
                              master=frame_time)
        lbl_time.grid(row=0, column=0)
        times = np.arange(1, 7, 1)
        time_var = tk.StringVar(self.window)
        time_opts = ttk.OptionMenu(frame_time, time_var, times[0], *times)
        time_opts.grid(row=0, column=1)
        return time_var

    def get_day(self):
        frame_day = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_day.grid(row=4, column=0, padx=1, pady=1)
        lbl_day = tk.Label(text='Tag:',
                           master=frame_day)
        lbl_day.grid(row=0, column=0)
        days = ["Mo", "Di", "Mi", "Do", "Fr"]
        day_var = tk.StringVar(self.window)
        day_opts = ttk.OptionMenu(frame_day, day_var, days[0], *days)
        day_opts.grid(row=0, column=1)
        return day_var

    def button(self):
        frame_ok = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_ok.grid(row=5, column=0, padx=1, pady=1)
        button = ttk.Button(text="OK", master=frame_ok, command=self.get_info)
        button.pack()

    def get_info(self):
        self.Period.prof = self.prof_input.get()
        self.Period.subject = self.subject_input.get()
        self.Period.time = self.time_input.get()
        self.Period.day = self.day_input.get()
        self.window.destroy()