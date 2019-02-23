#!/usr/bin/python3
# -*- coding: utf-8 -*-
from tkinter import *
import tkinter.messagebox as messagebox
import pyperclip, win32com.client

spk = win32com.client.Dispatch('SAPI.SpVoice')
snS = set([])
limitValue = 0


class MY_GUI():
    def __init__(self, init_window＿name):
        self.init_window_name = init_window＿name

    def set_init_window(self):
        self.init_window_name.title('unfinished')
        self.init_window_name.geometry('480x320+10+10')
        self.init_window_name.resizable(False, False)  # 禁止调整窗口大小
        self.init_window_name.protocol('WM_DELETE_WINDOW', self.callback)  # 绑定系统'X'(退出)按键
        self.init_SN_label = Label(self.init_window_name, text='请输入SN:')
        self.init_SN_label.place(x=10, y=10)
        self.init_SN_LimitValue_label = Label(self.init_window_name, text='首次输入SN字符长度为限制值')
        self.init_SN_LimitValue_label.place(x=230, y=10)
        self.init_Stdout_Hint_label = Label(self.init_window_name, fg='green', text=(len(snS)), font=('黑体', 100))
        self.init_Stdout_Hint_label.place(x=320, y=90)
        self.init_Stderr_Hint_label = Label(self.init_window_name, fg='red', text='', font=('黑体', 50))
        self.init_Stderr_Hint_label.place(x=280, y=230)
        self.init_data_Listbox = Listbox(self.init_window_name)
        self.init_data_Listbox.place(x=5, y=40, width=220, height=240)
        self.init_data_Listbox_Scrollbar_Y = Scrollbar(self.init_window_name, command=self.init_data_Listbox.yview)
        self.init_data_Listbox_Scrollbar_Y.place(x=225, y=40, height=255)
        self.init_data_Listbox_Scrollbar_X = Scrollbar(self.init_window_name, orient=HORIZONTAL,
                                                       command=self.init_data_Listbox.xview)
        self.init_data_Listbox_Scrollbar_X.place(x=5, y=280, width=220)
        self.init_data_Entry = Entry(self.init_window_name)
        self.init_data_Entry.place(x=75, y=10, width=150)
        self.init_data_Entry.bind('<Return>', self.submit)  # 绑定回车键
        self.init_clip_button = Button(self.init_window_name, text='复制到剪贴板', bg='lightblue',
                                       width=10, command=self.copy_to_clip)
        self.init_clip_button.place(x=260, y=50)
        self.init_reset_button = Button(self.init_window_name, text='清除数据', bg='lightblue',
                                        width=10, command=self.reste)
        self.init_reset_button.place(x=360, y=50)

    def submit(self, ev=None):  # 参数需要加(ev = None))
        inValue = self.init_data_Entry.get()
        self.init_data_Entry.delete(0, END)  # 回车后清楚原Entry数据
        global snS, limitValue
        abv = len(snS)
        if len(snS) == 0:
            limitValue = len(inValue)
            self.init_SN_LimitValue_label.config(text=('字符长度限制为:', limitValue))
            snS.add(inValue)
            self.init_Stdout_Hint_label.config(text=(len(snS)))
            self.init_data_Listbox.insert(0, inValue)
            spk.Speak(len(snS))
        elif limitValue == len(inValue):
            snS.add(inValue)
            aav = len(snS)
            if abv == aav:
                self.init_Stderr_Hint_label.config(text='重复')
                spk.Speak('重复')
            else:
                self.init_Stderr_Hint_label.config(text='')
                self.init_Stdout_Hint_label.config(text=(aav))
                self.init_data_Listbox.insert(0, inValue)
                spk.Speak(aav)
        else:
            self.init_Stderr_Hint_label.config(text='错误')
            spk.Speak('错误')

    def copy_to_clip(self):
        global snS
        inCilp = [str(x) for x in snS]
        pyperclip.copy('\n'.join(inCilp))

    def reste(self):
        global snS, limitValue
        snS = set([])
        limitValue = 0
        self.init_SN_LimitValue_label.config(text=('首次输入SN字符长度为限制值'))
        self.init_Stdout_Hint_label.config(text=(len(snS)))
        self.init_Stderr_Hint_label.config(text='')
        self.init_data_Listbox.delete(0, END)

    def callback(self):
        global snS
        if len(snS) == 0:
            exit()
        elif messagebox.askyesno('警告', '有至少一组SN，是否继续退出'):
            self.init_window_name.destroy()


def gui_start():
    init_window = Tk()
    PORTAL = MY_GUI(init_window)
    PORTAL.set_init_window()
    init_window.mainloop()


gui_start()
