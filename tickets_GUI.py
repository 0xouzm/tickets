import tkinter as tk
from tickets import *
import tkinter.messagebox

# -d    动车
# -g    高铁
# -k    快速
# -t    特快
# -z    直达


def onBtn():
    from_station = e1.get()
    to_station = e2.get()
    date = e3.get()
    try:
        s = Search(from_station, to_station, date, options={'-d': d.get(), '-g': g.get(), '-k': k.get(),
                                                         '-t': t.get(), '-z': z.get()})
        trains = s.run()

    except Exception:
        tkinter.messagebox.showerror(title='Error', message='请输入有效信息')

    print(trains)
    # print(prices)

root = tk.Tk()
root.title('火车票查询系统0.2')
# root.geometry('250x250')


search = tk.Frame(root)
search.pack(pady=10)

label1 = tk.Label(search, text='出发地:')
e1 = tk.Entry(search)
label1.pack()
e1.pack(padx=5, pady=5)


label2 = tk.Label(search, text='到达地:')
e2 = tk.Entry(search)
label2.pack()
e2.pack(padx=5, pady=5)

label3 = tk.Label(search, text='日期:(xxxx-xx-xx)')
e3 = tk.Entry(search)
label3.pack()
e3.pack(padx=5, pady=5)


lf = tk.LabelFrame(search, text="车型选择")
lf.pack(padx=10)

d = tk.IntVar(search, value=1)
g = tk.IntVar(search, value=1)
k = tk.IntVar(search, value=1)
t = tk.IntVar(search, value=1)
z = tk.IntVar(search, value=1)

rb1 = tk.Checkbutton(lf, text='动车', variable=d)
rb1.pack(side=tk.LEFT)

rb2 = tk.Checkbutton(lf, text='高铁', variable=g)
rb2.pack(side=tk.LEFT)

rb3 = tk.Checkbutton(lf, text='快车', variable=k)
rb3.pack(side=tk.LEFT)

rb4 = tk.Checkbutton(lf, text='特快', variable=t)
rb4.pack(side=tk.LEFT)

rb5 = tk.Checkbutton(lf, text='直达', variable=z)
rb5.pack(side=tk.LEFT)


btn = tk.Button(search, text="查询", command=onBtn)
btn.pack(padx=50, pady=20)


root.mainloop()
