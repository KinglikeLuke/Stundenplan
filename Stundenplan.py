import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import pandas as pd


class Period:
    def __init__(self, name, prof, ds, day):
        self.name, self.prof, self.ds, self.day = name, prof, ds, day


class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.get_prof()
        self.get_subject()
        self.get_period()
        self.get_day()
        self.window.mainloop()

    def get_prof(self):
        frame_prof = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_prof.grid(row=0, column=0, padx=1, pady=1)
        label_prompt = tk.Label(master=frame_prof,
                                text='Name des Dozierenden:',
                                width=20,
                                height=2)
        label_prompt.pack()
        entry_prof = tk.Entry(master=frame_prof)
        entry_prof.pack()

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

    def get_period(self):
        frame_period = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_period.grid(row=3, column=0, padx=1, pady=1)
        lbl_period = tk.Label(text='Doppelstunde:',
                              master=frame_period)
        lbl_period.grid(row=0, column=0)
        periods = np.arange(1, 7, 1)
        init_period = tk.StringVar(self.window)
        period_opts = ttk.OptionMenu(frame_period, init_period, periods[0], *periods)
        period_opts.grid(row=0, column=1)

    def get_day(self):
        frame_day = tk.Frame(master=self.window, relief=tk.RAISED)
        frame_day.grid(row=4, column=0, padx=1, pady=1)
        lbl_day = tk.Label(text='Tag:',
                           master=frame_day)
        lbl_day.grid(row=0, column=0)
        days = ["Mo", "Di", "Mi", "Do", "Fr"]
        init_days = tk.StringVar(self.window)
        period_opts = ttk.OptionMenu(frame_day, init_days, days[0], *days)
        period_opts.grid(row=0, column=1)
