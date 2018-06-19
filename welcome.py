from login import *

#账号
def r1(root):
    global choice
    choice = 1
    root.destroy()

# 游客
def r0(root):
    global choice
    choice = 0
    root.destroy()

choice = 0
def DengLu():
    root = tk.Tk()
    root.title('请选择登录方式')
    yonghu=tk.Button(root,text="登录",bg='CornflowerBlue',fg='White',command=lambda :r1(root))
    yonghu.pack(padx=35, pady=25, side=tk.LEFT)
    youke=tk.Button(root,text="游客登录",bg='DimGray',fg='White',command=lambda :r0(root))
    youke.pack(padx=35, pady=25,side=tk.RIGHT)
    root.mainloop()
    return choice

