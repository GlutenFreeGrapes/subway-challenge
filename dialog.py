from tkinter import simpledialog, filedialog

s=simpledialog.askstring('title', 'gib string')
print(s)

simpledialog.askfloat('title', 'gib float')
simpledialog.askinteger('title', 'gib int')

filedialog.askopenfile()
filedialog.askopenfiles()
filedialog.askopenfilename()
filedialog.askopenfilenames()
s=filedialog.askdirectory(initialdir='')
print(s)
