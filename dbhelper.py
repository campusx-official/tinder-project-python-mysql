import mysql.connector

class DB:

    def __init__(self):
        # connect to database
        try:
            self.conn = mysql.connector.connect(host='localhost',user='root',password='',database='tinder')
            self.mycursor = self.conn.cursor()
            print("Connected to Database")

        except:
            print("Some error occured")

    def register_user(self,name,email,password):
        try:
            query = "INSERT INTO users (user_id,name,email,password,dp) VALUES (NULL,'{}','{}','{}','avatar.png')".format(name,email,password)
            self.mycursor.execute(query)
            self.conn.commit()
            return 1
        except:
            return 0

    def login_user(self,email,password):
        try:
            query = "SELECT * FROM users WHERE email LIKE '{}' AND password LIKE '{}'".format(email,password)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def fetch_user_data(self,user_id):
        try:
            query = "SELECT * FROM users WHERE user_id={}".format(user_id)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def fetch_profile_data(self,user_id):
        try:
            query = "SELECT * FROM users WHERE user_id!={}".format(user_id)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def fetch_request_data(self,user_id):
        try:
            query = "SELECT * FROM users u JOIN proposals p ON p.juliet_id = u.user_id WHERE p.romeo_id = {}".format(user_id)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def fetch_proposal_data(self,user_id):
        try:
            query = "SELECT * FROM users u JOIN proposals p ON u.user_id = p.romeo_id WHERE p.juliet_id = {}".format(user_id)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def fetch_matches_data(self,user_id):
        try:
            query = "SELECT * FROM users u JOIN proposals p ON p.juliet_id = u.user_id WHERE p.juliet_id IN (SELECT p.romeo_id FROM proposals p WHERE p.juliet_id = {}) AND p.romeo_id = {}".format(user_id,user_id)
            self.mycursor.execute(query)
            data = self.mycursor.fetchall()
            return data
        except:
            return 0

    def propose_user(self,romeo_id,juliet_id):

        query1 = "SELECT * FROM proposals WHERE romeo_id={} AND juliet_id={}".format(romeo_id,juliet_id)
        self.mycursor.execute(query1)
        data = self.mycursor.fetchall()

        if len(data) == 0:
            try:
                query = "INSERT INTO proposals VALUES (NULL,{},{})".format(romeo_id,juliet_id)
                self.mycursor.execute(query)
                self.conn.commit()
                return 1
            except:
                return -1
        else:
            return 0

    def update_dp(self,user_id,filename):
        query = "UPDATE users SET dp = '{}' WHERE user_id={}".format(filename,user_id)
        try:
            self.mycursor.execute(query)
            self.conn.commit()
            return 1
        except:
            return 0

    def edit_profile(self,user_id,gender,age,city):
        query = "UPDATE users SET age={},gender='{}',city='{}' WHERE user_id={}".format(age,gender,city,user_id)
        try:
            self.mycursor.execute(query)
            self.conn.commit()
            return 1
        except:
            print(query)
            return 0
