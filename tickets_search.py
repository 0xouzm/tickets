#coding=utf-8
import tkinter as tk
from ticketsCLI import *
import tkinter.messagebox

def onBtn():

    from_station = e1.get()
    to_station = e2.get()
    date = e3.get()
    #
    # if not (from_station or to_station or date):
    #     tkinter.messagebox.showerror(title='Error', message='请输入完整查询信息')
    # elif from_station not in stations.names:
    #     tkinter.messagebox.showerror(title='Error', message='请输入正确的出发城市')
    # elif to_station not in stations.names:
    #     tkinter.messagebox.showerror(title='Error', message='请输入正确的到达城市')
    # else:
    try:
        s=Cli(from_station, to_station, date)
        search_result = s.run()
        for i in search_result:
            print(i)
    except ValueError:
        tkinter.messagebox.showerror(title='Error', message='请输入有效信息')


root = tk.Tk()
root.title('火车票查询系统1.0')
# root.geometry('250x250')
search = tk.Frame(root)
label1 = tk.Label(search, text='出发地:')
e1 = tk.Entry(search)
label1.pack()
e1.pack(padx=50, pady=20)


label2 = tk.Label(search, text='到达地:')
e2 = tk.Entry(search)
label2.pack()
e2.pack(padx=50, pady=20)

label3 = tk.Label(search, text='日期:(xxxx-xx-xx)')
e3 = tk.Entry(search)
label3.pack()
e3.pack(padx=50, pady=20)

btn = tk.Button(search, text="查询",command=onBtn)
btn.pack(padx=50, pady=20)

search.pack()

root.mainloop()
