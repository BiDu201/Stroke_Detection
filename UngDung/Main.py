import gzip
import math
import pickle
import tkinter as tk
from tkinter import ttk
import sys

import numpy as np
import pandas as pd
import pyodbc
from tkinter import messagebox as msb

from sklearn.preprocessing import StandardScaler


def main():
    #textbox chỉ nhập số
    def validate_number_input(new_value):
        if not new_value:
            return True

        try:
            int(new_value)
            return True
        except ValueError:
            return False
    def validate_number_input_float(new_value):
        if not new_value:
            return True

        try:
            float(new_value)
            return True
        except ValueError:
            return False
    # Tạo giao diện
    root = tk.Tk()
    root.title("CHUẨN ĐOÁN ĐỘT QUỴ")
    root.geometry("1250x800")
    validate_cmd = root.register(validate_number_input)
    validate_float_cmd=root.register(validate_number_input_float)
    # Tạo groupbox
    # Groupbox bệnh nhân
    grb_bn = tk.LabelFrame(root, text="Bệnh nhân", padx=10, pady=10)
    grb_bn.place(x=50, y=50)

    # Groupbox chuẩn đoán
    grb_cd = tk.LabelFrame(root, text="Chuẩn đoán", padx=10, pady=10)
    grb_cd.place(x=600, y=150)

    # Groupbox thông tin bệnh nhân
    grb_ttbn = tk.LabelFrame(root, text="Thông tin bệnh nhân", padx=10, pady=10)
    grb_ttbn.place(x=50, y=200)

    # Groupbox hồ sơ bệnh án
    grb_ba = tk.LabelFrame(root, text="Hồ sơ bệnh án", padx=10, pady=10)
    grb_ba.place(x=50, y=500)

    # ------------------------------------Tạo các label và entry trong groupbox bệnh nhân-------------------------------
    lbbn = tk.Label(grb_bn, text="Mã Bệnh Nhân:")
    txtmabn = tk.Entry(grb_bn, validate='key', validatecommand=(validate_cmd, '%P'))
    txtmabn.focus()
    lbht = tk.Label(grb_bn, text="Họ Tên:")
    txthoten = tk.Entry(grb_bn)
    lbdchi = tk.Label(grb_bn, text="Địa Chỉ:")
    txtdchi = tk.Entry(grb_bn)
    lbdt = tk.Label(grb_bn, text="Điện Thoại:")
    txtdt = tk.Entry(grb_bn, validate='key', validatecommand=(validate_cmd, '%P'))
    lbbhyt = tk.Label(grb_bn, text="Số BHYT:")
    txtbhyt = tk.Entry(grb_bn, validate='key', validatecommand=(validate_cmd, '%P'))

    def reset_texts():
        txtmabn.delete(0, "end")
        txthoten.delete(0, "end")
        txtdchi.delete(0, "end")
        txtdt.delete(0, "end")
        txtbhyt.delete(0, "end")
        txtmabn.focus()

    # check thêm bnh
    def check_them_Bnh():
        if (
                str(txtmabn.get()).strip() == ""
                or str(txthoten.get()).strip() == ""
                or str(txtdchi.get()).strip() == ""
                or str(txtdt.get()).strip() == ""
                or str(txtbhyt.get()).strip() == ""
        ):
            msb.showinfo("Bệnh Nhân", "Vui lòng điền đầy đủ thông tin của bảng bệnh nhân")
        else:
            themBenhNhan()

    btnre = tk.Button(grb_bn, text="Làm mới", command=reset_texts)
    btnthembn = tk.Button(grb_bn, text="Thêm bệnh nhân", command=check_them_Bnh)

    # Định vị các label và entry trong groupbox
    lbbn.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    txtmabn.grid(row=0, column=1, padx=5, pady=5)
    lbht.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    txthoten.grid(row=0, column=3, padx=5, pady=5)
    lbdchi.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    txtdchi.grid(row=1, column=1, padx=5, pady=5)
    lbdt.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    txtdt.grid(row=1, column=3, padx=5, pady=5)
    lbbhyt.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    txtbhyt.grid(row=2, column=1, padx=5, pady=5)

    btnre.grid(row=2, column=2, padx=5, pady=5)
    btnthembn.grid(row=2, column=3, padx=5, pady=5)

    # -----------------------------Tạo các label, entry, combobox trong groupbox chuẩn đoán ----------------------------
    lbgt = tk.Label(grb_cd, text="Giới tính:")
    cbbgt = ttk.Combobox(grb_cd, state="readonly")
    lbtuoi = tk.Label(grb_cd, text="Tuổi:")
    txttuoi_var = tk.StringVar()
    txttuoi = tk.Entry(grb_cd, textvariable=txttuoi_var, validate='key', validatecommand=(validate_cmd, '%P'))
    lbkh = tk.Label(grb_cd, text="Kết hôn:")
    cbbkh = ttk.Combobox(grb_cd, state="readonly")
    lbcv = tk.Label(grb_cd, text="Công việc:")
    cbbcv = ttk.Combobox(grb_cd, state="readonly")
    lbct = tk.Label(grb_cd, text="Cư trú:")
    cbbct = ttk.Combobox(grb_cd, state="readonly")
    lbht = tk.Label(grb_cd, text="Hút thuốc:")
    cbbht = ttk.Combobox(grb_cd, state="readonly")
    lbtha = tk.Label(grb_cd, text="Tăng huyết áp:")
    cbbtha = ttk.Combobox(grb_cd, state="readonly")
    lbtim = tk.Label(grb_cd, text="Bệnh tim:")
    cbbtim = ttk.Combobox(grb_cd, state="readonly")
    lbglu = tk.Label(grb_cd, text="Mức glucose trung bình:")
    txtglu_var = tk.StringVar()
    txtglu = tk.Entry(grb_cd, textvariable=txtglu_var, validate='key', validatecommand=(validate_float_cmd, '%P'))
    lbbmi = tk.Label(grb_cd, text="BMI:")
    txtbmi_var = tk.StringVar()
    txtbmi = tk.Entry(grb_cd, textvariable=txtbmi_var, validate='key', validatecommand=(validate_float_cmd, '%P'))
    txtkq_var = tk.StringVar(value="None")
    txtkq = tk.Entry(root, width=94, state="readonly", textvariable=txtkq_var, justify='center')

    value_gt = {"Male": 1, "Female": 0}
    value_kh = {"Yes": 1, "No": 0}
    value_ct = {"Urban": 1, "Rural": 0}
    value_tha = {"Yes": 1, "No": 0}
    value_tim = {"Yes": 1, "No": 0}

    def select_cbb():
        select_gt = cbbgt.get()
        select_kh = cbbkh.get()
        select_ctru = cbbct.get()
        select_tha = cbbtha.get()
        select_bt = cbbtim.get()

        gt = value_gt[select_gt]
        kh = value_kh[select_kh]
        ct = value_ct[select_ctru]
        tha = value_tha[select_tha]
        bt = value_tim[select_bt]
        return gt, kh, ct, tha, bt

    def chuandoan():
        glu = math.log(float(txtglu.get()))
        bmi = math.log(float(txtbmi.get()))

        sca_data = pd.read_csv('.\\standardScaler.csv')
        new_data = {'age': float(txttuoi.get()), 'avg_glucose_level': glu, 'bmi': bmi}

        sca_data = sca_data.append(new_data, ignore_index=True)

        s = StandardScaler()
        sca_data = s.fit_transform(sca_data)

        # # Chuẩn hóa (x - mean)/std
        # glu_s = round((glu - 4.59122703) / 0.36121063,6)
        # bmi_s = round((bmi - 3.33059652) / 0.26244426,6)
        # age_s = round((float(txttuoi.get()) - 43.18379937) / 22.61187988, 6)

        age_s, glu_s, bmi_s = sca_data[-1]
        gt, kh, ct, tha, bt = select_cbb()

        with gzip.open('.\\Model\\svm_stroke_model.pkl.gz', 'rb') as f:
            SVM = pickle.load(f)
        select_cbbcv = cbbcv.get()
        select_cbbht = cbbht.get()
        arr = np.array([[age_s, glu_s, bmi_s, gt, tha, bt, kh, 0, 0, 0, 0, ct, 0, 0, 0]])

        if select_cbbcv == 'Never_worked':
            arr[0, 7] = 1
        elif select_cbbcv == 'Private':
            arr[0, 8] = 1
        elif select_cbbcv == 'Self-employed':
            arr[0, 9] = 1
        elif select_cbbcv == 'children':
            arr[0, 10] = 1

        if select_cbbht == 'formerly smoked':
            arr[0, 12] = 1
        elif select_cbbht == 'never smoked':
            arr[0, 13] = 1
        elif select_cbbht == 'smokes':
            arr[0, 14] = 1

        pre = SVM.predict(arr)

        if pre == 0:
            kq = "Không bệnh"
        else:
            kq = "Có bệnh"

        txtkq_var.set(kq)

    btnchuandoan = tk.Button(grb_cd, text="Chuẩn đoán", command=chuandoan)

    # kiểm tra thông tin thêm bệnh án
    def check_them_benh_an():
        if str(cbbgt.get()).strip() == "" or str(txttuoi.get()).strip() == "" or str(cbbtha.get()).strip() == "" or str(
                cbbtim.get()).strip() == "" or str(cbbkh.get()).strip() == "" or str(cbbcv.get()).strip() == "" or str(
            cbbct.get()).strip() == "" or str(txtglu.get()).strip() == "" or str(txtbmi.get()).strip() == "" or str(
             cbbht.get()).strip() == "":
            msb.showinfo("Bệnh án", "Vui lòng nhập đầy đủ thông tin bệnh án")
        else:
            them_benh_an()
            reset_text()
            btncsdl.config(state="disabled")

    # thêm bệnh án
    def them_benh_an():
        select_item = trv_bn.focus()
        values = trv_bn.item(select_item, "values")
        mabnh = values[0]
        query = "insert into benhan(MABN,GENDER,AGE,HYPERTENSION,HEART_DISEASE,EVER_MARRIED,WORK_TYPE,RESIDENCE_TYPE,AVG_GLUCOSE_LEVEL,BMI,SMOKING_STATUS,STROKE) values(?,?,?,?,?,?,?,?,?,?,?,?)"
        value = (mabnh, str(cbbgt.get()).strip(), str(txttuoi.get()).strip(), str(cbbtha.get()).strip(),
                 str(cbbtim.get()).strip(), str(cbbkh.get()).strip(), str(cbbcv.get()).strip(),
                 str(cbbct.get()).strip(), str(txtglu.get()).strip(), str(txtbmi.get()).strip(),
                 str(cbbht.get()).strip(), str(txtkq.get()).strip())
        cursor.execute(query, value)
        con.commit()
        msb.showinfo("Bệnh án", "Thêm bệnh án thành công")
        trv_ba.delete(*trv_ba.get_children())
        data_benh_an()

    btncsdl = tk.Button(grb_cd, text="Lưu vào CSDL", command=check_them_benh_an)
    btncsdl.config(state="disabled")

    def reset_text():
        cbbgt.set("")
        txttuoi.delete(0, "end")
        cbbkh.set("")
        cbbcv.set("")
        cbbct.set("")
        cbbht.set("")
        cbbtha.set("")
        cbbtim.set("")
        txtglu.delete(0, "end")
        txtbmi.delete(0, "end")
        txtkq.delete(0, "end")
        txtkq_var.set("None")
        btncsdl.config(state="disabled")
        btnupdate.config(state="disabled")

    # lấy bệnh án theo mã bệnh án
    def data_benh_an():
        trv_ba.delete(*trv_ba.get_children())
        select_item = trv_bn.focus()
        values = trv_bn.item(select_item, "values")
        mabnh = values[0]
        cursor.execute("Select MABA,NGAYKHAM,GENDER,AGE,HYPERTENSION,HEART_DISEASE,EVER_MARRIED,WORK_TYPE,"
                       "RESIDENCE_TYPE,AVG_GLUCOSE_LEVEL,BMI FLOAT,SMOKING_STATUS,STROKE FROM BENHAN where mabn=" +
                       mabnh + "")
        for inx, r in enumerate(cursor.fetchall(), start=1):
            row_list1 = list(r)
            trv_ba.insert("", "end", text=str(inx), values=row_list1)

    # Load dữ liệu treeview bệnh án
    def load_ban():
        trv_ba.delete(*trv_ba.get_children())

        cursor.execute(
            "Select MABA,NGAYKHAM,GENDER,AGE,HYPERTENSION,HEART_DISEASE,EVER_MARRIED,WORK_TYPE,RESIDENCE_TYPE,AVG_GLUCOSE_LEVEL,BMI FLOAT,SMOKING_STATUS,STROKE FROM BENHAN"
        )
        for inx, r in enumerate(cursor.fetchall(), start=1):
            row_list1 = list(r)
            trv_ba.insert("", "end", text=str(inx), values=row_list1)

    # cập nhật bệnh án
    def update_ba():
        select_item = trv_ba.focus()
        values = trv_ba.item(select_item, "values")
        maba = values[0]
        if (
                str(txttuoi.get()).strip() == ""
                or str(txtglu.get()).strip() == ""
                or str(txtbmi.get()).strip() == ""
        ):
            msb.showinfo("Bệnh Nhân", "vui lòng điền đầy đủ thông tin bệnh án")
        else:
            try:
                query = "update benhan set gender=?,age=?,HYPERTENSION=?,HEART_DISEASE=?,EVER_MARRIED=?,WORK_TYPE=?,RESIDENCE_TYPE=?,AVG_GLUCOSE_LEVEL=?,BMI=?,SMOKING_STATUS=?, STROKE=? where maba=?"
                value = (
                    str(cbbgt.get()).strip(), str(txttuoi.get()).strip(), str(cbbtha.get()).strip(),
                    str(cbbtim.get()).strip(),
                    str(cbbkh.get()).strip(), str(cbbcv.get()).strip(), str(cbbct.get()).strip(), str(txtglu.get()).strip(),
                    str(txtbmi.get()).strip(), str(cbbht.get()).strip(), str(txtkq.get()).strip(),maba)
                cursor.execute(query, value)
                con.commit()
                msb.showinfo("bệnh án", "Cập nhật bệnh án thành công")
                data_benh_an()
            except:
                load_ban()
            btnupdate.config(state="disabled")


    btnreset = tk.Button(grb_cd, text="Làm mới", command=reset_text)
    btnupdate = tk.Button(grb_cd, text="Cập nhật", command=update_ba)
    btnupdate.config(state="disabled")

    # Thêm giá trị cho combobox
    cbbgt["values"] = ("Male", "Female")
    cbbkh["values"] = ("Yes", "No")
    cbbcv["values"] = (
        "Private",
        "Self-employed",
        "Govt_job",
        "children",
        "Never_worked",
    )
    cbbct["values"] = ("Urban", "Rural")
    cbbht["values"] = ("never smoked", "formerly smoked", "smokes", "Unknow")
    cbbtha["values"] = ("Yes", "No")
    cbbtim["values"] = ("Yes", "No")

    lbgt.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    cbbgt.grid(row=0, column=1, padx=5, pady=5)
    lbtuoi.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
    txttuoi.grid(row=0, column=3, padx=5, pady=5)
    lbkh.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
    cbbkh.grid(row=1, column=1, padx=5, pady=5)
    lbcv.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    cbbcv.grid(row=1, column=3, padx=5, pady=5)
    lbct.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    cbbct.grid(row=2, column=1, padx=5, pady=5)
    lbht.grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
    cbbht.grid(row=2, column=3, padx=5, pady=5)
    lbtha.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    cbbtha.grid(row=3, column=1, padx=5, pady=5)
    lbtim.grid(row=3, column=2, padx=5, pady=5, sticky=tk.W)
    cbbtim.grid(row=3, column=3, padx=5, pady=5)
    lbglu.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
    txtglu.grid(row=4, column=1, padx=5, pady=5)
    lbbmi.grid(row=4, column=2, padx=5, pady=5, sticky=tk.W)
    txtbmi.grid(row=4, column=3, padx=5, pady=5)
    txtkq.place(x=600, y=400)

    btnchuandoan.grid(row=6, column=0, padx=5, pady=5)
    btncsdl.grid(row=6, column=2, padx=5, pady=5)
    btnreset.grid(row=6, column=3, padx=1, pady=5)
    btnupdate.grid(row=6, column=1, padx=1, pady=5)
    # ----------------------------------------------Treeview bệnh nhân-------------------------------------------------
    trv_bn = ttk.Treeview(grb_ttbn)

    # Tạo scrollbar cuộn dọc
    scr_doc = ttk.Scrollbar(grb_ttbn, orient="vertical", command=trv_bn.yview)
    trv_bn.configure(yscrollcommand=scr_doc.set)
    scr_doc.pack(side="right", fill="y")

    # Tạo scrollbar cuộn ngang
    scr_ngang = ttk.Scrollbar(grb_ttbn, orient="horizontal", command=trv_bn.xview)
    trv_bn.configure(xscrollcommand=scr_ngang.set)
    scr_ngang.pack(side="bottom", fill="x")

    trv_bn.pack()

    # Thêm cột vào Treeview bên trái
    trv_bn["columns"] = ("col1", "col2", "col3", "col4", "col5")
    trv_bn.column("#0", width=50, minwidth=50)
    trv_bn.column("col1", width=60, minwidth=80)
    trv_bn.column("col2", width=80, minwidth=80)
    trv_bn.column("col3", width=80, minwidth=80)
    trv_bn.column("col4", width=80, minwidth=80)
    trv_bn.column("col5", width=80, minwidth=80)
    trv_bn.heading("#0", text="STT")
    trv_bn.heading("col1", text="Mã BN")
    trv_bn.heading("col2", text="Họ Tên")
    trv_bn.heading("col3", text="Địa Chỉ")
    trv_bn.heading("col4", text="Điện thoại")
    trv_bn.heading("col5", text="BHYT")

    # -----------------------------------------------Treeview bệnh án--------------------------------------------------
    trv_ba = ttk.Treeview(grb_ba)

    # Tạo scrollbar cuộn dọc
    scr_doc1 = ttk.Scrollbar(grb_ba, orient="vertical", command=trv_ba.yview)
    trv_ba.configure(yscrollcommand=scr_doc1.set)
    scr_doc1.pack(side="right", fill="y")

    # Tạo scrollbar cuộn ngang
    scr_ngang1 = ttk.Scrollbar(grb_ba, orient="horizontal", command=trv_ba.xview)
    trv_ba.configure(xscrollcommand=scr_ngang1.set)
    scr_ngang1.pack(side="bottom", fill="x")

    btnloadba_all = tk.Button(grb_ba, text="Load tất cả", command=load_ban)
    btnloadba_all.pack(padx=5, pady=5)

    trv_ba.pack()

    # Thêm cột vào Treeview bên phải
    trv_ba["columns"] = (
        "col1",
        "col2",
        "col3",
        "col4",
        "col5",
        "col6",
        "col7",
        "col8",
        "col9",
        "col10",
        "col11",
        "col12",
        "col13",
    )
    trv_ba.column("#0", width=50, minwidth=50)
    trv_ba.column("col1", width=80, minwidth=80)
    trv_ba.column("col2", width=80, minwidth=80)
    trv_ba.column("col3", width=80, minwidth=80)
    trv_ba.column("col4", width=80, minwidth=80)
    trv_ba.column("col5", width=80, minwidth=80)
    trv_ba.column("col6", width=80, minwidth=80)
    trv_ba.column("col7", width=80, minwidth=80)
    trv_ba.column("col8", width=85, minwidth=80)
    trv_ba.column("col9", width=80, minwidth=80)
    trv_ba.column("col10", width=80, minwidth=80)
    trv_ba.column("col11", width=80, minwidth=80)
    trv_ba.column("col12", width=85, minwidth=80)
    trv_ba.column("col13", width=80, minwidth=80)
    trv_ba.heading("#0", text="STT")
    trv_ba.heading("col1", text="Mã BA")
    trv_ba.heading("col2", text="Ngày Khám")
    trv_ba.heading("col3", text="Giới tính")
    trv_ba.heading("col4", text="Tuổi")
    trv_ba.heading("col5", text="Tăng Huyết Áp")
    trv_ba.heading("col6", text="Bệnh Tim")
    trv_ba.heading("col7", text="Kết Hôn")
    trv_ba.heading("col8", text="Công Việc")
    trv_ba.heading("col9", text="Cư Trú")
    trv_ba.heading("col10", text="Mức Glucose Trung Bình")
    trv_ba.heading("col11", text="BMI")
    trv_ba.heading("col12", text="Hút Thuốc")
    trv_ba.heading("col13", text="Đột Quỵ")

    # Kết nối đến csdl
    con = pyodbc.connect(sys.argv[1])
    cursor = con.cursor()

    # Sự kiện khi chọn vào dòng trên treeview bệnh án
    def select_trvba(event):
        select_item = trv_ba.focus()
        values = trv_ba.item(select_item, "values")

        cbbgt.set(values[2])
        txttuoi_var.set(values[3])
        cbbkh.set(values[6])
        cbbcv.set(values[7])
        cbbct.set(values[8])
        cbbht.set(values[11])
        cbbtha.set(values[4])
        cbbtim.set(values[5])
        txtglu_var.set(values[9])
        txtbmi_var.set(values[10])
        txtkq_var.set(values[12])
        btnupdate.config(state="active")

    trv_ba.bind("<<TreeviewSelect>>", select_trvba)

    # kiểm tra mã bệnh nhân
    def check_MaBNh(n):
        cursor.execute("select * from benhnhan where mabn=" + n + "")
        rows = cursor.fetchall()
        if len(rows) > 0:
            msb.showinfo("thêm bệnh nhân", "Mã bệnh nhân đã tồn tại")
            txtmabn.focus()
            return False
        else:
            return True

    # thêm bệnh nhân
    def themBenhNhan():
        if check_MaBNh(str(txtmabn.get()).strip()):
            query = "insert into benhnhan values(?,?,?,?,?)"
            value = (
                str(txtmabn.get()).strip(),
                str(txthoten.get()).strip(),
                str(txtdchi.get()).strip(),
                str(txtdt.get()).strip(),
                str(txtbhyt.get()).strip(),
            )
            cursor.execute(query, value)
            con.commit()
            msb.showinfo("thêm bệnh nhân", "thêm bệnh nhân thành công")
            trv_bn.delete(*trv_bn.get_children())
            loadTableBenhNhan()
            reset_texts()

    # Load dữ liệu treeview bệnh nhân
    def loadTableBenhNhan():
        cursor.execute("Select * from BENHNHAN")
        for index, row in enumerate(cursor.fetchall(), start=1):
            row_list = list(row)
            trv_bn.insert("", "end", text=str(index), values=row_list)

    # sự kiện click vào treeview bệnh nhân sẽ load lại treeview bệnh án
    def select_bnh(event):
        data_benh_an()
        # print(len(trv_ba.get_children()))
        if len(trv_ba.get_children()) == 0:
            btncsdl.config(state="active")
            btnupdate.config(state="disabled")
        else:
            btncsdl.config(state="active")
            btnupdate.config(state="active")

    trv_bn.bind("<<TreeviewSelect>>", select_bnh)

    loadTableBenhNhan()
    load_ban()
    # Chạy ứng dụng
    root.mainloop()
