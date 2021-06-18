from tkinter import *
from dbhelper import DB
from tkinter import messagebox
from PIL import Image,ImageTk
# pip install Pillow
from tkinter import filedialog
import shutil

class Tinder:

    def __init__(self):
        # connect to the db
        self.db = DB()
        # load the reg GUI
        self.root = Tk()
        self.root.title('Tinder Registration')
        self.root.maxsize(300, 500)
        self.root.minsize(300, 500)

        self.root.configure(background='#2906A8')

        self.load_reg_gui()

    def load_reg_gui(self):

        self.clear_gui()

        self.label1 = Label(self.root, text="Tinder", bg='#2906A8', fg='#ffffff')
        self.label1.pack(pady=(10, 10))
        self.label1.configure(font=('Verdana', 22, 'bold'))

        # creating a label
        self.label2 = Label(self.root, text="SignUp Here", bg='#2906A8', fg='#ffffff')
        self.label2.pack(pady=(10, 10))
        self.label2.configure(font=('Verdana', 12, 'italic'))

        self.name_input = Entry(self.root)
        self.name_input.insert(0, 'Name')
        self.name_input.pack(pady=(20,10),ipadx=80,ipady=10)

        self.email_input = Entry(self.root)
        self.email_input.insert(0, 'Email')
        self.email_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.password_input = Entry(self.root)
        self.password_input.insert(0, 'Password')
        self.password_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.reg_btn = Button(self.root,text='Sign Up',bg='#ffffff',width=30,height=2, command=lambda :self.perform_reg())
        self.reg_btn.pack(pady=(20,20))
        self.reg_btn.configure(font=('Verdana',10))

        self.label3 = Label(self.root, text="Already a member?", bg='#2906A8', fg='#ffffff')
        self.label3.pack(pady=(10, 10))
        self.label3.configure(font=('Verdana', 8, 'italic'))

        self.login_btn = Button(self.root, text='Login', bg='#ffffff', width=20, height=2,command=lambda: self.load_login_gui())
        self.login_btn.pack(pady=(0, 20))
        self.login_btn.configure(font=('Verdana', 8))


        self.root.mainloop()

    def load_edit_page(self):
        self.clear_gui()

        self.label1 = Label(self.root, text="Tinder", bg='#2906A8', fg='#ffffff')
        self.label1.pack(pady=(10, 10))
        self.label1.configure(font=('Verdana', 22, 'bold'))

        # creating a label
        self.label2 = Label(self.root, text="Edit Profile", bg='#2906A8', fg='#ffffff')
        self.label2.pack(pady=(10, 10))
        self.label2.configure(font=('Verdana', 12, 'italic'))

        self.gender_input = Entry(self.root)
        self.gender_input.insert(0, 'Gender')
        self.gender_input.pack(pady=(20, 10), ipadx=80, ipady=10)

        self.age_input = Entry(self.root)
        self.age_input.insert(0, 'Age')
        self.age_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.city_input = Entry(self.root)
        self.city_input.insert(0, 'City')
        self.city_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.edit_btn = Button(self.root, text='Edit Profile', bg='#ffffff', width=30, height=2,
                              command=lambda: self.edit_user_profile())
        self.edit_btn.pack(pady=(10,10))

    def edit_user_profile(self):
        gender = self.gender_input.get()
        age = self.age_input.get()
        city = self.city_input.get()

        result = self.db.edit_profile(self.user_id,gender,age,city)
        if result == 1:
            messagebox.showinfo("Tinder","Profile updated")
        else:
            messagebox.showerror("Tinder","Some error occured")



    def clear_gui(self,i=0):
        for i in self.root.pack_slaves()[i:]:
            i.destroy()

    def load_header_menu(self):
        menubar = Menu(self.root)

        filemenu = Menu(menubar, tearoff=0)

        filemenu.add_command(label="Browse Profiles",command=lambda :self.browse_profiles())
        filemenu.add_command(label="My Profile",command=lambda :self.load_profile_gui())
        filemenu.add_command(label="Edit Profile",command=lambda :self.load_edit_page())
        filemenu.add_command(label="Logout",command=lambda :self.logout())

        menubar.add_cascade(label="Profile", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="My Requests",command=lambda :self.fetch_requests())
        editmenu.add_command(label="My Proposals",command=lambda :self.fetch_proposals())
        editmenu.add_command(label="My Matches",command=lambda :self.fetch_matches())

        menubar.add_cascade(label="Options",menu=editmenu)

        self.root.config(menu=menubar)

    def fetch_requests(self):
        data = self.db.fetch_request_data(self.user_id)
        self.intermediate(data,show_propose_btn=0)

    def fetch_proposals(self):
        data = self.db.fetch_proposal_data(self.user_id)
        self.intermediate(data,show_propose_btn=1)

    def fetch_matches(self):
        data = self.db.fetch_matches_data(self.user_id)
        self.intermediate(data, show_propose_btn=0)

    def browse_profiles(self):
        # load data from database
        data = self.db.fetch_profile_data(self.user_id)
        self.intermediate(data)
        # list of tuple where each user is a tuple
        # display data

    def intermediate(self,data,index=0,show_propose_btn=1):
        self.load_others_profile_gui(data,index,show_propose_btn)

    def load_others_profile_gui(self,data,index,show_propose_btn=1):

        self.clear_gui(0)

        # create a menu
        self.load_header_menu()
        # print(data)
        # user name
        self.label2 = Label(self.root, text=data[index][1], bg='#2906A8', fg='#ffffff')
        self.label2.pack(pady=(10, 10))
        self.label2.configure(font=('Verdana', 16))

        text = "{} years old {} from {}".format(data[index][4], data[index][6], data[index][5])
        self.label2 = Label(self.root, text=text, bg='#2906A8', fg='#ffffff')
        self.label2.pack(pady=(0, 10))
        self.label2.configure(font=('Verdana', 13))

        frame = Frame(self.root)
        frame.pack()

        if index == 0:
            index1 = len(data)-1
        else:
            index1 = index
        prev = Button(frame,text="Previous", bg='#ffffff', width=10, height=1,command=lambda :self.intermediate(data,index1-1,show_propose_btn))
        prev.pack(side=LEFT)

        if show_propose_btn == 1:
            propose = Button(frame, text="Propose", bg='#ffffff', width=10, height=1,command=lambda :self.propose(data[index][0]))
            propose.pack(side=LEFT)

        if index == len(data) -1:
            index = -1

        next = Button(frame, text="Next", bg='#ffffff', width=10, height=1,command=lambda :self.intermediate(data,index+1,show_propose_btn))
        next.pack(side=LEFT)

    def propose(self,juliet_id):

        response = self.db.propose_user(self.user_id,juliet_id)
        if response == 1:
            messagebox.showinfo("Tinder","Proposal sent successfully")
        elif response == 0:
            messagebox.showerror("Tinder","Cannot propose twice")
        else:
            messagebox.showerror("Tinder","Some error occured! Try again")

    def change_dp(self):
        pathname = filedialog.askopenfilename(initialdir="/images", title="something")
        filename = pathname.split('/')[-1]
        #D:\My Projects\ML Projects\tinder-stp2021\img
        shutil.copyfile(pathname, "D:\\My Projects\\ML Projects\\tinder-stp2021\\img\\" + filename)
        # update the dp in the database
        self.db.update_dp(self.user_id,filename)
        self.load_profile_gui()


    def load_profile_gui(self):

        self.clear_gui(0)

        # create a menu
        self.load_header_menu()

        # fetch the logged in users data from db
        data = self.db.fetch_user_data(self.user_id)

        # load dp
        imageUrl = "img/{}".format(data[0][-1])

        load = Image.open(imageUrl)
        load = load.resize((200, 200), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(image=render)
        img.image = render
        img.pack()

        self.dp = Button(self.root, text="Change dp", command=lambda: self.change_dp())
        self.dp.pack(pady=(5, 5))


        #print(data)
        # user name
        if data != 0:
            self.label2 = Label(self.root, text=data[0][1], bg='#2906A8', fg='#ffffff')
            self.label2.pack(pady=(10, 10))
            self.label2.configure(font=('Verdana', 16))

            text = "{} years old {} from {}".format(data[0][4],data[0][6],data[0][5])
            self.label2 = Label(self.root, text=text, bg='#2906A8', fg='#ffffff')
            self.label2.pack(pady=(0, 10))
            self.label2.configure(font=('Verdana', 13))
        #

    def load_login_gui(self):
        # load the login gui
        # clear the exisiting gui
        self.clear_gui()
        self.root.config(menu="")

        self.label1 = Label(self.root, text="Tinder", bg='#2906A8', fg='#ffffff')
        self.label1.pack(pady=(10, 10))
        self.label1.configure(font=('Verdana', 22, 'bold'))
        # create gui
        # creating a label
        self.label2 = Label(self.root, text="Login Here", bg='#2906A8', fg='#ffffff')
        self.label2.pack(pady=(10, 10))
        self.label2.configure(font=('Verdana', 12, 'italic'))

        self.email_input = Entry(self.root)
        self.email_input.insert(0, 'Email')
        self.email_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.password_input = Entry(self.root)
        self.password_input.insert(0, 'Password')
        self.password_input.pack(pady=(10, 10), ipadx=80, ipady=10)

        self.signin_btn = Button(self.root, text='Login', bg='#ffffff', width=30, height=2,
                                 command=lambda: self.perform_login())
        self.signin_btn.pack(pady=(20, 20))
        self.signin_btn.configure(font=('Verdana', 10))

        self.label3 = Label(self.root, text="Not a member?", bg='#2906A8', fg='#ffffff')
        self.label3.pack(pady=(10, 10))
        self.label3.configure(font=('Verdana', 8, 'italic'))

        self.signup_btn = Button(self.root, text='Register', bg='#ffffff', width=20, height=2,
                                 command=lambda: self.load_reg_gui())
        self.signup_btn.pack(pady=(0, 20))
        self.signup_btn.configure(font=('Verdana', 8))

    def perform_login(self):
        # step 1 - fetch the input provided by the user
        email = self.email_input.get()
        password = self.password_input.get()

        # login
        data = self.db.login_user(email,password)
        if data == 0:
            messagebox.showerror("Tinder","Some error occured")
        else:
            if len(data) == 0:
                messagebox.showerror("Tinder","Incorrect email/password")
            else:
                # save user id of logged in user
                self.user_id = data[0][0]
                # load profile gui
                self.load_profile_gui()


    def perform_reg(self):
        # step 1 fetch input proivided by the user
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        # register
        response = self.db.register_user(name,email,password)
        if response == 1:
            print("Reg successful")
            messagebox.showinfo("Tinder","Registration Successful")
        else:
            print("Reg Failed")
            messagebox.showerror("Tinder","Some error occured")

    def logout(self):
        self.user_id = None
        self.load_login_gui()


obj = Tinder()

