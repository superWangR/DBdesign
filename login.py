import datetime
import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import  pymysql
from PIL import Image, ImageTk

window = tk.Tk()
window.title("住院管理信息系统");
window.geometry("550x240+550+300")
window.resizable(0, 0)

var1 = tk.StringVar()
var2 = tk.StringVar()

tk.Label(text='用户名:',font = 20).place(x=10,y=20)
e1 = tk.Entry(show = None,textvariable =var1,font = 20,width = 15)
e1.place(x = 150,y=20)

tk.Label(text='密码:',font = 20).place(x=10,y=70)
e2 = tk.Entry(show = '*',textvariable =var2,font = 20,width = 15)
e2.place(x= 150,y=70)

img = Image.open('picture/hospital.png')  # 打开图片
photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
imglabel = tk.Label(window, image=photo).place(x = 310,y=20)

def login():
    user = var1.get()
    psw = var2.get()
    print(user,psw)
    conn = pymysql.connect(host='localhost', user='root', password='123123', port=3306)
    cur = conn.cursor()
    cur.execute("use hospital;")
    sql='select * from identity where id=%s and psw=%s'
    cur.execute(sql,(user,psw))
    data = cur.fetchone()
    print(data)
    if data==None:
        tk.messagebox.askquestion(title='警告', message='错误的用户名或密码\n                                    or\n您没有权限登陆该系统')
    else:
        name = data[1]
        job = data[3]
        if job == '导诊护士':
            window.destroy()
            mainwindow = tk.Tk()
            mainwindow.title('导诊主界面')
            #mainwindow.state('zoomed')
            mainwindow.geometry("1100x700+250+120")
            mainwindow.resizable(0, 0)
            tk.Label(text='早上好 ! ' + job +':'+name , font=25).place(x=20, y=20)  # 问候语
            img = Image.open('picture/hospital.png')  # 打开图片
            photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
            tk.Label(mainwindow, image=photo).place(x=800, y=500)

            def apply():
                lp1 = tk.Label(text='患者ID:', font=20)
                lp1.place(x=50, y=60)
                varNo = tk.StringVar()
                le1 = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                le1.place(x=250, y=60)
                lp2 = tk.Label(text='患者姓名 :', font=20)
                lp2.place(x=50, y=100)
                varName = tk.StringVar()
                le2 = tk.Entry(show=None, textvariable=varName, font=21, width=15)
                le2.place(x=250, y=100)
                lp3 = tk.Label(text='患者年龄 :', font=20)
                lp3.place(x=50, y=140)
                varAge = tk.IntVar()
                le3 = tk.Entry(show=None, textvariable=varAge, font=21, width=15)
                le3.place(x=250, y=140)
                lp4 = tk.Label(text='患者性别 :', font=20)
                lp4.place(x=50, y=180)
                varSex = tk.StringVar()
                le4 = tk.Entry(show=None, textvariable=varSex, font=21, width=15)
                le4.place(x=250, y=180)
                lp5 = tk.Label(text='联系方式 :', font=20)
                lp5.place(x=50, y=220)
                varPhone = tk.StringVar()
                le5 = tk.Entry(show=None, textvariable=varPhone, font=21, width=15)
                le5.place(x=250, y=220)

                def submit():
                    num = varNo.get()
                    name = varName.get()
                    phone = varPhone.get()
                    sex = varSex.get()
                    age = varAge.get()
                    # print(dept_name, num, name, phone, sex, age, deposit, now_time, bed)  # 获取所有文本框中的输入
                    sql = 'insert into patient (p_num,p_name,p_sex,p_age,p_phone) values(%s,%s,%s,%s,%s)'
                    try:
                        cur.execute(sql, (num, name, sex, age, phone))  # 将患者信息插入patient表中
                        conn.commit()
                        tk.messagebox.showwarning(title='提示',message='提交成功！')
                    except Exception:
                        tk.messagebox.showwarning(title='警告', message='提交失败！')
                        conn.rollback()

                def cancel():
                    lp1.destroy()
                    lp2.destroy()
                    lp3.destroy()
                    lp4.destroy()
                    lp5.destroy()


                    le1.destroy()
                    le2.destroy()
                    le3.destroy()
                    le4.destroy()
                    le5.destroy()


                    b1.destroy()
                    b2.destroy()

                b1 = tk.Button(text='录入系统', font=20, command=submit)
                b1.place(x=70, y=350)
                b2 = tk.Button(text='取消', font=20, command=cancel)
                b2.place(x=220, y=350)

            def search():
                sql = 'select dept_name from department'
                cur.execute(sql)
                dept = cur.fetchall()
                print(dept)
                l1 = tk.Label(text='科室选择 :', font=20)
                l1.place(x=50, y=260)
                deptList = ttk.Combobox(font=20, width=50)
                deptList.place(x=250, y=260)
                deptList['value'] = dept

                def query():
                    deptname = deptList.get()
                    sql = 'select count(*) from bed where dept_name=%s and bed_state=1'
                    cur.execute(sql,(deptname))
                    result = cur.fetchone()
                    print(result)
                    number = str(result[0])
                    tk.messagebox.askquestion(title='提示',
                                              message=deptname+'剩余床位数：'+number)

                def cancel():
                    l1.destroy()
                    b1.destroy()
                    b2.destroy()
                    deptList.destroy()

                b1 = tk.Button(text='搜索', font=20, command=query)
                b1.place(x=70, y=350)
                b2 = tk.Button(text='取消', font=20, command=cancel)
                b2.place(x=220, y=350)

            menubar = tk.Menu(mainwindow)
            Service = tk.Menu(menubar, tearoff=0)  # 服务菜单
            menubar.add_cascade(label='选项', menu=Service)  # 入院、出院登记
            Service.add_command(label='填写住院登记', command=apply)
            Service.add_command(label='剩余床位查询', command=search)
            # Service.add_command(label='Discharge Registration', command=discharge)

            mainwindow.config(menu=menubar)
            mainwindow.mainloop()

        if job=='收银员' :                                 #收费员主界面
            window.destroy()
            mainwindow = tk.Tk()
            mainwindow.title('收银员主界面')
            mainwindow.geometry("1100x700+250+120")
            mainwindow.resizable(0, 0)
            tk.Label(text='早上好 ! ' + job + ':' + name, font=25).place(x=20, y=20)  # 问候语
            img = Image.open('picture/hospital.png')  # 打开图片
            photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
            tk.Label(mainwindow, image=photo).place(x=800, y=500)


            def admission():      #确认信息后，办理住院手续
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=50, y=60)
                varNo = tk.StringVar()
                e1 = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                e1.place(x=250, y=60)
                t = tk.Text(height=5, font=20)
                t.place(x=50,y=100)
                t.insert('end', '患者信息：\n')
                l2 = tk.Label(text='押金 :', font=20)
                l2.place(x=50, y=260)
                varDeposit = tk.DoubleVar()
                e2 = tk.Entry(show=None, textvariable=varDeposit, font=21, width=15)
                e2.place(x=250, y=260)


                def search():
                    num = varNo.get()
                    sql = 'select p_name,p_sex,p_age,p_phone from patient where p_num=%s'
                    cur.execute(sql,(num))
                    data = cur.fetchone()
                    name = data[0]
                    sex = data[1]
                    age = str(data[2])
                    phone = data[3]
                    result = '姓名：'+name+'\n性别：'+sex+'\n年龄：'+age+'\n联系方式：'+phone
                    print(data)
                    t.insert('end',result)

                def submit():
                    num = varNo.get()
                    deposit = varDeposit.get()
                    now_time = datetime.datetime.now()
                    sql = 'update patient set admissionTime=%s,deposit=%s where p_num=%s'
                    try:
                        cur.execute(sql,(now_time,deposit,num))  #将患者信息插入patient表中
                        conn.commit()
                        tk.messagebox.showinfo(title='提示：',message='提交成功！')

                    except Exception:
                        print(Exception)
                        tk.messagebox.showwarning(title='警告：',message='提交失败！')
                        conn.rollback()


                def cancel():
                    l1.destroy()
                    l2.destroy()
                    e1.destroy()
                    e2.destroy()
                    lb1.destroy()
                    lb2.destroy()
                    lb3.destroy()
                    t.destroy()


                lb1 = tk.Button(text='搜索',font=20,command =search)
                lb1.place(x=550,y=55)
                lb2 = tk.Button(text='取消', font=20, command=cancel)
                lb2.place(x=650, y=55)
                lb3 = tk.Button(text='提交', font=20, command=submit)
                lb3.place(x=50, y=350)


            def discharge():
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=50, y=60)
                varNo = tk.StringVar()
                e1 = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                e1.place(x=250, y=60)
                t = tk.Text(height = 10,font=20)
                t.insert('end','患者历史：\n')
                t.place(x=50,y=110)

                def query():
                    pnum = varNo.get()
                    sql = 'select items.i_name,i_cost,takeTime from takes natural join items where p_num=%s'
                    cur.execute(sql,(pnum))
                    items = cur.fetchall()
                    print(data)
                    global sum
                    sum = 0
                    for item in items:
                        iname = item[0]
                        icost = str(item[1])
                        itime = item[2].strftime("%Y-%m-%d %H:%M:%S")
                        st = '检查项目名称：'+iname+' 费用：' + icost+' 时间：' + itime+'\n'
                        t.insert('end',st)
                        sum=sum+item[1]
                    print(sum)

                    sql = 'select medicine.m_name,medicine.m_cost,count,takeTime from medicine natural join prescription where p_num=%s'
                    cur.execute(sql,(pnum))
                    meds = cur.fetchall()
                    print(meds)
                    for med in meds:
                        mname = med[0]
                        mcost = str(med[1])
                        count = str(med[2])
                        mtime = med[3].strftime("%Y-%m-%d %H:%M:%S")
                        st = '处方名称：' + mname + ' 费用：' + mcost + ' 数量：'+count+' 时间：' + mtime + '\n'
                        t.insert('end',st)
                        sum=sum+med[2]*med[1]
                    print(sum)

                    global now_time
                    now_time = datetime.datetime.now()
                    sql = 'select admissionTime,deposit from patient where p_num=%s'
                    cur.execute(sql,(pnum))
                    result = cur.fetchone()
                    admissionTime = result[0]
                    global deposit
                    deposit = result[1]
                    difference = now_time-admissionTime
                    daynum = difference.days
                    print(daynum)
                    print(type(daynum))
                    st = '入院时间：'+admissionTime.strftime("%Y-%m-%d %H:%M:%S")+' 押金：'+ str(deposit)+' 累计入院：'+str(daynum)+' 天\n'
                    t.insert('end',st)
                    pay=40  #每日床位费
                    sum = sum +daynum*pay
                    print(sum)
                    st = '合计：'+str(sum)+' 元'
                    t.insert('end',st)

                def cal():
                    print(sum,deposit)
                    pnum = varNo.get()
                    sql = 'update patient set leaveTime=%s,total=%s where p_num=%s'
                    cur.execute(sql,(now_time,sum,pnum))
                    differ = deposit-sum
                    if differ>0:
                        tk.messagebox.showinfo(title='提示',message='办理成功！退还剩余押金'+str(differ)+'元')
                    else:
                        differ = -differ
                        tk.messagebox.showinfo(title='提示',message='办理成功！需补交金额'+str(differ)+'元')



                def cancel():
                    b1.destroy()
                    b2.destroy()
                    b3.destroy()
                    l1.destroy()
                    e1.destroy()
                    t.destroy()

                b1 = tk.Button(text='搜索', font=20, command=query)
                b1.place(x=500, y=60)
                b2 = tk.Button(text='取消', font=20, command=cancel)
                b2.place(x=600, y=60)
                b3 = tk.Button(text='结算', font=20, command=cal)
                b3.place(x=50, y=600)

            menubar = tk.Menu(mainwindow)
            Service = tk.Menu(menubar, tearoff=0)  # 服务菜单
            menubar.add_cascade(label='选项', menu=Service)                #入院、出院登记
            Service.add_command(label='入院缴费', command=admission)
            Service.add_command(label='出院结算', command=discharge)


            mainwindow.config(menu=menubar)
            mainwindow.mainloop()

        if job=='病区护士':
            window.destroy()
            mainwindow = tk.Tk()
            mainwindow.title('病区主界面')
            mainwindow.geometry("1100x700+250+120")
            mainwindow.resizable(0, 0)
            tk.Label(text='早上好 ! ' + job + ':' + name, font=25).place(x=20, y=20)  # 问候语
            img = Image.open('picture/hospital.png')  # 打开图片
            photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
            tk.Label(mainwindow, image=photo).place(x=800, y=500)

            def info():
                varNo = tk.StringVar()
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=40, y=60)
                No = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                No.place(x=240, y=60)
                t = tk.Text(height=7, width=100, font=21)
                t.place(x=40, y=100)
                t.insert('1.0', '详细信息 :\n')

                def query():
                    pass
                def cancel():
                    l1.destroy()
                    No.destroy()
                    t.destroy()
                    lb2.destroy()
                    lb3.destroy()

                lb2 = tk.Button(text='搜索', font=20, command=query)
                lb2.place(x=550, y=55)
                lb3 = tk.Button(text='取消', font=20, command=cancel)
                lb3.place(x=650, y=55)

            def allocate():
                sql = 'select dept_name from department'
                cur.execute(sql)
                dept = cur.fetchall()
                print(dept)
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=50, y=60)
                varNo = tk.StringVar()
                No = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                No.place(x=240, y=60)
                l2 = tk.Label(text='科室选择 :', font=20)
                l2.place(x=50, y=100)
                deptList = ttk.Combobox(font=20, width=50)
                deptList.place(x=240, y=100)
                deptList['value'] = dept
                t = tk.Text(height=3,font=20)
                t.place(x=50,y=150)
                t.insert('end','空闲床位号：\n')
                varbnum = tk.StringVar()
                l3 = tk.Label(text='床位选择 :', font=20)
                l3.place(x=50, y=320)
                e1 = tk.Entry(show=None, textvariable=varbnum, font=21, width=15)
                e1.place(x=240, y=320)

                def query():
                    deptname = deptList.get()
                    sql = 'select bed_num from bed where dept_name=%s and bed_state=1'
                    cur.execute(sql, (deptname))
                    result = cur.fetchone()
                    print(result)
                    t.insert('end',result)


                def allo():
                    pnum = varNo.get()
                    bnum = varbnum.get()
                    deptname = deptList.get()
                    now_time = datetime.datetime.now()
                    sql = 'insert into deptrecord(p_num,dept_name,inTime,bed_num) values (%s,%s,%s,%s)'
                    try:
                        cur.execute(sql,(pnum,deptname,now_time,bnum))
                        conn.commit()
                        tk.messagebox.showinfo(title='提示',
                                              message='提交成功！')
                    except Exception:
                        conn.rollback()
                        tk.messagebox.showwarning(title='警告',message='提交失败！')
                    sql = 'update bed set bed_state=0 where dept_name=%s and bed_num=%s'
                    try:
                        cur.execute(sql,(deptname,bnum))
                        conn.commit()
                    except Exception:
                        conn.rollback()
                        tk.messagebox.showwarning(title='警告', message='提交失败！')

                def cancel():
                    l1.destroy()
                    l2.destroy()
                    l3.destroy()
                    t.destroy()
                    e1.destroy()
                    b1.destroy()
                    b2.destroy()
                    b3.destroy()
                    No.destroy()
                    deptList.destroy()

                b1 = tk.Button(text='搜索', font=20, command=query)
                b1.place(x=890, y=95)
                b2 = tk.Button(text='取消', font=20, command=cancel)
                b2.place(x=980, y=95)
                b3 = tk.Button(text='分配床位', font=20, command=allo)
                b3.place(x=450, y=320)

            def transferout():
                sql = 'select dept_name from department'
                cur.execute(sql)
                dept = cur.fetchall()
                print(dept)
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=50, y=60)
                varNo = tk.StringVar()
                No = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                No.place(x=240, y=60)
                l2 = tk.Label(text='科室选择 :', font=20)
                l2.place(x=50, y=100)
                deptList = ttk.Combobox(font=20, width=50)
                deptList.place(x=240, y=100)
                deptList['value'] = dept

                def transfer():
                    pnum = varNo.get()
                    deptname = deptList.get()
                    now_time = datetime.datetime.now()
                    sql = 'select bed_num from deptrecord where p_num=%s'
                    try:
                        cur.execute(sql, (pnum))
                        result = cur.fetchone()
                        bnum = result[0]
                        print(bnum)
                        conn.commit()
                    except Exception:
                        conn.rollback()
                        tk.messagebox.showwarning(title='警告', message='提交失败！')

                    sql = 'update bed set bed_state=1 where dept_name=%s and bed_num=%s'
                    try:
                        cur.execute(sql, (deptname,bnum))
                        conn.commit()
                    except Exception:
                        conn.rollback()
                        tk.messagebox.showwarning(title='警告', message='提交失败！')

                    sql = 'update deptrecord set outTime=%s where p_num=%s'
                    try:
                        cur.execute(sql,(now_time,pnum))
                        conn.commit()
                        tk.messagebox.showinfo(title='提示',message='提交成功！')
                    except Exception:
                        conn.rollback()
                        tk.messagebox.showwarning(title='警告',message='提交失败！')

                def cancel():
                    l1.destroy()
                    l2.destroy()
                    No.destroy()
                    deptList.destroy()
                    b1.destroy()
                    b2.destroy()

                b1 = tk.Button(text='转出', font=20, command=transfer)
                b1.place(x=890, y=95)
                b2 = tk.Button(text='取消', font=20, command=cancel)
                b2.place(x=980, y=95)



            menubar = tk.Menu(mainwindow)
            Condition = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label='选项', menu=Condition)
            Condition.add_command(label='患者信息', command=info)
            Condition.add_command(label='分配病床', command=allocate)
            Condition.add_command(label='科室转出', command=transferout)

            # Transfer = tk.Menu(menubar, tearoff = 0)  # tearoff意为下拉         #转科室菜单
            # menubar.add_cascade(label = 'PatientTransfer',menu = Transfer)
            # Transfer.add_command(label='Patient Out', command=out)
            # Transfer.add_command(label='Patient In', command=In)
            mainwindow.config(menu=menubar)
            mainwindow.mainloop()


        if job == '医生':                       #医生主界面
            #job = 'Doc.'
            window.destroy()
            mainwindow = tk.Tk()
            mainwindow.title('医生主界面')
            mainwindow.geometry("1100x700+250+120")
            mainwindow.resizable(0, 0)
            tk.Label(text='早上好 ! ' + job + ':' + name, font=25).place(x=20, y=20)  # 问候语
            img = Image.open('picture/hospital.png')  # 打开图片
            photo = ImageTk.PhotoImage(img)  # 用PIL模块的PhotoImage打开
            tk.Label(mainwindow, image=photo).place(x=800, y=500)

            def diagnose():                #诊断 菜单键
                varNo = tk.StringVar()
                l1 = tk.Label(text = '患者ID :', font = 20)
                l1.place(x=40, y=60)
                No = tk.Entry(show = None,textvariable = varNo,font = 21,width = 15)
                No.place(x=140,y=60)
                l2 = tk.Label(text='诊断 :', font = 20)
                l2.place(x=40, y=100)
                Dia = tk.Text(height = 5,font = 21,width=50)
                Dia.place(x=140, y=100)
                Hist = tk.Text(height = 15,width = 20,font = 21)
                Hist.place(x=820, y=60)
                Hist.insert('1.0','病史记录 :\n')
                def input():               #录入系统，诊断信息录入treat表
                    number = varNo.get()
                    dia = Dia.get('1.0','end')
                    print(number,dia)
                    now_time = datetime.datetime.now()             #记录入科时间
                    sql = 'insert into treat(p_num,d_num,diagnosis) values (%s,%s,%s)'    #医生进行诊断，开住院单
                    cur.execute(sql, (number, user,dia))
                    data = cur.fetchone()
                    print(data)
                    if data == None:
                        tk.messagebox.askquestion(title='提示', message='提交成功!')
                        print("Successfully Handeling!")
                    else:
                        tk.messagebox.askquestion(title='警告', message='提交失败!')
                        print("Something Went Wrong!!")

                def history():
                    number = varNo.get()
                    sql = 'select * from treat where p_num=%s'
                    cur.execute(sql,(number))
                    hist = cur.fetchall()
                    print(hist)
                    for item in hist:
                        d_num=item[1]
                        sql2 = 'select d_name,dept_name from doctor where d_num=%s'
                        cur.execute(sql2,(d_num))
                        data=cur.fetchone()
                        d_name=data[0]
                        dept_name=data[1]
                        dia=item[2]
                        result='主治医生：'+d_name+' 科室：'+dept_name+' 诊断：'+dia+'\n'
                        Hist.insert('end',result)


                def cancel():
                    l1.destroy()
                    No.destroy()
                    l2.destroy()
                    Dia.destroy()
                    b1.destroy()
                    b2.destroy()
                    b3.destroy()
                    Hist.destroy()

                b3 = tk.Button(text='搜索历史', font=10, command=history)
                b3.place(x=540, y=55)
                b1=tk.Button(text='提交诊断', font=10, command=input)
                b1.place(x=40, y=400)   #录入系统键
                b2=tk.Button(text='取消', font=10, command=cancel)
                b2.place(x=300, y=400)

            def items():
                sql = 'select i_name from items'
                cur.execute(sql)
                items = cur.fetchall()
                print(items)
                varNo = tk.StringVar()
                l1 = tk.Label(text='患者No. :', font=20)
                l1.place(x=40, y=60)
                No = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                No.place(x=240, y=60)
                t = tk.Text(height=7,font=20)
                t.insert('1.0','历史信息:\n')
                t.place(x=40,y=100)
                l2 = tk.Label(text='检查项目:', font=20)
                l2.place(x=40, y=300)
                itemList = ttk.Combobox(font=20,width=50)
                itemList.place(x=240,y=300)
                itemList['value'] = items

                def history():
                    pnum = varNo.get()
                    sql = 'select i_name,takeTime from takes where p_num=%s'
                    cur.execute(sql,(pnum))
                    hist = cur.fetchall()
                    if hist!=():
                        pass
                    else:
                        tk.messagebox.askquestion(title='警告', message='该患者不存在')
                        print("There was no patient of this number in the system!")
                    print(hist)
                    for items in hist:
                        t.insert('end',items)
                        t.insert('end','\n')


                def take():
                    pnum = varNo.get()
                    iname = itemList.get()
                    now_time = datetime.datetime.now()
                    print(pnum,iname,user)
                    sql = 'insert into takes (p_num,d_num,i_name,takeTime) values (%s,%s,%s,%s)'
                    cur.execute(sql,(pnum,user,iname,now_time))
                    result = cur.fetchone()
                    if result == None:
                        tk.messagebox.askquestion(title='提示', message='提交成功!')
                        print("Successfully Handeling!")
                    else:
                        tk.messagebox.askquestion(title='警告', message='提交失败!')
                        print("Something Went Wrong!!")

                def cancel():
                    l1.destroy()
                    l2.destroy()
                    b1.destroy()
                    b2.destroy()
                    b3.destroy()
                    itemList.destroy()
                    t.destroy()
                    No.destroy()


                b1 = tk.Button(text='搜索历史', font=10, command=history)
                b1.place(x=420, y=55)
                b2 = tk.Button(text='取消', font=10, command=cancel)
                b2.place(x=600, y=55)
                b3 = tk.Button(text='提交', font=10, command=take)
                b3.place(x=800, y=295  )  # 录入系统键
                # Dia = tk.Text(height=5, font=21)
                # Dia.place(x=240, y=100)

            def prescription():
                sql = 'select m_name from medicine'
                cur.execute(sql)
                medicines = cur.fetchall()
                print(medicines)
                varNo = tk.StringVar()
                l1 = tk.Label(text='患者ID :', font=20)
                l1.place(x=40, y=60)
                No = tk.Entry(show=None, textvariable=varNo, font=21, width=15)
                No.place(x=240, y=60)
                t = tk.Text(height=7, font=20)
                t.insert('1.0', 'History:\n')
                t.place(x=40, y=100)
                l2 = tk.Label(text='处方清单:', font=20)
                l2.place(x=40, y=300)
                medList = ttk.Combobox(font=20, width=50)
                medList.place(x=240, y=300)
                medList['value'] = medicines
                varQuantity = tk.IntVar()
                l3 = tk.Label(text='数量:', font=20)
                l3.place(x=40, y=340)
                q = tk.Entry(show=None, textvariable=varQuantity, font=21, width=15)
                q.place(x=240, y=340)

                def history():
                    pnum = varNo.get()
                    sql = 'select m_name,count,takeTime from prescription where p_num=%s'
                    cur.execute(sql, (pnum))
                    hist = cur.fetchall()
                    if hist != ():
                        pass
                    else:
                        tk.messagebox.askquestion(title='警告',
                                                  message='该患者不存在')
                        print("There was no patient of this number in the system!")
                    print(hist)
                    for items in hist:
                        t.insert('end', items)
                        t.insert('end', '\n')

                def take():
                    pnum = varNo.get()
                    mname = medList.get()
                    quantity = varQuantity.get()
                    now_time = datetime.datetime.now()
                    print(pnum, mname, quantity,user)
                    sql = 'insert into prescription (p_num,d_num,m_name,takeTime,count) values (%s,%s,%s,%s,%s)'
                    cur.execute(sql, (pnum, user, mname, now_time,quantity))
                    result = cur.fetchone()
                    if result == None:
                        tk.messagebox.askquestion(title='提示', message='提交成功!')
                        print("Successfully Handeling!")
                    else:
                        tk.messagebox.askquestion(title='警告', message='错误的用户名或密码\n                                    or\n您没有权限登陆该系统')

                def cancel():
                    l1.destroy()
                    l2.destroy()
                    l3.destroy()
                    b1.destroy()
                    b2.destroy()
                    b3.destroy()
                    medList.destroy()
                    t.destroy()
                    No.destroy()
                    q.destroy()

                b1 = tk.Button(text='搜索历史', font=10, command=history)
                b1.place(x=450, y=55)
                b2 = tk.Button(text='取消', font=10, command=cancel)
                b2.place(x=580, y=55)
                b3 = tk.Button(text='提交', font=10, command=take)
                b3.place(x=880, y=295)  # 录入系统键

            menubar = tk.Menu(mainwindow)
            Condition = tk.Menu(menubar,tearoff = 0)                           #病情菜单
            menubar.add_cascade(label = '选项',menu = Condition)
            Condition.add_command(label='诊断开立', command=diagnose)
            Condition.add_command(label='检查项目开立', command=items)
            Condition.add_command(label='处方项目开立', command=prescription)

            mainwindow.config(menu=menubar)
            mainwindow.mainloop()







tk.Button(text='登录',font = 10,command = login).place(x=30,y=120)
tk.Button(text='取消',font = 10,command = login).place(x=150,y=120)
window.mainloop()
