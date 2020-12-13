
import threading
import codecs

from pos import main
from tkinter import *

#---------------------------------------

def call_func():

	main()
	with codecs.open("./output/hindi_tags.txt", 'r',encoding='utf-8') as f:
		for line in f:
			l = line
			lbl3.configure(text=l)
			break


def clicked():
	res = "Got data: " + txt.get()
	with codecs.open("./data/hindi_testing.txt", 'w',encoding='utf-8') as f:
		f.write(txt.get())

	call_func()

#---------------------------------------

window = Tk()
window.title("POS Tagger for Hindi Language!")
window.geometry('640x400')

col_count, row_count = 5, 5

for col in range(col_count):
	window.grid_columnconfigure(col, minsize=60)

for row in range(row_count):
	window.grid_rowconfigure(row, minsize=60)

lbl1 = Label(window, text="Enter your text here: ")
lbl1.grid(column=1, row=0)

txt = Entry(window,width=60)
txt.grid(column=2, row=0)

btn = Button(window, text="Start", command=clicked)
btn.grid(column=3, row=0)

lbl2 = Label(window, text="Result:")
lbl2.grid(column=1, row=1)

lbl3 = Label(window, text="")
lbl3.grid(column=2, row=1)

window.mainloop()
