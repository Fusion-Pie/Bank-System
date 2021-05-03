import string as s
import random as ran
import datetime as dt
import mysql.connector as myconn

bank_db = myconn.connect (                                                      #Connecting Database 
        host="localhost",
        user="Pie_Bank",
        password="piyush@1234",
        database = "pie_bank")

bank_cur = bank_db.cursor()                                                     #Creating cursor                                          


class Bank:
    bank_name = "Pie Bank Of India"
    
    def CreateUser(self):                                                      #Create New User
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        self.first_name = input("\nEnter First Name: ")
        self.last_name = input("Enter Last Name: ")
        self.mob_no = input("Enter Mobile No: ")
        self.address = input("Enter Address: ")
        self.pin = input("Enter Pin: ")
        
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        print("\nYou have to deposit atleast 1000Rs")
        self.deposit_amount = int(input("\nEnter Amount To Deposit: "))
        
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        
        if self.deposit_amount >= 1000:    
            
            user.CardGenerator()
            
            self.dt = dt.datetime.now()
            self.dt = str(self.dt).split()
            
            query = "Insert into Bank_Users(First_Name,Last_Name,Address,Mobile_No,Card_no,Pin,Balance,Opening_Date,Acc_Status) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (self.first_name,self.last_name,self.address,self.mob_no,self.card_no,self.pin,self.deposit_amount,self.dt[0],'o')
        
            bank_cur.execute(query , val)
            bank_db.commit()
            
        
            print("\n\n-------------------------------------------------------------------------------------------------------------------------------")
            print("\nCongratulations! Account Created Successfully")
            print("\nThank You! For Choosing Us")
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        else:
            
            print("\nDeposit amount is low to open an account")
            print("\nPlease try again later")
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
    
    def AllExistingUser(self):                                                  #Show all user from the Databse
        bank_cur.execute("Select * from Bank_Users")
        
        result = bank_cur.fetchall()
        
        for i in result:
            print(i)
            
    
    def CheckBalance(self,p):                                                   #Checks Balance
        query = "Select Balance,First_Name from Bank_Users where Pin = %s"
        val = (p,)
        
        bank_cur.execute(query,val)
        
        result = bank_cur.fetchall()
              
        print(f"\nHi! {result[0][1]}, Your available balance is {result[0][0]}Rs") 
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
    
    
    def CheckPin(self,p):                              
        query = "Select First_Name from Bank_Users where Pin = %s"
        val = (p,)
        bank_cur.execute(query,val)
        
        result = bank_cur.fetchall()
        
        print(f"\nHi! {result[0][0]}, Hope you are having a nice day")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
    
    def Deposit(self,p):                                                       #Adds Money to account
        self.dep_amount = int(input("Please enter the amount to deposit: "))
        
        query = "Update Bank_Users set Balance = Balance + %s where Pin = %s"
        val = (self.dep_amount,p)
        
        bank_cur.execute(query,val)
        
        query = "Update Bank_Users set Balance = Balance + %s where User_id = 1"
        val = (self.dep_amount,)
        
        bank_db.commit()
        
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print(f"\n{self.dep_amount} Rs Deposited Successfully")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
    
    def WithDraw(self,p):                                                      #Deducts money from account
        self.with_amount = int(input("\nPlease enter the amount you want to withdraw: "))
        
        query = "Select Balance,First_Name from Bank_Users where Pin = %s"
        val = (p,)
        
        bank_cur.execute(query,val)
    
        result = bank_cur.fetchall()
        
        if result[0][0] >= self.with_amount:
            query = "Update Bank_Users set Balance = Balance - %s where Pin = %s"
            val = (self.with_amount,p)
            
            bank_cur.execute(query,val)
            
            bank_db.commit()
            
            print(f"\nHi! {result[0][1]}")
            print("\nMoney Withdarwn Successfully")
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
        else:
            print(f"\nHi! {result[0][1]}")
            print(f"\nYou don't have enough balance to withdarw {self.with_amount} Rs")
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            
    
    def PinChange(self,p):                                                      #Changes Pin
        self.new_pin = input("\nPlease enter new pin: ")
        
        query = "Update Bank_Users set Pin = %s where Pin = %s"
        val = (self.new_pin,p)
        
        bank_cur.execute(query,val)
        
        bank_db.commit()
        
        print("\nPin Changed Successfully")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
    
    
    def CardGenerator(self):  
        query = "Select Card_no from Bank_Users"
        
        bank_cur.execute(query)
        
        res = bank_cur.fetchall()
        
        n = 16
        self.card_no = "".join(ran.choices(s.digits, k = n))
        
        if self.card_no in res[0]:
            n = 16
            self.card_no = "".join(ran.choices(s.digits, k = n))
                  
        c = 0
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print("\nYour Card Number is: ",end = "")
        for i in self.card_no:
            c += 1 
            if c == 4:
                print(i,end = " ")
                c = 0
            else:
                print(i, end = "")
    
        
    def Loan(self):
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        self.loan_amount = int(input("\nPlease enter the loan amount: "))
        self.loan_duration = None
        self.total_loan = None
        
        query = "Select Balance from Bank_Users where User_id = 1"
        
        bank_cur.execute(query)
        
        result = bank_cur.fetchall()
         
        if self.loan_amount <= 500000 and result[0][0] > self.loan_amount:
            
            print("\nYou can repay the loan in 60 months (5 years) or less of your choice")
            
            self.loan_duration = int(input("\nPlease enter the no. of months in which you want repay the money: "))
            
            i = 5                                                    #interest(%)
            r = round(i/12/100,5)
            
            EMI = round(self.loan_amount * r * (1+r)**self.loan_duration / ((1+r)**self.loan_duration - 1))
            repay_amount = round(EMI * self.loan_duration)
            
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            
            print(f"\nLoan Amount = {self.loan_amount} Rs \nLoan Duration = {self.loan_duration} months \nInterest(%) = {i} %")
            print(f"Total Interest = {round(EMI*self.loan_duration - self.loan_amount)} Rs")
            print(f"EMI (Equated Monthly Installment): {EMI} Rs")
            print(f"Repay Amount = {repay_amount} Rs")
            
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            
            res = input("\nDo you want to confirm your loan(y/n): ")
            
            if res == 'y':
                con = input("\nDo you have account in our bank(y/n): ")
                if con == 'y':
                    print("\n-------------------------------------------------------------------------------------------------------------------------------")
                    pin = input("\nPlease enter your pin: ")
                    user.CheckPin(pin)
                    
                    print("\nYour loan is going to be in your account in a minute")
                    
                    query = "Update Bank_Users set Balance = Balance + %s where Pin = %s"
                    val = (self.loan_amount,pin)
                    
                    bank_cur.execute(query,val)
                    
                    query = "Update Bank_Users set Balance = Balance - %s where User_id = 1"
                    val = (self.loan_amount,)
                    
                    bank_cur.execute(query,val)
                    
                    query = "Select User_id from Bank_Users where Pin = %s"
                    val = (pin,)
                    
                    bank_cur.execute(query,val)
                    
                    result_id = bank_cur.fetchall()
                    result_id = result_id[0][0]
                    
                    
                    date = str(dt.datetime.now()).split()[0]
        
                    
                    query = "Insert into Loan_Users(User_id,Loan_approved,EMI,Total_repay_amount,Loan_issue_date,Loan_Period) Values (%s,%s,%s,%s,%s,%s)"
                    val = (result_id,self.loan_amount,EMI,repay_amount,date,self.loan_duration)
                    
                    bank_cur.execute(query,val)
                    
                    bank_db.commit()
                    
                    
                    
                    print("\nCongratulations! Loan Amount Successfully added to your account")
                    print("\nThank you! for choosing us, Please pay your loan on time to avoid additional penalty charges")
                    print("\n-------------------------------------------------------------------------------------------------------------------------------")
                    
                elif con == 'n':
                    print("\n-------------------------------------------------------------------------------------------------------------------------------")
                    acc_res = input("\nDo you want to open account in our bank(y/n): ")
                    if acc_res == 'y':
                        user.CreateUser()
                        
                        pin = input("\nPlease enter your pin: ")
                        user.CheckPin(pin)
                    
                        print("\nYour loan is going to be in your account in a minute")
                        
                    
                        query = "Update Bank_Users set Balance = Balance + %s where Pin = %s"
                        val = (self.loan_amount,pin)
                    
                        bank_cur.execute(query,val)
                        
                        
                        query = "Update Bank_Users set Balance = Balance - %s where User_id = 1"
                        val = (self.loan_amount,)
                        
                        bank_cur.execute(query,val)
                        
                        query = "Select User_id from Bank_Users where Pin = %s"
                        val = (pin,)
                    
                        bank_cur.execute(query,val)
                    
                        result_id = bank_cur.fetchall()
                        result_id = result_id[0][0]
                    
                        date = dt.datetime.now()
                        date = str(date).split()
                        date = date[0]
                    
                        query = "Insert into Loan_Users(User_id,Loan_approved,EMI,Total_repay_amount,Loan_issue_date,Loan_Period) Values (%s,%s,%s,%s,%s,%s)"
                        val = (result_id,self.loan_amount,EMI,repay_amount,date,self.loan_duration)
                    
                        bank_cur.execute(query,val)
                    
                        bank_db.commit()
                        
                        
                        print("\nCongratulations! Loan Amount Successfully added to your account")
                        print("\nThank you! for choosing us, Please pay your loan on time to avoid additional penalty charges")
                        print("\n-------------------------------------------------------------------------------------------------------------------------------")
                    
                    elif acc_res == 'n':
                        print("\nYou have to personally visit the bank to get the loan. \nThank you!")
                    
                    else:
                        print("\nIncorect Response ----- Please try again -------- Thank you!")
                        
                else:
                    print("\nIncorect Response ----- Please try again -------- Thank you!")
                
            elif res == 'n':
                print("\n-------------------------------------------------------------------------------------------------------------------------------")
                print("\nThank you for interacting with us.")
                print("\n-------------------------------------------------------------------------------------------------------------------------------")
                
            else:
                print("\n-------------------------------------------------------------------------------------------------------------------------------")
                print("\n                         Incorect Response ----- Please try again -------- Thank you!")
                print("\n-------------------------------------------------------------------------------------------------------------------------------")
        else:
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            print("\n                                                     NO LOANS AVAILABLE")
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            
    
    def Complaint(self):
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print("\n1.Bad customer service \n2.Loan issues \n3.Bad Service \n4.Other")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        self.res = int(input("\nPlease choose from above choices: "))
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        if self.res == 1:
            query = "Insert into Complaints (Complaint) values(%s)"
            val = ('Bad customer service',)
            
            bank_cur.execute(query,val)
            
            bank_db.commit()
            
            print("\nYour complaint is recorded")
            print("\nSorry for the inconvinience, we will work on your complaint")
        
        if self.res == 2:
            query = "Insert into Complaints (Complaint) values(%s)"
            val = ('Loan issues',)
            
            bank_cur.execute(query,val)
            
            bank_db.commit()
            
            print("\nYour complaint is recorded")
            print("\nSorry for the inconvinience, we will work on your complaint")
        
        if self.res == 3:
            query = "Insert into Complaints (Complaint) values(%s)"
            val = ('Bad Service',)
            
            bank_cur.execute(query,val)
            
            bank_db.commit()
            
            print("\nYour complaint is recorded")
            print("\nSorry for the inconvinience, we will work on your complaint")
            
        if self.res == 4:
            self.comp = input("\nPlease write your complaint as short as you can: ")
            
            query = "Insert into Complaints (Complaint) values(%s)"
            val = (self.comp,)
            
            bank_cur.execute(query,val)
            
            bank_db.commit()
            
            print("\nYour complaint is recorded")
            print("\nSorry for the inconvinience, we will work on your complaint")
            
            
    def CloseAccount(self):
        
        self.close_pin = input("\nPlease enter pin: ")
        
        query = "Select First_Name from Bank_Users where Pin = %s"
        val = (self.close_pin,)
        bank_cur.execute(query,val)
        
        result = bank_cur.fetchall()
        
        print(f"\nHi! {result[0][0]}\n")
        
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        self.last_res = input("\nAre you sure you want to close your account(y/n): ")
        
        if self.last_res == 'y':
            query = "Select User_id,Balance,Acc_Status from Bank_Users where Pin = %s"
            val = (self.close_pin,)
            
            bank_cur.execute(query,val)
            
            res_query1 = bank_cur.fetchall()
            
            query = "Select * from Loan_Users where User_id = %s"
            val = (res_query1[0][0],)
            
            bank_cur.execute(query,val)
            
            res_query2 = bank_cur.fetchall()
            
            if len(res_query2) == 0:
                
                if res_query1[0][1] > 0:
                    
                    print("\n-------------------------------------------------------------------------------------------------------------------------------")
                    print(f"\nYou need to withdraw all the amount you have in your account i.e {res_query1[0][1]} Rs")
                    
                    last_res1 = input("\nDo you want to continue(y/n): ")
                    
                    if last_res1 == 'y':
                        query = "Update Bank_Users set Balance = Balance - %s, Acc_Status = 'c' where pin = %s"
                        val = (res_query1[0][1],self.close_pin)
                        
                        bank_cur.execute(query,val)
                        
                        bank_db.commit()
                        
                        print("\n-------------------------------------------------------------------------------------------------------------------------------")
                        
                        print(f"\n{res_query1[0][1]} Rs withdrawn successfully")
                        
                        print("\n-------------------------------------------------------------------------------------------------------------------------------")
                        
                        print(f"\nThanks {result[0][0]}, for using our services")
                        
                        print("\n-------------------------------------------------------------------------------------------------------------------------------")
                        
                    elif last_res1 == 'n':
                        print("Looks like You changed your mind! Thats's great news for us!")
                    
                else:
                    print("OK")
            else:
                print("You have't repaid the loan yet. First you have to pay your loan and then you can access this service.")
                
        elif self.last_res == 'n':
            print("Nice")
        
        else:
            print("Invalid Response")
            
            
    def CloseAccountDB(self): 
        query = "Select * from Bank_Users where Acc_Status = 'c'"
        
        bank_cur.execute(query)
        
        result = bank_cur.fetchall()
        
        
        if len(result)!= 0: 
            for i in range (len(result)):
            
                date = str(dt.datetime.now()).split()[0]
            
                query = "Insert into Closed_Bank_Users(User_id,First_Name,Last_Name,Address,Mobile_No,Card_no,Pin,Balance,Opening_Date,Closed_Date,Acc_Status) Values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                val = (result[i][0],result[i][1],result[i][2],result[i][3],result[i][4],result[i][5],result[i][6],result[i][7],result[i][8],date,result[i][9])
                
                bank_cur.execute(query,val)
                
                query = "Delete from Bank_Users where pin = %s and Acc_Status = %s"
                val = (result[i][6],'c')
                    
                bank_cur.execute(query,val)
                
                bank_db.commit()
        else:
            pass
        
        
user = Bank()

print("\n-------------------------------------------------------------------------------------------------------------------------------")
print("\n------------------------------------------------- WELCOME TO PIE BANK OF INDIA ------------------------------------------------")
print("\n-------------------------------------------------------------------------------------------------------------------------------")

print("""\n          Bank created by Piyush Hatewar(Pie) himself. This Bank is one of the best Banks which is fully auomated.  \n""")


res = 'y'

while(res == 'y'):
    
    print("\n-------------------------------------------------------------------------------------------------------------------------------")
    print("\nServices Provided By Bank :")
    print("\n1.Loan Services \n2.Accessing Account \n3.Create Account \n4.Close Account \n5.Complaint ")
    print("\n(Note: Use Numbers as Input For Accessing Services)")
    print("\n-------------------------------------------------------------------------------------------------------------------------------")
    
    
    user_res = input("\nService Number: ")
    
    if user_res == '1':
        user.Loan()
    
    elif user_res == '2':
        print("\nServices: ")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print("\n1.Check Balance \n2.Deposite \n3.Withdaraw \n4.Pin Change ")
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        
        user_res1 = int(input("\nPlease Select Service: "))
        
        if user_res1 == 1:
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            pin = input("\nPlease enter pin: ")
            user.CheckBalance(pin)
        elif user_res1 == 2:
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            pin = input("\nPlease enter pin: ")
            user.Deposit(pin)
        elif user_res1 == 3:
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            pin = input("\nPlease enter pin: ")
            user.WithDraw(pin)
        elif user_res1 == 4:
            print("\n-------------------------------------------------------------------------------------------------------------------------------")
            pin = input("\nPlease enter pin: ")
            user.PinChange(pin)
        else:
            print("\nIncorect Response ----- Please try again -------- Thank you!")
    
    elif user_res == '3':
        user.CreateUser()
        
    elif user_res == '4':
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        user.CloseAccount()
    
    elif user_res == '5':
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        user.Complaint()
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
    
    user.CloseAccountDB()
    
    res = input("\nDo you want to continue(y/n): ")
    if res == 'n':
        print("\n-------------------------------------------------------------------------------------------------------------------------------")
        print("                                              Thank you for using our services")
        print("-------------------------------------------------------------------------------------------------------------------------------")

# user.AllExistingUser()

# user.CardGenerator()

# user.CloseAccountDB()