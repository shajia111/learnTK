#!/usr/bin/python3
# -*- coding: utf-8 -*-
import tkinter
root=tkinter.Tk()

scrolly=tkinter.Scrollbar(root)
scrolly.pack(side=tkinter.RIGHT,fill=tkinter.Y)
mylb=tkinter.Listbox(root,yscrollcommand=scrolly.set)
mylb.pack()

for item in range(1,20):
    mylb.insert(tkinter.END,item)
scrolly.config(command=mylb.yview)
tkinter.mainloop()