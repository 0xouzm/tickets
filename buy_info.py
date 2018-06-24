import tkinter as tk

# 2018-07-01
# K503
# 重庆北
# 0643
# 成都东
# 1053
# ('3', ['巫家竞', '男', '500109199203150431', '成人', '15702387382'])
# ('1', ['董哲彤', '男', '50010519951009581X', '成人', ''])
# ('2', ['范朝艳', '女', '52273119940925758X', '成人', ''])
# ticket_num: ["RW_num':'1'", "WZ_num':'14'", "YW_num':'101'", "YZ_num':'122'"]
# price: ["RW_price':'01405'", "WZ_price':'00465'", "YW_price':'00925'", "YZ_price':'00465'"]


def confirm_snp(t_file):
    root = tk.Tk()
    root.geometry('800x800')
    # 列车信息
    l1 = tk.Label(root, text='列车信息(余票信息仅供参考)', bg='blue', fg="white")
    l1.pack(anchor='nw', ipady=20)
    # 列车信息显示
    f = tk.Frame(root)
    f.pack(anchor='nw')

    l2 = tk.Label(f, text='2018-06-20', bg='blue')
    l2.pack(side=tk.LEFT)
    l3 = tk.Label(f, text='G153次', bg='blue')
    l3.pack(side=tk.LEFT)

    l4 = tk.Label(f, text='北京南站', bg='blue')
    l4.pack(side=tk.LEFT)

    l5 = tk.Label(f, text='(8:00开)', bg='blue')
    l5.pack(side=tk.LEFT)

    l6 = tk.Label(f, text='—上海站', bg='blue')
    l6.pack(side=tk.LEFT)

    l7 = tk.Label(f, text='(20:52到)', bg='blue')
    l7.pack(side=tk.LEFT)

    # 座位信息
    f2 = tk.Frame(root)
    f2.pack(anchor='nw', ipady=20)

    v = tk.IntVar(f2, value=0)
    rb1 = tk.Radiobutton(f2, text='商务票(￥999)1张', variable=v, value=0)
    rb1.pack(side=tk.LEFT)

    rb2 = tk.Radiobutton(f2, text='一等座(￥444)12张', variable=v, value=1)
    rb2.pack(side=tk.LEFT)

    rb3 = tk.Radiobutton(f2, text='二等座(￥232)15张', variable=v, value=2)
    rb3.pack(side=tk.LEFT)

    # 乘客信息

    root.mainloop()


if __name__ == '__main__':
    confirm_snp()
