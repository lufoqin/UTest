import tkinter
import tkinter.simpledialog
import json


 
def formatparams():
    params_after={}
    params_before = tkinter.simpledialog.askstring(title = '获取信息',prompt='请输入参数：',initialvalue = '')
    print("转换前的接口参数：\n"+params_before)
    params_before=params_before.splitlines(keepends=False)
    for param in params_before:
        key,value=param.split(':')
        value=value.replace(" ", "")
        if value=='true' or value=='True':
            value=True
        elif value=='false' or value=='False':
            value=False
        params_after[key]=value
    print("转换后的接口参数：\n")
    print(params_after)

root = tkinter.Tk()
root.minsize(300,300)     
btn = tkinter.Button(root,text = '点击输入待转换的接口参数',command = formatparams)
btn.pack()
root.mainloop()
