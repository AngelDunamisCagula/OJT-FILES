from tkcalendar import Calendar, DateEntry
from datetime import datetime
from tkcalendar import Calendar
import time
import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import *
import tkinter as dlms
from tkinter import ttk
import tkinter.messagebox
from tkinter import RIDGE
import sqlite3
from tkinter import *
import hashlib

# ________APPDATABASE________#


class AppDatabase(dlms.Tk):
    def __init__(self):
        dlms.Tk.__init__(self)
        self.config(bg="Gray")
        Table = dlms.Frame(self)
        Table.pack(side="top", fill="both", expand=True)
        Table.rowconfigure(0, weight=1)
        Table.columnconfigure(0, weight=1)
        self.frames = {}
        self.current_user = None 

        for i in (Home, Dormer, Logbook, Guardian, Destination, Companion, Registration, Login):
            frame = i(Table, self)
            self.frames[i] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_user_table()
        self.ShowFrame(Login) 

    def update_staff_button_state(self, state):
        home_frame = self.frames[Home]
        if home_frame.staff_button:
            if self.current_user == "Admin":  # Check if the current user is an Admin user
                # Enable the button for the Admin user
                home_frame.staff_button.configure(state="normal")
            else:
                home_frame.staff_button.configure(state="disabled")

    def ShowFrame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()

    def create_user_table(self):
        conn = sqlite3.connect("logd.db")
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS user(User_Name TEXT PRIMARY KEY,Role TEXT,Password TEXT,Email TEXT)""")
        admin_password = hashlib.sha256("admin_password".encode()).hexdigest()
        cur.execute(
            "INSERT OR IGNORE INTO user(User_Name,Role, Password, Email) VALUES (?, ?, ?, ?)",
            ("admin_username", "Admin", admin_password, "admin@example.com"))
        conn.commit()
        conn.close()

    # ________Login________#


class Login(dlms.Frame):
    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("ST. THERESE OF LISIEUX DORMLOG MONITOR SYSTEM")

        label = dlms.Label(self, text="Login", font=("Bodoni MT", 60, "bold"))
        label.pack(pady=50)

        self.username_label = dlms.Label(
            self, text="Username", font=("Palatino roman", 20))
        self.username_label.pack(pady=10)

        self.username_entry = dlms.Entry(self, font=("Palatino roman", 20))
        self.username_entry.pack(pady=10)

        self.password_label = dlms.Label(
            self, text="Password", font=("Palatino roman", 20))
        self.password_label.pack(pady=10)

        self.password_entry = dlms.Entry(
            self, show="*", font=("Palatino roman", 20))
        self.password_entry.pack(pady=10)

        login_button = dlms.Button(
            self, text="Login", command=self.login, font=("Palatino roman", 20))
        login_button.pack(pady=20)

        register_button = dlms.Button(self, text="Register", command=lambda: controller.ShowFrame(
            Registration), font=("Palatino roman", 10))
        register_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conn = sqlite3.connect("logd.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE User_Name = ?", (username,))
        result = cur.fetchone()
        conn.close()

        if result:
            # Assuming password is stored in the 3rd column
            stored_password = result[2]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if hashed_password == stored_password:
                # Assign the Role value to current_user
                self.controller.current_user = result[1]

                if self.controller.current_user == "Staff":
                    self.controller.update_staff_button_state("disabled")
                elif self.controller.current_user == "Admin":
                    # Enable the Dormer button for Admin user
                    self.controller.update_staff_button_state("normal")

                self.controller.ShowFrame(Home)

                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            else:
                tkinter.messagebox.showerror("Login Error", "Invalid password")
        else:
            tkinter.messagebox.showerror("Login Error", "User not found")


# ________Registration________#

class Registration(dlms.Frame):
    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Registration")

        label = dlms.Label(self, text="Registration",
                           font=("Bodoni MT", 60, "bold"))
        label.pack(pady=50)

        self.username_label = dlms.Label(
            self, text="Username", font=("Palatino roman", 20))
        self.username_label.pack(pady=10)

        self.username_entry = dlms.Entry(self, font=("Palatino roman", 20))
        self.username_entry.pack(pady=10)

        self.password_label = dlms.Label(
            self, text="Password", font=("Palatino roman", 20))
        self.password_label.pack(pady=10)

        self.password_entry = dlms.Entry(
            self, show="*", font=("Palatino roman", 20))
        self.password_entry.pack(pady=10)

        self.email_label = dlms.Label(
            self, text="Email", font=("Palatino roman", 20))
        self.email_label.pack(pady=10)

        self.email_entry = dlms.Entry(self, font=("Palatino roman", 20))
        self.email_entry.pack(pady=10)

        self.role_label = dlms.Label(
            self, text="Role", font=("Palatino roman", 20))
        self.role_label.pack(pady=10)

        self.role_entry = dlms.Entry(self, font=("Palatino roman", 20))
        self.role_entry.pack(pady=10)

        register_button = dlms.Button(
            self, text="Register", command=self.register, font=("Palatino roman", 15))
        register_button.pack(pady=10)

        back_button = dlms.Button(self, text="Back", command=lambda: self.go_back(
            self.controller), font=("Palatino roman", 10))
        back_button.pack(pady=20)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()
        email = self.email_entry.get()  # Add this line

        if role != "Staff":
            tkinter.messagebox.showerror(
                "Registration Error", "Only staff user can register")
            return

        conn = sqlite3.connect("logd.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE User_Name = ?", (username,))
        result = cur.fetchone()

        if result:
            tkinter.messagebox.showerror(
                "Registration Error", "Username already exists")
        else:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cur.execute("INSERT INTO user (User_Name, Role, Password, Email) VALUES (?, ?, ?, ?)",
                        (username, role, hashed_password, email))
            conn.commit()
            tkinter.messagebox.showinfo(
                "Registration", "Registration successful!")
            self.controller.ShowFrame(Login)

        conn.close()

    def go_back(self, controller):
        controller.ShowFrame(Login)


# ________Home________#

class Home(dlms.Frame):
    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller

        Top = Frame(self, bg="#809bce",relief='groove', bd=15, height=1)
        Top.pack(side='top',  fill='x')
        label = dlms.Label(Top, text="S T.   T H E R E S E   O F   L I S I E U X",
                           font=("Bodoni MT", 35, "bold"),fg="#ffffff", height=2)
        label.config(bg=label.master.cget('background'))
        label.pack(side='top', fill='x')
        Top1 = Frame(self, bg="#809bce",relief='groove', bd=1, height=1)
        Top1.pack(side='top',  fill='x')
        label1 = dlms.Label(Top1, text="D O R M L O G    M O N I T O R    S Y S T E M", bd=2,
                           font=("Bodoni MT", 15),fg="#ffffff", height=1)
        label1.config(bg=label1.master.cget('background'))
        label1.pack(side='top', fill='x')

        Center = Frame(self, bg="#f9f6f2", relief='groove', bd=1) 
        Center.pack(side='top', fill='both', expand=True)

        Bottom = Frame(self, bg="#809bce",height=1, relief='groove', bd=2)
        Bottom.pack(side='top', fill='x')

        # Create the Dormer button
        self.staff_button = dlms.Button(Center, text="Dormer", font=("Palatino roman", 25, "bold"), bd=10, width=10,
                                        bg="#fefeff", fg="#809bce", state="disabled",
                                        command=lambda: controller.ShowFrame(Dormer)) 
        self.staff_button.place(relx=0.5, rely=0.4, anchor='center')

        Button3 = dlms.Button(Center, text="Logbook", font=("Palatino roman", 25, "bold"), bd=10, width=10,
                              bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Logbook))
        Button3.place(relx=0.5, rely=0.6, anchor='center')

        logout_button = dlms.Button(Bottom, text="Logout", font=("Palatino roman", 10, "bold"), bd=10, width=10,
                                    bg="#fefeff", fg="#809bce", command=self.logout)  
        logout_button.pack(side='left')

    def logout(self):
        self.controller.current_user = None
        self.controller.update_staff_button_state("disabled")
        self.controller.ShowFrame(Login)


# ________Dormer FUNCTIONS________#

class Dormer(dlms.Frame):

    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller

        Top = Frame(self, bg="#809bce", relief='groove', bd=3, height=1)
        Top.pack(side='top', fill='both')

        label = dlms.Label(Top, text="D O R M E R    I N F O R M A T I ON", bd=4, font=("Times new roman", 30, "bold"), fg="#ffffff")
        label.config(bg=label.master.cget('background'))
        label.pack(side='top', fill='x')

        Center = Frame(self, bg="#f9f6f2", relief='groove', bd=1) 
        Center.pack(side='top', fill='both', expand=True)
        table = Frame(Center, relief='groove', bd=1)
        table.pack(side='left',fill='both', expand=True)
        table.config(bg=table.master.cget('background'))
        label = Frame(Center, relief='groove', bd=1)
        label.config(bg=label.master.cget('background'))
        label.pack(side='left',fill='y', expand = True)

        Bottom = Frame(self, bg="#809bce",height=1, relief='groove', bd=3)
        Bottom.pack(side='top', fill='x')

        DormerID = StringVar()
        Dormer_Name = StringVar()
        RoomNum = StringVar()
        Dormer_ContactNum = StringVar()
        SearchBar_Var = StringVar()

        def connectDormer():
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS dormer(DormerID TEXT PRIMARY KEY, Dormer_Name TEXT, RoomNum TEXT, Dormer_ContactNum TEXT)")
            conn.commit()
            conn.close()

        def addDormer():
            conn = sqlite3.connect("logd.db")
            c = conn.cursor()
            c.execute("INSERT INTO dormer(DormerID, Dormer_Name, RoomNum, Dormer_ContactNum) VALUES (?,?,?,?)",
                      (DormerID.get(), Dormer_Name.get(), RoomNum.get(), Dormer_ContactNum.get()))
            conn.commit()
            conn.close()
            DormerID.set('')
            Dormer_Name.set('')
            RoomNum.set('')
            Dormer_ContactNum.set('')
            tkinter.messagebox.showinfo("Dormer", "Successfully added!")
            displayDormer()

        def displayDormer():
            self.Dormerlist.delete(*self.Dormerlist.get_children())
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM dormer")
            rows = cur.fetchall()
            for row in rows:
                self.Dormerlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            conn.close()

        def updateDormer():
            for selected in self.Dormerlist.selection():
                conn = sqlite3.connect("logd.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE dormer SET DormerID=?, Dormer_Name=?, RoomNum=?, Dormer_ContactNum=? WHERE DormerID=?",
                            (DormerID.get(), Dormer_Name.get(), RoomNum.get(), Dormer_ContactNum.get(), self.Dormerlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo("Dormer", "Successfully updated!")
                displayDormer()
                clear()
                conn.close()

        def editDormer():
            x = self.Dormerlist.focus()
            if x == "":
                tkinter.messagebox.showerror(
                    "Dormer", "Please select a record.")
                return
            values = self.Dormerlist.item(x, "values")
            DormerID.set(values[0])
            Dormer_Name.set(values[1])
            RoomNum.set(values[2])
            Dormer_ContactNum.set(values[3])

        def deleteDormer():
            try:
                messageDelete = tkinter.messagebox.askyesno(
                    " DORMLOG MONITOR SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:
                    con = sqlite3.connect("logd.db")
                    cur = con.cursor()
                    x = self.Dormerlist.selection()[0]
                    DormerID = self.Dormerlist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute(
                        "DELETE FROM dormer WHERE DormerID = ?", (DormerID,))
                    con.commit()
                    self.Dormerlist.delete(x)
                    tkinter.messagebox.askyesno(
                        "Dormer", "Successfully deleted!")
                    displayDormer()
                    con.close()
            except:
                tkinter.messagebox.showerror(
                    "Dormer", "already exist in the record")

        def searchDormer():
            DormerID = SearchBar_Var.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM dormer WHERE DormerID = ?", (DormerID,))
            con.commit()
            self.Dormerlist.delete(*self.Dormerlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.Dormerlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def Refresh():
            displayDormer()

        def clear():

            DormerID.set('')
            Dormer_Name.set('')
            RoomNum.set('')
            Dormer_ContactNum.set('')

        def OnDoubleclick(event):
            item = self.Dormerlist.selection()[0]
            values = self.Dormerlist.item(item, "values")
            DormerID.set(values[0])
            Dormer_Name.set(values[1])
            RoomNum.set(values[2])
            Dormer_ContactNum.set(values[3])

# ________WINDOW BUTTONS________#

        Button1 = dlms.Button(Bottom, text="Home", font=("Palatino roman", 20, "bold"), bd=7,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Home))
        Button1.pack(side='left')
        Button2 = dlms.Button(Bottom, text="Guardian", font=("Palatino roman", 20, "bold"), bd=7,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Guardian))
        Button2.pack(side='right')


# ________LABELS AND ENTRIES________#
        InfoFrame = Frame(label, bd=4, relief=GROOVE)
        InfoFrame.pack(side='top', fill='both', expand=True)
        InfoFrame.config(bg=InfoFrame.master.cget('background'))

        self.lblDormerID = Label(InfoFrame, font=("Time new roman", 18, "bold"),
                                 text="Dormer ID:", padx=5, pady=5,fg="#579ABE")
        self.lblDormerID.config(bg=self.lblDormerID.master.cget('background'))
        self.lblDormerID.place(relx=0.5, rely=0.1, anchor='center')
        self.txtDormerID = Entry(InfoFrame, font=("Time new roman", 28), textvariable=DormerID, width=15,fg="black", bg="#fefeff")
        self.txtDormerID.place(relx=0.5, rely=0.2, anchor='center')

        self.lblDormerName = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Dormer Name:", padx=5, pady=5,fg="#579ABE")
        self.lblDormerName.config(bg=self.lblDormerName.master.cget('background'))
        self.lblDormerName.place(relx=0.5, rely=0.3, anchor='center')
        self.txtDormerName = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Dormer_Name, width=15,fg="black", bg="#fefeff")
        self.txtDormerName.place(relx=0.5, rely=0.4, anchor='center')

        self.lblRoomNum = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Room Num:", padx=5, pady=5, fg="#579ABE")
        self.lblRoomNum.config(bg=self.lblRoomNum.master.cget('background'))
        self.lblRoomNum.place(relx=0.5, rely=0.5, anchor='center')
        self.txtRoomNum = Entry(InfoFrame, font=( "Time new roman", 28), textvariable=RoomNum, width=15, fg="black", bg="#fefeff")
        self.txtRoomNum.place(relx=0.5, rely=0.6, anchor='center')

        self.lblDormerContactNum = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Dormer ContactNum:", padx=5, pady=5,fg="#579ABE")
        self.lblDormerContactNum.config(bg=self.lblDormerContactNum.master.cget('background'))
        self.lblDormerContactNum.place(relx=0.5, rely=0.7, anchor='center')
        self.txtDormerContactNum = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Dormer_ContactNum, width=15, fg="black",  bg="#fefeff")
        self.txtDormerContactNum.place(relx=0.5, rely=0.8, anchor='center')
     
        Info = Frame(table, bd=1, bg="#FFFEFC", relief=GROOVE, height=60)
        Info.pack(side='top', fill='x')
        
        self.SearchBarlbl = Label(Info, font=("Time new roman", 12, "bold"),
                                  text="DormerID:", padx=5, pady=5,fg="#809bce")
        self.SearchBarlbl.config(bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='left', anchor='w')
        self.SearchBar = Entry(Info, font=("Time new roman", 14), textvariable=SearchBar_Var, width=50, fg="#809bce", bg="#fefeff")
        self.SearchBar.pack(side='left', anchor='e', expand=True)
        self.btnSearch = Button(Info, text="SEARCH", font=("Palatino roman", 14, "bold"), bg="#fefeff", fg="#809bce", command=searchDormer)
        self.btnSearch.pack(side='left')
        self.btnRefresh = Button(Info, text="Refresh", font=('Palatino roman', 14, "bold"), height=1, width=10, bg="#fefeff", fg="#809bce", command=Refresh)
        self.btnRefresh.pack(side='left')


# ________TREEVIEW________#

        scrollbar = Scrollbar(table, orient=VERTICAL)

        self.Dormerlist = ttk.Treeview(table, columns=(
            "DormerID", "Dormer_Name", "RoomNum", "Dormer_ContactNum"), height=20,  yscrollcommand=scrollbar.set)
        self.Dormerlist.heading("DormerID", text="DormerID")
        self.Dormerlist.heading("Dormer_Name", text="Name")
        self.Dormerlist.heading("RoomNum", text="RoomNum")
        self.Dormerlist.heading("Dormer_ContactNum", text="ContactNum")
        self.Dormerlist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(
            "Source code", 18, "bold"), foreground="Black")
        style.configure("Treeview", font=("Source code", 15))
        style.map('Treeview', background=[
                  ('selected', 'grey')], foreground=[('selected', 'Black')])
        self.Dormerlist.column("DormerID", width=50)
        self.Dormerlist.column("Dormer_Name", width=200)
        self.Dormerlist.column("RoomNum", width=50)
        self.Dormerlist.column("Dormer_ContactNum", width=200)
        self.Dormerlist.bind("<Double-1> ", OnDoubleclick)
        self.Dormerlist.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.Dormerlist.yview)

# ________Dormer BUTTONS________#

        ButtonFrame = Frame(label, bd=4, bg="#fefeff", relief=GROOVE)
        ButtonFrame.pack(side='bottom', fill='both')

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=addDormer)
        self.btnAddID.pack(side='left')
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=updateDormer)
        self.btnUpdate.pack(side='left')
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=clear)
        self.btnClear.pack(side='left')
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=deleteDormer)
        self.btnDelete.pack(side='left')

        connectDormer()
        displayDormer()


# ________Guardian FUNCTIONS________#

class Guardian(dlms.Frame):

    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller

        Top = Frame(self, bg="#809bce", height=1, relief='groove', bd=3)
        Top.pack(side='top', fill='x')

        label = dlms.Label(Top, text="DORMER'S GUARDIAN INFORMATION", bd=4, font=("Times new roman", 30, "bold"), fg="#ffffff")
        label.config(bg=label.master.cget('background'))
        label.pack(side='top', fill='x')

        Center = Frame(self, bg="#f9f6f2", relief='groove', bd=1)  # Increase the height to accommodate the larger treeview
        Center.pack(side='top', fill='both', expand=True)
        table = Frame(Center, relief='groove', bd=1)
        table.pack(side='left',fill='both', expand=True)
        table.config(bg=table.master.cget('background'))
        label = Frame(Center, relief='groove', bd=1)
        label.config(bg=label.master.cget('background'))
        label.pack(side='left',fill='y', expand = True)

        Bottom = Frame(self, bg="#809bce",height=1, relief='groove', bd=3)
        Bottom.pack(side='top', fill='x')

        Guardian_Name = StringVar()
        Guardian_ContactNum = StringVar()
        DdormerID = StringVar()
        SearchBar_Var = StringVar()

        def connectGuardian():
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS guardian(Guardian_Name TEXT,Guardian_ContactNum TEXT,DdormerID TEXT, FOREIGN KEY (DdormerID) REFERENCES dormer(DormerID))")
            conn.commit()
            conn.close()

        def addGuardian():
            conn = sqlite3.connect("logd.db")
            c = conn.cursor()
            c.execute("INSERT INTO guardian(Guardian_Name, Guardian_ContactNum, DdormerID) VALUES (?,?,?)",
                      (Guardian_Name.get(), Guardian_ContactNum.get(), DdormerID.get()))
            conn.commit()
            conn.close()
            Guardian_Name.set('')
            Guardian_ContactNum.set('')
            DdormerID.set('')
            tkinter.messagebox.showinfo("Guardian", "Successfully added!")
            displayGuardian()

        def displayGuardian():
            self.Guardianlist.delete(*self.Guardianlist.get_children())
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM guardian")
            rows = cur.fetchall()
            for row in rows:
                self.Guardianlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            conn.close()

        def updateGuardian():
            for selected in self.Guardianlist.selection():
                conn = sqlite3.connect("logd.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE guardian SET Guardian_Name=?, Guardian_ContactNum=?, DdormerID=? WHERE GuardianID=?",
                            (Guardian_Name.get(), Guardian_ContactNum.get(), DdormerID.get(), self.Guardianlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo(
                    "Guardian", "Successfully updated!")
                displayGuardian()
                clear()
                conn.close()

        def editGuardian():
            x = self.Guardianlist.focus()
            if x == "":
                tkinter.messagebox.showerror(
                    "Guardian", "Please select a record.")
                return
            values = self.Guardianlist.item(x, "values")
            Guardian_Name.set(values[0])
            Guardian_ContactNum.set(values[1])
            DdormerID.set(values[2])

        def deleteGuardian():
            try:
                messageDelete = tkinter.messagebox.askyesno(
                    "DORMLOG MONITOR SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:
                    con = sqlite3.connect("logd.db")
                    cur = con.cursor()
                    x = self.Guardianlist.selection()[0]
                    Guardian_Name = self.Guardianlist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute(
                        "DELETE FROM guardian WHERE Guardian_Name = ?", (Guardian_Name,))
                    con.commit()
                    self.Guardianlist.delete(x)
                    tkinter.messagebox.askyesno(
                        "Guardian", "Successfully deleted!")
                    displayGuardian()
                    con.close()
            except:
                tkinter.messagebox.showerror(
                    "Guardian", "already exist in the record")

        def searchGuardian():
            DdormerID = SearchBar_Var.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM guardian WHERE DdormerID = ?", (DdormerID,))
            con.commit()
            self.Guardianlist.delete(*self.Guardianlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.Guardianlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def Refresh():
            displayGuardian()

        def clear():

            Guardian_Name.set('')
            Guardian_ContactNum.set('')
            DdormerID.set('')

        def OnDoubleclick(event):
            item = self.Guardianlist.selection()[0]
            values = self.Guardianlist.item(item, "values")
            Guardian_Name.set(values[0])
            Guardian_ContactNum.set(values[1])
            DdormerID.set(values[2])

# ________WINDOW BUTTONS________#

        Button1 = dlms.Button(Bottom, text="Dormer", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10,bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Dormer))
        Button1.pack(side='right')


# ________LABELS AND ENTRIES________#
        InfoFrame = Frame(label, bd=4, relief=GROOVE)
        InfoFrame.config(bg=InfoFrame.master.cget('background'))
        InfoFrame.pack(side='top', fill='both', expand=True)

        self.lblDdormerID = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Dormer ID:", padx=5, pady=5,fg="#579ABE")
        self.lblDdormerID.config(bg=self.lblDdormerID.master.cget('background'))
        self.lblDdormerID.place(relx=0.5, rely=0.1, anchor='center')
        self.txtDdormerID = Entry(InfoFrame, font=("Time new roman", 28), textvariable=DdormerID, width=15,fg="black", bg="#fefeff")
        self.txtDdormerID.place(relx=0.5, rely=0.2, anchor='center')

        self.lblGuardianName = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Guardian Name:", padx=5, pady=5,fg="#579ABE")
        self.lblGuardianName.config(bg=self.lblGuardianName.master.cget('background'))
        self.lblGuardianName.place(relx=0.5, rely=0.3, anchor='center')
        self.txtGuardianName = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Guardian_Name, width=15,fg="black", bg="#fefeff")
        self.txtGuardianName.place(relx=0.5, rely=0.4, anchor='center')

        self.lblGuardianContactNum = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Guardian ContactNum:", padx=5, pady=5,fg="#579ABE")
        self.lblGuardianContactNum.config(bg=self.lblGuardianContactNum.cget('background'))
        self.lblGuardianContactNum.place(relx=0.5, rely=0.5, anchor='center')
        self.txtGuardianContactNum = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Guardian_ContactNum, width=15, fg="black", bg="#fefeff")
        self.txtGuardianContactNum.place(relx=0.5, rely=0.6, anchor='center')

        Info = Frame(table, bd=1, bg="#FFFEFC", relief=GROOVE, height=60)
        Info.pack(side='top', fill='x')
        
        self.SearchBarlbl = Label(Info, font=("Time new roman", 12, "bold"),text="Dormer ID:", padx=5, pady=5, fg="#809bce")
        self.SearchBarlbl.config(bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='left', anchor='w')
        self.SearchBar = Entry(Info, font=("Time new roman", 14), textvariable=SearchBar_Var, width=50, fg="#809bce", bg="#fefeff")
        self.SearchBar.pack(side='left', anchor='e', expand=True)
        self.btnSearch = Button(Info, text="SEARCH", font=("Palatino roman", 14, "bold"), bg="#fefeff", fg="#809bce", command=searchGuardian)
        self.btnSearch.pack(side='left')
        self.btnRefresh = Button(Info, text="Refresh", font=('Palatino roman', 14, "bold"), height=1, width=10, bg="#fefeff", fg="#809bce", command=Refresh)
        self.btnRefresh.pack(side='left')


# ________TREEVIEW________#

        scrollbar = Scrollbar(table, orient=VERTICAL)

        self.Guardianlist = ttk.Treeview(table, columns=(
            "Guardian_Name", "Guardian_ContactNum", "DdormerID"), height=20,  yscrollcommand=scrollbar.set)
        self.Guardianlist.heading("Guardian_Name", text="Guardian Name")
        self.Guardianlist.heading("Guardian_ContactNum", text="Contact Num")
        self.Guardianlist.heading("DdormerID", text="DormerID")
        self.Guardianlist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(
            "Source code", 18, "bold"), foreground="Black")
        style.configure("Treeview", font=("Source code", 15))
        style.map('Treeview', background=[
                  ('selected', 'grey')], foreground=[('selected', 'Black')])
        self.Guardianlist.column("Guardian_Name", width=250)
        self.Guardianlist.column("Guardian_ContactNum", width=200)
        self.Guardianlist.column("DdormerID", width=50)
        self.Guardianlist.bind("<Double-1> ", OnDoubleclick)
        self.Guardianlist.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.Guardianlist.yview)

# ________Guardian BUTTONS________#

        ButtonFrame = Frame(label, bd=4, bg="#fefeff", relief=GROOVE)
        ButtonFrame.pack(side='bottom', fill='both')

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=addGuardian)
        self.btnAddID.pack(side='left')
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=updateGuardian)
        self.btnUpdate.pack(side='left')
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=clear)
        self.btnClear.pack(side='left')
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=deleteGuardian)
        self.btnDelete.pack(side='left')

        connectGuardian()
        displayGuardian()


# ________Companion FUNCTIONS________#

class Companion(dlms.Frame):

    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title(" DORMLOG MONITOR SYSTEM")

        Top = Frame(self, bg="#809bce", height=1, relief='groove', bd=3)
        Top.pack(side='top', fill='x')

        label = dlms.Label(Top, text="C O M P A N I O N", bd=4, font=("Times new roman", 30, "bold"), fg="#ffffff")
        label.config(bg=label.master.cget('background'))
        label.pack(side='top', fill='x')

        Center = Frame(self, bg="#f9f6f2", relief='groove', bd=1)  # Increase the height to accommodate the larger treeview
        Center.pack(side='top', fill='both', expand=True)
        table = Frame(Center, relief='groove', bd=1)
        table.pack(side='left',fill='both', expand=True)
        table.config(bg=table.master.cget('background'))
        label = Frame(Center, relief='groove', bd=1)
        label.config(bg=label.master.cget('background'))
        label.pack(side='left',fill='y', expand = True)

        Bottom = Frame(self, bg="#809bce",height=1, relief='groove', bd=3)
        Bottom.pack(side='top', fill='x')


        Companion_Name = StringVar()
        Companion_ContactNum = StringVar()
        SearchBar_Var = StringVar()

        def connectCompanion():
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS companion(Companion_Name TEXT PRIMARY KEY, Companion_ContactNum TEXT)")
            conn.commit()
            conn.close()

        def addCompanion():
            conn = sqlite3.connect("logd.db")
            c = conn.cursor()
            c.execute("INSERT INTO companion(Companion_Name,Companion_ContactNum) VALUES (?,?)",
                      (Companion_Name.get(), Companion_ContactNum.get()))
            conn.commit()
            conn.close()
            Companion_Name.set('')
            Companion_ContactNum.set('')
            tkinter.messagebox.showinfo("Companion", "Successfully added!")
            displayCompanion()

        def displayCompanion():
            self.Companionlist.delete(*self.Companionlist.get_children())
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM companion")
            rows = cur.fetchall()
            for row in rows:
                self.Companionlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            conn.close()

        def updateCompanion():
            for selected in self.Companionlist.selection():
                conn = sqlite3.connect("logd.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE companion SET Companion_ContactNum=? WHERE Companion_Name=?",
                            (Companion_ContactNum.get(), self.Companionlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo(
                    "Companion", "Successfully updated!")
                displayCompanion()
                clear()
                conn.close()

        def editCompanion():
            x = self.Companionlist.focus()
            if x == "":
                tkinter.messagebox.showerror(
                    "Companion", "Please select a record.")
                return
            values = self.Companionlist.item(x, "values")
            Companion_Name.set(values[0])
            Companion_ContactNum.set(values[1])

        def deleteCompanion():
            try:
                messageDelete = tkinter.messagebox.askyesno(
                    " DORMLOG MONITOR SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:
                    con = sqlite3.connect("logd.db")
                    cur = con.cursor()
                    x = self.Companionlist.selection()[0]
                    Companion_Name = self.Companionlist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute(
                        "DELETE FROM companion WHERE Companion_Name = ?", (Companion_Name,))
                    con.commit()
                    self.Companionlist.delete(x)
                    tkinter.messagebox.askyesno(
                        "Companion", "Successfully deleted!")
                    displayCompanion()
                    con.close()
            except:
                tkinter.messagebox.showerror(
                    "Companion", "already exist in the record")

        def searchCompanion():
            Companion_Name = SearchBar_Var.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM companion WHERE Companion_Name = ?", (Companion_Name,))
            con.commit()
            self.Companionlist.delete(*self.Companionlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.Companionlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def Refresh():
            displayCompanion()

        def clear():

            Companion_Name.set('')
            Companion_ContactNum.set('')

        def OnDoubleclick(event):
            item = self.Companionlist.selection()[0]
            values = self.Companionlist.item(item, "values")
            Companion_Name.set(values[0])
            Companion_ContactNum.set(values[1])

# ________WINDOW BUTTONS________#

        Button1 = dlms.Button(Bottom, text="Logbook", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Logbook))
        Button1.pack(side='left')
        Button2 = dlms.Button(Bottom, text="Destination", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Destination))
        Button2.pack(side='right')


# ________LABELS AND ENTRIES________#
        InfoFrame = Frame(label, bd=4, relief=GROOVE)
        InfoFrame.pack(side='top', fill='both', expand=True)
        InfoFrame.config(bg=InfoFrame.master.cget('background'))

        self.lblCompanionName = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Companion Name:", padx=5, pady=5, fg="#579ABE")
        self.lblCompanionName.config(bg=self.lblCompanionName.master.cget('background'))
        self.lblCompanionName.place(relx=0.5, rely=0.3, anchor='center')
        self.txtCompanionName = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Companion_Name, width=15, fg="black", bg="#fefeff")
        self.txtCompanionName.place(relx=0.5, rely=0.4, anchor='center')

        self.lblCompanionContactNum = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Contact Number:", padx=5, pady=5,fg="#579ABE")
        self.lblCompanionContactNum.config(bg=self.lblCompanionContactNum.master.cget('background'))
        self.lblCompanionContactNum.place(relx=0.5, rely=0.5, anchor='center')
        self.txtCompanionContactNum = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Companion_ContactNum, width=15,fg="black", bg="#fefeff")
        self.txtCompanionContactNum.place(relx=0.5, rely=0.6, anchor='center')

        Info = Frame(table, bd=1, bg="#FFFEFC", relief=GROOVE, height=30)
        Info.pack(side='top', fill='x')

        self.SearchBarlbl = Label(Info, font=("Time new roman", 18, "bold"),
                                  text="Companion Name:", padx=5, pady=5,fg="#809bce")
        self.SearchBarlbl.config(bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='left', anchor='w')
        self.SearchBar = Entry(Info, font=("Time new roman", 18), textvariable=SearchBar_Var, width=25,fg="#809bce", bg="GHOSTWHITE")
        self.SearchBar.pack(side='left', anchor='e', expand=True)
        self.btnSearch = Button(Info, text="SEARCH", font=("Palatino roman", 14, "bold"), bg="#fefeff", fg="#809bce", command=searchCompanion)
        self.btnSearch.pack(side='left')
        self.btnRefresh = Button(Info, text="Refresh", font=('Palatino roman', 14, "bold"), height=1, width=10,bg="#fefeff", fg="#809bce", command=Refresh)
        self.btnRefresh.pack(side='right')


# ________TREEVIEW________#

        scrollbar = Scrollbar(table, orient=VERTICAL)

        self.Companionlist = ttk.Treeview(table, columns=(
            "Companion_Name", "Companion_ContactNum"), height=20,  yscrollcommand=scrollbar.set)
        self.Companionlist.heading("Companion_Name", text="Companion Name")
        self.Companionlist.heading("Companion_ContactNum", text="Contact Number")
        self.Companionlist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(
            "Source code", 18, "bold"), foreground="Black")
        style.configure("Treeview", font=("Source code", 15))
        style.map('Treeview', background=[
                  ('selected', 'grey')], foreground=[('selected', 'Black')])
        self.Companionlist.column("Companion_Name", width=50)
        self.Companionlist.column("Companion_ContactNum", width=400)
        self.Companionlist.bind("<Double-1> ", OnDoubleclick)
        self.Companionlist.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.Companionlist.yview)

# ________Companion BUTTONS________#

        ButtonFrame = Frame(label, bd=1, bg="#fefeff", relief=GROOVE)
        ButtonFrame.pack(side='bottom', fill='both')

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=addCompanion)
        self.btnAddID.pack(side='left',)
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=updateCompanion)
        self.btnUpdate.pack(side='left')
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=clear)
        self.btnClear.pack(side='left')
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=('Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=deleteCompanion)
        self.btnDelete.pack(side='left')

        connectCompanion()
        displayCompanion()


# ________Destination FUNCTIONS________#

class Destination(dlms.Frame):

    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title(" DORMLOG MONITOR SYSTEM")

        Top = Frame(self, bg="#809bce", height=1, relief='groove', bd=3)
        Top.pack(side='top', fill='x')

        label = dlms.Label(Top, text="D E S T I N A T I O N", bd=4, font=("Times new roman", 30, "bold"), fg="#ffffff")
        label.config(bg=label.master.cget('background'))
        label.pack(side='top', fill='x')

        DestID = StringVar()
        Complete_Address = StringVar()
        SearchBar_Var = StringVar()

        Center = Frame(self, bg="#f9f6f2", relief='groove', bd=1)  # Increase the height to accommodate the larger treeview
        Center.pack(side='top', fill='both', expand=True)
        table = Frame(Center, relief='groove', bd=1)
        table.pack(side='left',fill='both', expand=True)
        table.config(bg=table.master.cget('background'))
        label = Frame(Center, relief='groove', bd=1)
        label.config(bg=label.master.cget('background'))
        label.pack(side='left',fill='y', expand = True)

        Bottom = Frame(self, bg="#809bce",height=1, relief='groove', bd=3)
        Bottom.pack(side='top', fill='x')


        def connectDestination():
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS destination (DestID TEXT PRIMARY KEY, Complete_Address TEXT)")
            conn.commit()
            conn.close()

        def addDestination():
            conn = sqlite3.connect("logd.db")
            c = conn.cursor()
            c.execute("INSERT INTO destination(DestID, Complete_Address) VALUES (?,?)",
                      (DestID.get(), Complete_Address.get()))
            conn.commit()
            conn.close()
            DestID.set('')
            Complete_Address.set('')
            tkinter.messagebox.showinfo("Destination", "Successfully added!")
            displayDestination()

        def displayDestination():
            self.Destinationlist.delete(*self.Destinationlist.get_children())
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM destination")
            rows = cur.fetchall()
            for row in rows:
                self.Destinationlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            conn.close()

        def updateDestination():
            for selected in self.Destinationlist.selection():
                conn = sqlite3.connect("logd.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE destination SET Complete_Address=? WHERE DestID=?",
                            (Complete_Address.get(), self.Destinationlist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo(
                    "Destination", "Successfully updated!")
                displayDestination()
                clear()
                conn.close()

        def editDestination():
            x = self.Destinationlist.focus()
            if x == "":
                tkinter.messagebox.showerror(
                    "Destination", "Please select a record.")
                return
            values = self.Destinationlist.item(x, "values")
            DestID.set(values[0])
            Complete_Address.set(values[1])

        def deleteDestination():
            try:
                messageDelete = tkinter.messagebox.askyesno(
                    " DORMLOG MONITOR SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:
                    con = sqlite3.connect("logd.db")
                    cur = con.cursor()
                    x = self.Destinationlist.selection()[0]
                    DestID = self.Destinationlist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute(
                        "DELETE FROM destination WHERE DestID = ?", (DestID,))
                    con.commit()
                    self.Destinationlist.delete(x)
                    tkinter.messagebox.askyesno(
                        "Destination", "Successfully deleted!")
                    displayDestination()
                    con.close()
            except:
                tkinter.messagebox.showerror(
                    "Destination", "already exist in the record")

        def searchDestination():
            Complete_Address = SearchBar_Var.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute(
                "SELECT * FROM destination WHERE Complete_Address LIKE ?", ('%' + Complete_Address + '%',)) 
            con.commit()
            self.Destinationlist.delete(*self.Destinationlist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.Destinationlist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def Refresh():
            displayDestination()

        def clear():

            DestID.set('')
            Complete_Address.set('')

        def OnDoubleclick(event):
            item = self.Destinationlist.selection()[0]
            values = self.Destinationlist.item(item, "values")
            DestID.set(values[0])
            Complete_Address.set(values[1])

# ________WINDOW BUTTONS________#

        Button1 = dlms.Button(Bottom, text="Logbook", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Logbook))
        Button1.pack(side='left')
        Button2 = dlms.Button(Bottom, text="Companion", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Companion))
        Button2.pack(side='right')

# ________LABELS AND ENTRIES________#
        InfoFrame = Frame(label, bd=4, relief=GROOVE)
        InfoFrame.pack(side='top', fill='both', expand=True)
        InfoFrame.config(bg=InfoFrame.master.cget('background'))

        self.lblDestID = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Destination ID:", padx=5, pady=5, fg="#579ABE")
        self.lblDestID.config(bg=self.lblDestID.master.cget('background'))
        self.lblDestID.place(relx=0.5, rely=0.3, anchor='center')

        self.txtDestID = Entry(InfoFrame, font=("Time new roman", 28), textvariable=DestID, width=15,  fg="black", bg="#fefeff")
        self.txtDestID.place(relx=0.5, rely=0.4, anchor='center')

        self.lblCompleteAddress = Label(InfoFrame, font=("Time new roman", 18, "bold"), text="Complete Address:", padx=5, pady=5,fg="#579ABE")
        self.lblCompleteAddress.config(bg=self.lblCompleteAddress.master.cget('background'))
        self.lblCompleteAddress.place(relx=0.5, rely=0.5, anchor='center')

        self.txtCompleteAddress = Entry(InfoFrame, font=("Time new roman", 28), textvariable=Complete_Address, width=15,  fg="black", bg="#fefeff")
        self.txtCompleteAddress.place(relx=0.5, rely=0.6, anchor='center')



        Info = Frame(table, bd=1, bg="#FFFEFC", relief=GROOVE, height=30)
        Info.pack(side='top', fill='x')

        self.SearchBarlbl = Label(Info, font=("Time new roman", 18, "bold"), text="Address:", padx=5, pady=5, fg="#809bce")
        self.SearchBarlbl.config(bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='left', anchor='w')
        self.SearchBar = Entry(Info, font=( "Time new roman", 18), textvariable=SearchBar_Var, width=25,fg="#809bce", bg="GHOSTWHITE")
        self.SearchBar.pack(side='left', anchor='e', expand=True)
        self.btnSearch = Button(Info, text="SEARCH", font=("Palatino roman", 14, "bold"), bg="#fefeff", fg="#809bce", command=searchDestination)
        self.btnSearch.pack(side='left')
        self.btnRefresh = Button(Info, text="Refresh", font=( 'Palatino roman', 14, "bold"), height=1, width=10, bg="#fefeff", fg="#809bce", command=Refresh)
        self.btnRefresh.pack(side='right')


# ________TREEVIEW________#

        scrollbar = Scrollbar(table, orient=VERTICAL)

        self.Destinationlist = ttk.Treeview(table, columns=("DestID", "Complete_Address"), height=20, yscrollcommand=scrollbar.set)  # Increase the height to display more rows
        self.Destinationlist.heading("DestID", text="Destination ID")
        self.Destinationlist.heading("Complete_Address", text="Complete Address")
        self.Destinationlist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=( "Source code", 18, "bold"), foreground="Black")
        style.configure("Treeview", font=("Source code", 15))
        style.map('Treeview', background=[ ('selected', 'grey')], foreground=[('selected', 'Black')])
        self.Destinationlist.column("DestID", width=50)
        self.Destinationlist.column("Complete_Address", width=400)
        self.Destinationlist.bind("<Double-1> ", OnDoubleclick)
        self.Destinationlist.pack(side='left', fill='both', expand=True)  # Expand the treeview to fill available space
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.Destinationlist.yview)

# ________Destination BUTTONS________#

        ButtonFrame = Frame(label, bd=1, bg="#fefeff", relief=GROOVE)
        ButtonFrame.pack(side='bottom', fill='both')

        self.btnAddID = Button(ButtonFrame, text="ADD", font=('Palatino roman', 18, "bold"),
                               height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=addDestination)
        self.btnAddID.pack(side='left')
        self.btnUpdate = Button(ButtonFrame, text="UPDATE", font=(
            'Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=updateDestination)
        self.btnUpdate.pack(side='left')
        self.btnClear = Button(ButtonFrame, text="CLEAR", font=(
            'Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=clear)
        self.btnClear.pack(side='left')
        self.btnDelete = Button(ButtonFrame, text="DELETE", font=(
            'Palatino roman', 18, "bold"), height=1, width=7, bd=1, bg="#fefeff", fg="#579ABE", command=deleteDestination)
        self.btnDelete.pack(side='left')

        connectDestination()
        displayDestination()

# ________Logbook FUNCTIONS________#


class Logbook(dlms.Frame):

    def __init__(self, parent, controller):
        dlms.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("DORMLOG MONITOR SYSTEM")

        LogID = StringVar()
        DesNo = StringVar()
        DorNo = StringVar()
        ComNo = StringVar()
        Purpose = StringVar()
        Depart_datetime = StringVar()
        Return_expectedDate = StringVar()
        Return_actualDateTime = StringVar()
        SearchBar_Var = StringVar()
        SearchBar_Var2 = StringVar()

        Admin_dateFrame = Frame(self, bg= "#809bce", height=1, relief='groove', bd=3)
        Admin_dateFrame.pack(side='top', fill='x')
        logbook_frame = Frame(self, bg="#F5FEFD",height=200, relief='groove', bd=1)
        logbook_frame.pack(side='top', fill='x')
        tableframe = Frame(self, bg="#F5FEFD", relief='groove', bd=1)
        tableframe.pack(side='top', fill='both', expand=True)
        tableframe.pack_propagate(0)

        button_frame = Frame(self, bg= "#809bce",height=1, relief='groove', bd=3)
        button_frame.pack(side='top', fill='x')

        clockdateLabel = tk.Label(Admin_dateFrame, font=('times', 18, 'bold'), relief='flat', compound='left', fg="#FFFEFC")
        clockdateLabel.config(bg=clockdateLabel.master.cget('background'))
        clockdateLabel.place(x=10, y=15)

        clocktimLabel = tk.Label(Admin_dateFrame, font=('times', 18, 'bold'), relief='flat', fg="#FFFEFC")
        clocktimLabel.config(bg=clocktimLabel.master.cget('background'))
        clocktimLabel.place(x=210, y=15)

        self.update_clock(clockdateLabel, clocktimLabel)

        Date_Tim(clockdateLabel, clocktimLabel)

        self.update_clock(clockdateLabel, clocktimLabel)

        def connectLogbook():
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS logbook (LogID TEXT PRIMARY KEY,DesNo TEXT,DorNo TEXT,ComNo TEXT,Purpose TEXT,Depart_datetime TEXT,Return_expectedDate TEXT,Return_actualDateTime TEXT,FOREIGN KEY (DorNo) REFERENCES dormer(DormerID),FOREIGN KEY (DesNo) REFERENCES destination(DestID),FOREIGN KEY (ComNo) REFERENCES companion(Companion_Name))")
            conn.commit()
            conn.close()

        def addLogbook():
            conn = sqlite3.connect("logd.db")
            c = conn.cursor()
            log_id = LogID.get()
            c.execute("SELECT * FROM logbook WHERE LogID=?", (log_id,))
            existing_log = c.fetchone()
            if existing_log:
                conn.close()
                tkinter.messagebox.showerror("Logbook", f"Log ID '{log_id}' already exists!")
                return
        
            c.execute("INSERT INTO logbook(LogID,DesNo,DorNo,ComNo,Purpose,Depart_datetime,Return_expectedDate,Return_actualDateTime) VALUES (?,?,?,?,?,?,?,?)",
                      (LogID.get(), DesNo.get(), DorNo.get(), ComNo.get(), Purpose.get(), Depart_datetime.get(), Return_expectedDate.get(), Return_actualDateTime.get()))
            conn.commit()
            conn.close()
            LogID.set('')
            DesNo.set('')
            DorNo.set('')
            ComNo.set('')
            Purpose.set('')
            Depart_datetime.set('')
            Return_expectedDate.set('')
            Return_actualDateTime.set('')
            tkinter.messagebox.showinfo("Logbook", "Successfully added!")

            displayLogbook()

        def displayLogbook():
            self.Logbooklist.delete(*self.Logbooklist.get_children())
            conn = sqlite3.connect("logd.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM logbook")
            rows = cur.fetchall()
            for row in rows:
                self.Logbooklist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            conn.close()

        def updateLogbook():
            for selected in self.Logbooklist.selection():
                conn = sqlite3.connect("logd.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("UPDATE logbook SET Return_actualDateTime=? WHERE LogID=?",
                            (Return_actualDateTime.get(), self.Logbooklist.set(selected, '#1')))
                conn.commit()
                tkinter.messagebox.showinfo("Logbook", "Successfully updated!")
                displayLogbook()
                clear()
                conn.close()

        def editLogbook():
            x = self.Logbooklist.focus()
            if x == "":
                tkinter.messagebox.showerror(
                    "Logbook", "Please select a record.")
                return
            values = self.Logbooklist.item(x, "values")
            LogID.set(values[0])
            DesNo.set(values[1])
            DorNo.set(values[2])
            ComNo.set(values[3])
            Purpose.set(values[4])
            Depart_datetime.set(values[5])
            Return_expectedDate.set(values[6])
            Return_actualDateTime.set(values[7])

        def deleteLogbook():
            try:
                messageDelete = tkinter.messagebox.askyesno(
                    " DORMLOG MONITOR SYSTEM", "Are you sure you want to delete this record?")
                if messageDelete > 0:
                    con = sqlite3.connect("logd.db")
                    cur = con.cursor()
                    x = self.Logbooklist.selection()[0]
                    LogID = self.Logbooklist.item(x)["values"][0]
                    cur.execute("PRAGMA foreign_keys = ON")
                    cur.execute(
                        "DELETE FROM logbook WHERE LogID = ?", (LogID,))
                    con.commit()
                    self.Logbooklist.delete(x)
                    tkinter.messagebox.askyesno(
                        "Logbook", "Successfully deleted!")
                    displayLogbook()
                    con.close()
            except:
                tkinter.messagebox.showerror(
                    "Logbook", "already exist in the record")

        def searchLogbook():
            DorNo = SearchBar_Var.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM logbook WHERE DorNo = ?", (DorNo,))
            con.commit()
            self.Logbooklist.delete(*self.Logbooklist.get_children())
            rows = cur.fetchall()
            for row in rows:
                self.Logbooklist.insert(
                    "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def searchLobook():

            Depart_datetime = SearchBar_Var2.get()
            con = sqlite3.connect("logd.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM logbook WHERE Depart_datetime LIKE ?",
                        ('%' + Depart_datetime + '%',))
            con.commit()
            self.Logbooklist.delete(*self.Logbooklist.get_children())
            rows = cur.fetchall()
            if len(rows) == 0:
                tkinter.messagebox.showinfo(
                    "Logbook", "No entries found for the specified date.")
            else:
                for row in rows:
                    self.Logbooklist.insert(
                        "", dlms.END, text=row[0], values=row[0:])
            con.close()

        def Refresh():
            displayLogbook()

        def clear():

            LogID.set('')
            DesNo.set('')
            DorNo.set('')
            ComNo.set('')
            Purpose.set('')
            Depart_datetime.set('')
            Return_expectedDate.set('')
            Return_actualDateTime.set('')

        def OnDoubleclick(event):
            item = self.Logbooklist.selection()[0]
            values = self.Logbooklist.item(item, "values")
            LogID.set(values[0])
            DesNo.set(values[1])
            DorNo.set(values[2])
            ComNo.set(values[3])
            Purpose.set(values[4])
            Depart_datetime.set(values[5])
            Return_expectedDate.set(values[6])
            Return_actualDateTime.set(values[7])

# ________WINDOW BUTTONS________#

        Button1 = dlms.Button(button_frame, text="Destination", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Destination))
        Button1.pack(side='right')
        Button2 = dlms.Button(button_frame, text="Home", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Home))
        Button2.pack(side='left')
        Button3 = dlms.Button(button_frame, text="Companion", font=("Palatino roman", 20, "bold"), bd=10,
                              width=10, bg="#fefeff", fg="#809bce", command=lambda: controller.ShowFrame(Companion))
        Button3.pack(side='right')

# ________LABELS AND ENTRIES________#

        entry = Frame(logbook_frame, relief=GROOVE, bd=5)
        entry.pack(fill='both')
        entry.config(bg=entry.master.cget('background'))

        self.lblLogID = Label(entry, font=("Time new roman", 15), text="Log ID:", padx=5, pady=5, fg="black")
        self.lblLogID.config(bg=self.lblLogID.master.cget('background'))
        self.lblLogID.grid(row=0, column=0, sticky='w')
        self.txtLogID = Entry(entry, font=("Time new roman", 15), textvariable=LogID, width=15, fg="black", bg="ghostwhite")
        self.txtLogID.grid(row=0, column=1, sticky='w')

        self.lblDesNo = Label(entry, font=("Time new roman", 15), text="Destination ID:", padx=5, pady=5, fg="black")
        self.lblDesNo.config(bg=self.lblDesNo.master.cget('background'))
        self.lblDesNo.grid(row=0, column=2, sticky='w')
        self.txtDesNo = Entry(entry, font=( "Time new roman", 15), textvariable=DesNo, width=15, fg="black", bg="ghostwhite")
        self.txtDesNo.grid(row=0, column=3, sticky='w')

        self.lblDorNo = Label(entry, font=("Time new roman", 15), text="Dormer ID:", padx=5, pady=5, fg="black")
        self.lblDorNo.config(bg=self.lblDorNo.master.cget('background'))
        self.lblDorNo.grid(row=1, column=0, sticky='w')
        self.txtDorNo = Entry(entry, font=("Time new roman", 15), textvariable=DorNo, width=15, fg="black", bg="GHOSTWHITE")
        self.txtDorNo.grid(row=1, column=1, sticky='w')

        self.lblComNo = Label(entry, font=("Time new roman", 15), text="Companion:", padx=5, pady=5, fg="black")
        self.lblComNo.config(bg=self.lblComNo.master.cget('background'))
        self.lblComNo.grid(row=1, column=2, sticky='w')
        self.txtComNo = Entry(entry, font=("Time new roman", 15), textvariable=ComNo, width=15, fg="black", bg="ghostwhite")
        self.txtComNo.grid(row=1, column=3, sticky='w')

        self.lblPurpose = Label(entry, font=("Time new roman", 15), text="Purpose:", padx=5, pady=5, fg="black")
        self.lblPurpose.config(bg=self.lblPurpose.master.cget('background'))
        self.lblPurpose.grid(row=2, column=2, sticky='w')
        self.txtPurpose = Entry(entry, font=("Time new roman", 15), textvariable=Purpose, width=30, fg="black", bg="ghostwhite")
        self.txtPurpose.grid(row=2, column=3, sticky='w')

        current_date = datetime.now().date()
        current_time = datetime.now().time()


        self.lblDepart_datetime = Label(entry, font=("Time new roman", 15), text="Departure Date & Time:", padx=5, pady=5, fg="black")
        self.lblDepart_datetime.config(bg=self.lblDepart_datetime.master.cget('background'))
        self.lblDepart_datetime.grid(row=0, column=4, sticky='w')

        self.txtDepart_date = DateEntry(entry, font=("Time new roman", 15), textvariable=Depart_datetime, width=15, fg="black")
        self.txtDepart_date.grid(row=0, column=5, sticky='w')
        self.txtDepart_date.set_date(current_date)

        self.txtDepart_time = Entry(entry, font=("Time new roman", 15), width=7, fg="black")
        self.txtDepart_time.grid(row=0, column=6, sticky='w')
        self.txtDepart_time.insert(0, current_time.strftime("%H:%M"))

        self.lblReturn_expectedDate = Label(entry, font=("Time new roman", 15), text="Expected Return Date:", padx=5, pady=5, fg="black")
        self.lblReturn_expectedDate.config(bg=self.lblReturn_expectedDate.master.cget('background'))
        self.lblReturn_expectedDate.grid(row=1, column=4, sticky='w')

        self.txtReturn_expectedDate = DateEntry(entry, font=("Time new roman", 15), textvariable=Return_expectedDate, width=15, fg="black")
        self.txtReturn_expectedDate.grid(row=1, column=5, sticky='w')

        self.lblReturn_actualDateTime = Label(entry, font=("Time new roman", 15), text="Actual Return Date & Time:", padx=5, pady=5, fg="black")
        self.lblReturn_actualDateTime.config(bg=self.lblReturn_actualDateTime.master.cget('background'))
        self.lblReturn_actualDateTime.grid(row=2, column=4, sticky='w')

        self.txtReturn_date = DateEntry(entry, font=("Time new roman", 15), textvariable=Return_actualDateTime, width=15, fg="black")
        self.txtReturn_date.grid(row=2, column=5, sticky='w')
        self.txtReturn_date.set_date(current_date)

        self.txtReturn_time = Entry(entry, font=("Time new roman", 15), width=7, fg="black")
        self.txtReturn_time.grid(row=2, column=6)
        self.txtReturn_time.insert(0, current_time.strftime("%H:%M"))


        InfoFrame = Frame(Admin_dateFrame, bd=4, bg="#f9f6f2", relief=GROOVE)
        InfoFrame.pack(side='right', fill='x')

        self.btnSearch = Button(InfoFrame, text="SEARCH", font=(
            "Palatino roman", 12, "bold"), bg="#fefeff", fg="#809bce", command=searchLogbook)
        self.btnSearch.pack(side='right', padx=10, pady=10)
        self.SearchBar = Entry(InfoFrame, font=(
            "Time new roman", 15), textvariable=SearchBar_Var, width=18, fg="black", bg="#fefeff")
        self.SearchBar.pack(side='right', padx=10, pady=10)
        self.SearchBarlbl = Label(InfoFrame, font=(
            "Time new roman", 15, "bold"), text="DormerID:", bg="GHOSTWHITE", fg="#809bce")
        self.SearchBarlbl.config(bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='right', padx=10, pady=10)

        self.btnSearch = Button(InfoFrame, text="SEARCH", font=(
            "Palatino roman", 12, "bold"), bg="#fefeff", fg="#809bce", command=searchLobook)
        self.btnSearch.pack(side='right', padx=10, pady=10)
        self.SearchBarlbl.pack(side='right', padx=10, pady=10)
        self.SearchBar = Entry(InfoFrame, font=(
            "Time new roman", 15), textvariable=SearchBar_Var2, width=18, fg="black", bg="#fefeff")
        self.SearchBar.pack(side='right', padx=10, pady=10)
        self.SearchBarlbl = Label(InfoFrame, font=(
            "Time new roman", 15, "bold"), text="Date:", bg="GHOSTWHITE", fg="#809bce")
        self.SearchBarlbl.config(
            bg=self.SearchBarlbl.master.cget('background'))
        self.SearchBarlbl.pack(side='right', padx=10, pady=10)

# ________TREEVIEW________#

        scrollbar_frame = Frame(tableframe)
        scrollbar_frame.pack(side='right', fill='y')

        scrollbar = Scrollbar(scrollbar_frame, orient=VERTICAL)

        self.Logbooklist = ttk.Treeview(tableframe, columns=("LogID", "DesNo", "DorNo", "ComNo", "Purpose", "Depart_datetime", "Return_expectedDate", "Return_actualDateTime"), height=10, yscrollcommand=scrollbar.set)
        self.Logbooklist.heading("LogID", text="LogID")
        self.Logbooklist.heading("DesNo", text="DestinationID")
        self.Logbooklist.heading("DorNo", text="DormerID")
        self.Logbooklist.heading("ComNo", text="Companion")
        self.Logbooklist.heading("Purpose", text="Purpose")
        self.Logbooklist.heading("Depart_datetime", text="Depart")
        self.Logbooklist.heading("Return_expectedDate", text="Expected Return")
        self.Logbooklist.heading("Return_actualDateTime", text="Return")
        self.Logbooklist['show'] = 'headings'
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(
            "Source code", 12, "bold"), foreground="Black")
        style.configure("Treeview", font=("Source code", 15))
        style.map('Treeview', background=[('selected', 'grey')], foreground=[('selected', 'Black')])
        self.Logbooklist.column("LogID", width=100)
        self.Logbooklist.column("DesNo", width=150)
        self.Logbooklist.column("DorNo", width=100)
        self.Logbooklist.column("ComNo", width=225)
        self.Logbooklist.column("Purpose", width=235)
        self.Logbooklist.column("Depart_datetime", width=100)
        self.Logbooklist.column("Return_expectedDate", width=200)
        self.Logbooklist.column("Return_actualDateTime", width=80)
        self.Logbooklist.bind("<Double-1> ", OnDoubleclick)
        self.Logbooklist.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        scrollbar.config(command=self.Logbooklist.yview)




# ________Logbook BUTTONS________#

        buttonframe = Frame(logbook_frame, bg="#F5FEFD", relief=GROOVE,width=10, bd=2)
        buttonframe.pack(side='top', fill='both')

        self.btnRefresh = Button(buttonframe, text="Refresh", font=(
            'Palatino roman', 12, "bold"), height=1, width=7, bg="#FFFEFC", fg="#809bce", command=Refresh)
        self.btnRefresh.pack(side='right')
        self.btnAddID = Button(buttonframe, text="ADD", font=(
            'Palatino roman', 14, "bold"), height=1, width=7, bg="#FFFEFC", fg="#809bce", command=addLogbook)
        self.btnAddID.pack(side='left', padx=0, pady=0)
        self.btnUpdate = Button(buttonframe, text="UPDATE", font=(
            'Palatino roman', 14, "bold"), height=1, width=7, bg="#FFFEFC", fg="#809bce", command=updateLogbook)
        self.btnUpdate.pack(side='left', padx=0, pady=0)
        self.btnClear = Button(buttonframe, text="CLEAR", font=(
            'Palatino roman', 14, "bold"), height=1, width=7, bg="#FFFEFC", fg="#809bce", command=clear)
        self.btnClear.pack(side='left', padx=0, pady=0)
        self.btnDelete = Button(buttonframe, text="DELETE", font=(
            'Palatino roman', 14, "bold"), height=1, width=7, bg="#FFFEFC", fg="#809bce", command=deleteLogbook)
        self.btnDelete.pack(side='left', padx=0, pady=0)

        connectLogbook()
        displayLogbook()

    def update_clock(self, date_label, time_label):
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%m/%d/%Y")
        time_label.configure(text="Time: " + time_string)
        date_label.configure(text="Date: " + date_string)
        self.after(1000, lambda: self.update_clock(date_label, time_label))


def Date_Tim(clockdateLabel, clocktimLabel):
    time_string = time.strftime("%H:%M:%S")
    date_string = time.strftime("%m/%d/%Y")
    clocktimLabel.configure(text="Time: " + time_string)
    clockdateLabel.configure(text="Date: " + date_string)
    clocktimLabel.after(1000, lambda: Date_Tim(clockdateLabel, clocktimLabel))


app = AppDatabase()
app.geometry("1350x750+0+0")
app.mainloop()
