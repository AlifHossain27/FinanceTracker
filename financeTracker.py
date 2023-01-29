#!/usr/bin/env python3
import os
import sqlite3
import datetime
import functools
import operator
from simple_term_menu import TerminalMenu

class FinanceTracker():
    def __init__(self) -> None:
        pass

    def _conn_database(self):
        self.conn = sqlite3.connect("financeTracker.db")
        self.cur = self.conn.cursor()
        return self.cur

    def dailyExpenditure(self):
        # Categories List
        categoryList = ["Add Category", "Proceed"]
        # Getting user input
        date =  input("Enter the date (YYYY-MM-DD): ")
        earn = int(input("Amount of money earned: "))
        spent = int(input("Amount of money spent: "))
        saved = int(earn-spent)

        if date == "":
            date = datetime.date.today()
            # Inserting the Data into the database
            self._conn_database()
            self.cur.execute("INSERT INTO DailyExpense (date, earn, spent, saved) VALUES (?,?,?,?)", (date, earn, spent, saved))
            self.conn.commit()

            # Expense Category
            subMenuExit = False
            while subMenuExit == False:
                self._conn_database()
                self.cur.execute("SELECT DISTINCT category FROM ExpenseList")
                categories= self.cur.fetchall()
                for category in categories:
                    categoryList.append(functools.reduce(operator.add, (category)))
                categoryList = set(categoryList)
                categoryList = list(categoryList)
                categoryList.sort(key='Add Category'.__eq__)
                categoryList.sort(key='Proceed'.__eq__)
                new_options = categoryList
                subMenu = TerminalMenu(new_options, title = "Select Category")
                new_optionsIndex = subMenu.show()
                new_optionsChoice = new_options[new_optionsIndex]
                if new_optionsChoice == "Proceed":
                    subMenuExit = True
                    break
                if new_optionsChoice == "Add Category":
                    os.system("clear")
                    new_category = input("Enter a new Category: ")
                    desc = input("Enter a description: ")
                    amount = int(input("Enter the amount: "))
                    
                    self._conn_database()
                    self.cur.execute("INSERT INTO ExpenseList (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, new_category, desc, amount))
                    self.conn.commit()
                else:
                    os.system("clear")
                    new_category = new_optionsChoice
                    desc = input("Enter a description: ")
                    amount = int(input("Enter the amount: "))
                    
                    self._conn_database()
                    self.cur.execute("INSERT INTO ExpenseList (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, new_category, desc, amount))
                    self.conn.commit()

        else:
            # Inserting the Data into the database
            self._conn_database()
            self.cur.execute("INSERT INTO DailyExpense (date, earn, spent, saved) VALUES (?,?,?,?)", (date, earn, spent, saved))
            self.conn.commit()

            # Expense Category
            subMenuExit = False
            while subMenuExit == False:
                self._conn_database()
                self.cur.execute("SELECT DISTINCT category FROM ExpenseList")
                categories= self.cur.fetchall()
                for category in categories:
                    categoryList.append(functools.reduce(operator.add, (category)))
                categoryList = set(categoryList)
                categoryList = list(categoryList)
                categoryList.sort(key='Add Category'.__eq__)
                categoryList.sort(key='Proceed'.__eq__)
                new_options = categoryList
                subMenu = TerminalMenu(new_options, title = "Select Category")
                new_optionsIndex = subMenu.show()
                new_optionsChoice = new_options[new_optionsIndex]
                if new_optionsChoice == "Proceed":
                    subMenuExit = True
                    break
                if new_optionsChoice == "Add Category":
                    os.system("clear")
                    new_category = input("Enter a new Category: ")
                    desc = input("Enter a description: ")
                    amount = int(input("Enter the amount:"))
                    
                    self._conn_database()
                    self.cur.execute("INSERT INTO ExpenseList (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, new_category, desc, amount))
                    self.conn.commit()
                else:
                    os.system("clear")
                    new_category = new_optionsChoice
                    desc = input("Enter a description: ")
                    amount = int(input("Enter the amount: "))
                    self._conn_database()
                    self.cur.execute("INSERT INTO ExpenseList (date, category, description, amount) VALUES (?, ?, ?, ?)", (date, new_category, desc, amount))
                    self.conn.commit()
            

    def _stats(self):
        month = input("Enter the month (MM): ")
        year = input("Enter the year (YYYY): ")
        os.system("clear")
        print("=====Finance Stats=====")

        if month == "" or year == "":
            month = datetime.datetime.now().strftime('%m')
            year = datetime.datetime.now().strftime('%Y')
            self._conn_database()
            self.cur.execute("SELECT SUM(earn), SUM(spent), SUM(saved) FROM DailyExpense WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
            data = self.cur.fetchall()
            for i in data:
                print(f"Earning: {i[0]}")
                print(f"Spent: {i[1]}")
                print(f"Saving: {i[2]}")
            
            self.cur.execute("SELECT category, sum(amount) FROM ExpenseList WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? GROUP BY category", (month, year))
            expenseData = self.cur.fetchall()
            for expense in expenseData:
                print(f"Categoty: {expense[0]} -> Total: {expense[1]}")
            
        else:
            self._conn_database()
            self.cur.execute("SELECT SUM(earn), SUM(spent), SUM(saved) FROM DailyExpense WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?", (month, year))
            data = self.cur.fetchall()
            for i in data:
                print(f"Earning: {i[0]}")
                print(f"Spent: {i[1]}")
                print(f"Saving: {i[2]}")
            
            self.cur.execute("SELECT category, sum(amount) FROM ExpenseList WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ? GROUP BY category", (month, year))
            expenseData = self.cur.fetchall()
            for expense in expenseData:
                print(f"Categoty: {expense[0]}, Total: {expense[1]}")
    
    def _get_menu(self):
        options = ["Expenditure", "Stats","Quit"]
        quitting = False

        mainMenu = TerminalMenu(options, title = "=====Finance Tracker=====")

        while not quitting:
            optionsIndex = mainMenu.show()
            optionsChoice = options[optionsIndex]
            if optionsChoice == "Quit":
                self._conn_database()
                self.conn.close()
                quitting = True
            if optionsChoice == "Expenditure":
                os.system("clear")
                try:
                    self.dailyExpenditure()
                except Exception as e:
                    print(e)
                    #print("An Error occurred!!! USE THE CORRECT DATATYPE")
                    continue
            if optionsChoice == "Stats":
                os.system("clear")
                self._stats()
            else:
                pass
                

if __name__ == '__main__':
    FinanceTracker()._get_menu()