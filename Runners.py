# Frank Entriken
# entriken@chapman.edu
# CPSC 408 - Final, Runners.py

import csv
import random
import math
from faker import Faker
import mysql.connector
import pandas as pd
from pandas import DataFrame
import warnings

warnings.filterwarnings("ignore")

# print DataFrame containing the entire student table
def DisplayAll():
    mycursor = db.cursor()
    query = '''
            SELECT Runners.RunnerID, Runners.FirstName, Runners.LastName, Runners.Nationality, Runners.DOB, 100M.Time 100M, 200M.Time 200M, 400M.Time 400M, 800M.Time 800M, 1600M.Time 1600M
            FROM Runners
            LEFT JOIN 100M on Runners.RunnerID = 100M.RunnerID
            LEFT JOIN 200M on Runners.RunnerID = 200M.RunnerID
            LEFT JOIN 400M on Runners.RunnerID = 400M.RunnerID
            LEFT JOIN 800M on Runners.RunnerID = 800M.RunnerID
            LEFT JOIN 1600M on Runners.RunnerID = 1600M.RunnerID
            WHERE isDeleted != 1
            '''
    mycursor.execute(query)
    df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Nationality', 'DOB', '100M', '200M', '400M', '800M', '1600M'])

    # convert seconds to time
    n = len(df.index)
    count = -1
    for i in df:
        column = df[i]
        for item in column:
            count = count + 1
            if count < n*5:
                continue
            else:
                if item is None:
                    continue
                elif math.isnan(item):
                    continue

                arr = str(item).split(".")
                if len(str(int(arr[0]) % 60)) is 1:
                    end = "0" + str(round(item % 60, 2))
                elif len(arr[1]) is 1:
                    end = str(round(item % 60, 2)) + "0"
                else:
                    end = str(round(item % 60, 2))
                if len(end) is 4:
                    end = "0" + str(round(item % 60, 2)) + "0"
                column[count % n] = str(int(item//60)) + ":" + end
    print(df)
    mycursor.close()


def get_runners():
    mycursor = db.cursor()
    mycursor.execute("SELECT RunnerID FROM Runners")
    list = mycursor.fetchall()
    for i in range(len(list)):
        list[i] = str(list[i]).replace("(","")
        list[i] = str(list[i]).replace(",","")
        list[i] = str(list[i]).replace(")","")
        list[i] = int(list[i])
    return list


# make sure new student value is a string
def input_validation(message, desired_input, type):
    if type is 'string':
        while True:
            val = input(message)
            val = val.lower()
            for i in range(len(desired_input)):
                desired_input[i] = desired_input[i].lower()
            if val not in desired_input:
                print("Please enter an appropriate string")
                print("\n")
                continue
            else:
                return val

    if type is 'int':
        while True:
            try:
                val = int(input(message))
            except ValueError:
                print("Please enter an appropriate integer")
                print("\n")
                continue
            if val not in desired_input:
                print("Please enter an appropriate integer")
                print("\n")
                continue
            else:
                return val

    if type is 'date':
        days = []
        months = []
        for i in range(31):
            days.append(i+1)
        for i in range(12):
            months.append(i+1)
        while True:
            try:
                val = input(message)
                split = val.split('-')

                if len(split[0]) != 4:
                    print("Please enter a valid year")
                    print("\n")
                    continue
                if len(split[1]) != 2 or int(split[1]) not in months:
                    print("Please enter a valid month")
                    print("\n")
                    continue
                if len(split[2]) != 2 or int(split[2]) not in days:
                    print("Please enter a valid day")
                    print("\n")
                    continue
                return val
            except IndexError:
                print("Please enter a valid date")
                print("\n")
                continue

    if type is 'time':
        while True:
            val = input(message)
            if val is '':
                return val
            try:
                split = val.split(":")
                if len(split[0]) < 1 or len(split[0]) > 2 or len(split[1]) < 3 or len(split[1]) > 5:
                    print("Please enter a valid time1")
                    print("\n")
                    continue
                else:
                    return val
            except (ValueError, TypeError):
                print("Please enter a valid time2")
                print("\n")
                continue


def drop(table):
    mycursor = db.cursor()
    try:
        mycursor.execute("DROP TABLE " + table)
    except mysql.connector.errors.ProgrammingError:
        pass
    mycursor.close()


# creates tables for database schema
def create_tables():
    mycursor = db.cursor()
    # https://stackoverflow.com/questions/11100911/cant-drop-table-a-foreign-key-constraint-fails/11100985
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    mycursor.execute("DROP TABLE IF EXISTS Runners")
    mycursor.execute("DROP TABLE IF EXISTS 100M")
    mycursor.execute("DROP TABLE IF EXISTS 200M")
    mycursor.execute("DROP TABLE IF EXISTS 400M")
    mycursor.execute("DROP TABLE IF EXISTS 800M")
    mycursor.execute("DROP TABLE IF EXISTS 1600M")
    mycursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    mycursor.close()

    # -------------------- RUNNERS
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE Runners "
                     "(RunnerID INT NOT NULL AUTO_INCREMENT,"
                     "FirstName VARCHAR(50),"
                     "LastName VARCHAR(50),"
                     "Nationality VARCHAR(100),"
                     "DOB DATE,"
                     "Gender VARCHAR(10),"
                     "isDeleted INT DEFAULT 0,"
                     "PRIMARY KEY (RunnerID))"
                     )
    mycursor.close()

    # -------------------- 100M
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE 100M "
                     "(RunnerID INT UNIQUE AUTO_INCREMENT,"
                     "Time DOUBLE," # store as double and convert to time manually so i dont have to deal with datetime objects
                     "Date DATE,"
                     "Location VARCHAR(100),"
                     "FOREIGN KEY (RunnerID) REFERENCES Runners(RunnerID))"
                     )
    mycursor.close()

    # -------------------- 200M
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE 200M "
                     "(RunnerID INT UNIQUE AUTO_INCREMENT,"
                     "Time DOUBLE,"
                     "Date DATE,"
                     "Location VARCHAR(100),"
                     "FOREIGN KEY (RunnerID) REFERENCES Runners(RunnerID))"
                     )
    mycursor.close()

    # -------------------- 400M
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE 400M "
                     "(RunnerID INT UNIQUE AUTO_INCREMENT,"
                     "Time DOUBLE,"
                     "Date DATE,"
                     "Location VARCHAR(100),"
                     "FOREIGN KEY (RunnerID) REFERENCES Runners(RunnerID))"
                     )
    mycursor.close()

    # -------------------- 800M
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE 800M "
                     "(RunnerID INT UNIQUE AUTO_INCREMENT,"
                     "Time DOUBLE,"
                     "Date DATE,"
                     "Location VARCHAR(100),"
                     "FOREIGN KEY (RunnerID) REFERENCES Runners(RunnerID))"
                     )
    mycursor.close()

    # -------------------- 1600M
    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE 1600M "
                     "(RunnerID INT UNIQUE AUTO_INCREMENT,"
                     "Time DOUBLE,"
                     "Date DATE,"
                     "Location VARCHAR(100),"
                     "FOREIGN KEY (RunnerID) REFERENCES Runners(RunnerID))"
                     )
    mycursor.close()


# generates appropriately random data for the runners table
def gen_Runners(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        FirstName = fake.first_name()
        LastName = fake.last_name()
        Nationality = fake.country()
        DOB = fake.date()
        Gender = random.choice(["Male", "Female"])

        query = """INSERT INTO Runners (FirstName, LastName, Nationality, DOB, Gender) VALUES (%s, %s, %s, %s, %s)"""
        mycursor.execute(query, (FirstName, LastName, Nationality, DOB, Gender,))
    mycursor.close()
    db.commit()


# generates appropriately random data for the 100M table
def gen_100M(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        Time = random.choice([None, round(random.uniform(9.58, 12.00), 2)])
        if Time is None:
            Date = None
            Location = None
        else:
            Date = fake.date_between('-15y', 'today')
            Location = fake.city()

        query = """INSERT INTO 100M (Time, Date, Location) VALUES (%s, %s, %s)"""
        mycursor.execute(query, (Time, Date, Location,))
    mycursor.close()
    db.commit()


# generates appropriately random data for the 100M table
def gen_200M(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        Time = random.choice([None, round(random.uniform(19.12, 23.00), 2)])
        if Time is None:
            Date = None
            Location = None
        else:
            Date = fake.date_between('-15y', 'today')
            Location = fake.city()

        query = """INSERT INTO 200M (Time, Date, Location) VALUES (%s, %s, %s)"""
        mycursor.execute(query, (Time, Date, Location,))
    mycursor.close()
    db.commit()


# generates appropriately random data for the 100M table
def gen_400M(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        Time = random.choice([None, round(random.uniform(43.03, 50.00), 2)])
        if Time is None:
            Date = None
            Location = None
        else:
            Date = fake.date_between('-15y', 'today')
            Location = fake.city()

        query = """INSERT INTO 400M (Time, Date, Location) VALUES (%s, %s, %s)"""
        mycursor.execute(query, (Time, Date, Location,))
    mycursor.close()
    db.commit()


# generates appropriately random data for the 100M table
def gen_800M(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        Time = random.choice([None, round(random.uniform(100.91, 120.00), 2)])
        if Time is None:
            Date = None
            Location = None
        else:
            Date = fake.date_between('-15y', 'today')
            Location = fake.city()

        query = """INSERT INTO 800M (Time, Date, Location) VALUES (%s, %s, %s)"""
        mycursor.execute(query, (Time, Date, Location,))
    mycursor.close()
    db.commit()


# generates appropriately random data for the 100M table
def gen_1600M(n):
    fake = Faker()
    mycursor = db.cursor()
    for i in range(n):
        Time = random.choice([None, round(random.uniform(227.00, 270.00), 2)])
        if Time is None:
            Date = None
            Location = None
        else:
            Date = fake.date_between('-15y', 'today')
            Location = fake.city()

        query = """INSERT INTO 1600M (Time, Date, Location) VALUES (%s, %s, %s)"""
        mycursor.execute(query, (Time, Date, Location,))
    mycursor.close()
    db.commit()


def gen_data(n):
    gen_Runners(n)
    gen_100M(n)
    gen_200M(n)
    gen_400M(n)
    gen_800M(n)
    gen_1600M(n)


def AddRecord():
    mycursor = db.cursor()
    print("Please enter the following information, press return to leave NULL")
    uFirstName = input("FIRST NAME............")
    uLastName = input("Last NAME............")
    uNationality = input("Nationality............")
    uDOB = input_validation("Date of Birth............", None, "date")
    uGender = input("Gender............")

    query = '''
            INSERT INTO Runners (FirstName, LastName, Nationality, DOB, Gender)
            VALUES (%s, %s, %s, %s, %s);
            '''
    mycursor.execute(query, (uFirstName, uLastName, uNationality, uDOB, uGender))

    Events = ['100M', '200M', '400M', '800M', '1600M']
    for i in Events:
        uTime = input_validation(i + " Time (MM:SS.NN)........", None, "time")
        if uTime is not '':
            uDate = input_validation(i + " Date (YYYY-MM-DD)......", None, "date")
            uLocation = input(i + " Location............")

            time = uTime.split(":")
            if len(time[0]) is 1:
                time = float(time[0]) * 60 + float(time[1])
            elif len(time[0]) is 2:
                time = float(time[0][1]) * 60 + float(time[1])
            else:
                time = float(time[0])
                pass
            time = round(time, 2)
        else:
            uTime = None
            uDate = None
            uLocation = None
        query = "INSERT INTO %s (Time, Date, Location) VALUES (%s, %s, %s);" % (i, '%s', '%s', '%s',)
        mycursor.execute(query, (time, uDate, uLocation))

    mycursor.close()
    db.commit()


def df_times(df):
    if df.empty:
        pass
    else:
        count = -1
        for item in df['Time']:
            count = count + 1
            arr = str(item).split(".")
            if len(str(int(arr[0]) % 60)) is 1:
                end = "0" + str(round(item % 60, 2))
            elif len(arr[1]) is 1:
                end = str(round(item % 60, 2)) + "0"
            else:
                end = str(round(item % 60, 2))
            if len(end) is 4:
                end = "0" + str(round(item % 60, 2)) + "0"
            df['Time'][count] = str(int(item//60)) + ":" + end
        print(df)


def Query():
    DisplayAll()
    print("\n")
    mycursor = db.cursor()
    print("| 1. Display all data from RunnerID")
    print("| 2. Display runners from first name")
    print("| 3. Display runners from last name")
    print("| 4. Display all data where time is faster than given for an event")
    print("| 5. Display all data where time is slower than given for an event")
    print("| 6. Display all data where time is equal to given for an event")
    inp = input_validation("| ... ", [1, 2, 3, 4, 5, 6], "int")
    print("\n")

    if inp is 1:
        var = input_validation("Enter the RunnerID...", get_runners(), "int")
        print("\n")
        mycursor.execute("SELECT RunnerID, FirstName, LastName, Nationality, DOB, Gender FROM Runners WHERE RunnerID = %s" % var)
        df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Nationality', 'DOB', 'Gender'])
        print(df)
        print("\n")

        Events = ['100M', '200M', '400M', '800M', '1600M']
        for i in Events:
            mycursor.execute("SELECT * FROM %s WHERE RunnerID = %s AND %s.Time IS NOT NULL" % (i, var, i,))
            df = DataFrame(mycursor, columns=['RunnerID', 'Time', 'Date', 'Location'])
            if df.empty:
                pass
            else:
                print("-------------------------------------------------- " + i)
                df_times(df)
                print("\n")

    elif inp is 2:
        var = input("Enter a first name...")
        print("\n")
        mycursor.execute("SELECT RunnerID, FirstName, LastName, Nationality, DOB, Gender FROM Runners WHERE FirstName = '%s'" % var)
        df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Nationality', 'DOB', 'Gender'])
        if df.empty:
            print("No results using first name, " + var)
        else:
            print(df)

    elif inp is 3:
        var = input("Enter a last name...")
        print("\n")
        mycursor.execute("SELECT RunnerID, FirstName, LastName, Nationality, DOB, Gender FROM Runners WHERE LastName = '%s'" % var)
        df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Nationality', 'DOB', 'Gender'])
        if df.empty:
            print("No results using last name, " + var)
        else:
            print(df.to_string(index=False))

    elif inp is 4 or 5 or 6:
        print("Choose the event you would like to query")
        print("| 1. 100M")
        print("| 2. 200M")
        print("| 3. 400M")
        print("| 4. 800M")
        print("| 5. 1600M")
        num = input_validation("| ... ", [1, 2, 3, 4, 5], "int")
        print("\n")

        if num is 1:
            table = "100M"
        if num is 2:
            table = "200M"
        if num is 3:
            table = "400M"
        if num is 4:
            table = "800M"
        if num is 5:
            table = "1600M"

        if inp is 4:
            time1 = input_validation("You want to see times faster than (MM:SS.NN or SS.NN)...", None, "time")
            message = "There are no times faster than " + time1 + " for the " + table
            op = "<"
        if inp is 5:
            time1 = input_validation("You want to see times slower than (MM:SS.NN or SS.NN)...", None, "time")
            message = "There are no times slower than " + time1 + " for the " + table
            op = ">"
        if inp is 6:
            time1 = input_validation("You want to see times equal to (MM:SS.NN or SS.NN)...", None, "time")
            message = "There are no times equal to " + time1 + " for the " + table
            op = "="

        time = time1.split(":")
        if len(time[0]) is 1:
            time = float(time[0]) * 60 + float(time[1])
        elif len(time[0]) is 2:
            time = float(time[0][1]) * 60 + float(time[1])
        else:
            time = float(time[0])
            pass
        time = round(time, 2)
        query = '''
                SELECT Runners.RunnerID, FirstName, LastName, %s.Time, %s.Date, %s.Location
                FROM %s
                INNER JOIN Runners on %s.RunnerID = Runners.RunnerID
                WHERE Time %s %s
                ORDER BY Time
                ''' % (table, table, table, table, table, op, time,)
        mycursor.execute(query)
        df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Time', 'Date', 'Location'])
        if df.empty:
            print("\n")
            print(message)
        else:
            print("\n")
            df_times(df)


def Update():
    DisplayAll()
    print("\n")
    idd = input_validation("Enter the RunnerID of the record you would like to update...", get_runners(), "int")

    print("What table would you like to update from?")
    print("| 1. Runners")
    print("| 2. 100M")
    print("| 3. 200M")
    print("| 4. 400M")
    print("| 5. 800M")
    print("| 6. 1600M")
    num = input_validation("| ... ", [1, 2, 3, 4, 5, 6], "int")
    print("\n")

    if num is 1:
        table = "Runners"
    if num is 2:
        table = "100M"
    if num is 3:
        table = "200M"
    if num is 4:
        table = "400M"
    if num is 5:
        table = "800M"
    if num is 6:
        table = "1600M"

    if table == "Runners":
        headers = ['RunnerID', 'FirstName', 'LastName', 'Nationality', 'DOB', 'Gender']
        valid = ['FirstName', 'LastName', 'Nationality', 'DOB', 'Gender']
        column_in = "Enter the column you would like to update (FirstName, LastName, Nationality, Date, Gender)..."
        mycursor = db.cursor()
        query = "SELECT RunnerID, FirstName, LastName, Nationality, DOB, Gender FROM Runners WHERE RunnerID = %s" % idd
        mycursor.execute(query)
        df = DataFrame(mycursor, columns=headers)

    else:
        headers = ['RunnerID', 'Time', 'Date', 'Location']
        valid = ['Time', 'Date', 'Location']
        column_in = "Enter the column you would like to update (Time, Date, Location)..."
        mycursor = db.cursor()
        query = "SELECT * FROM %s WHERE RunnerID = %s AND %s.Time IS NOT NULL" % (table, idd, table,)
        mycursor.execute(query)
        df = DataFrame(mycursor, columns=headers)

    if df.empty:
        print("There is no recorded time, would you like to create a record for the " + table + "?")
        print("| 1. Yes")
        print("| 2. No, exit")
        inp = input_validation("| ... ", [1, 2], "int")

        if inp is 1:
            uTime = input_validation(table + " Time (MM:SS.NN)........", None, "time")
            time = uTime.split(":")
            if len(time[0]) is 1:
                time = float(time[0]) * 60 + float(time[1])
            elif len(time[0]) is 2:
                time = float(time[0][1]) * 60 + float(time[1])
            else:
                time = float(time[0])
                pass
            time = round(time, 2)
            uTime = time
            if uTime is not '':
                uDate = input_validation(table + " Date (YYYY-MM-DD)......", None, "date")
                uLocation = input(table + " Location............")
            else:
                uTime = None
                uDate = None
                uLocation = None

            query = "UPDATE %s SET Time = '%s', Date = '%s', Location = '%s' WHERE RunnerID = %s" % (table, uTime, uDate, uLocation, idd,)
            mycursor.execute(query)

            mycursor.execute("SELECT * FROM %s WHERE RunnerID = %s AND %s.Time IS NOT NULL" % (table, idd, table,))
            df = DataFrame(mycursor, columns=headers)
            print("\n")
            print(df)

            mycursor.close()
            db.commit()

        if inp is 2:
            pass

    else:
        print(df)
        print("\n")
        while(True):
            column = input(column_in)
            if column not in valid:
                print("Please enter a valid column with appropriate capitalization")
                print("\n")
                continue
            else:
                break
        value = input("Enter the new value...")
        mycursor.execute("UPDATE %s SET %s = '%s' WHERE RunnerID = %s" % (table, column, value, idd,))
        print("\n")
        print("Updated row: ")
        mycursor.execute(query)
        df = DataFrame(mycursor, columns=headers)
        if table == "Runners":
            print("\n")
            print(df)
        else:
            df_times(df)
        mycursor.close()
        db.commit()


def Analysis():
    print("| 1. 100M")
    print("| 2. 200M")
    print("| 3. 400M")
    print("| 4. 800M")
    print("| 5. 1600M")
    inp = input_validation("| ... ", [1, 2, 3, 4, 5], "int")
    print("\n")

    if inp is 1:
        table = "100M"
    if inp is 2:
        table = "200M"
    if inp is 3:
        table = "400M"
    if inp is 4:
        table = "800M"
    if inp is 5:
        table = "1600M"

    mycursor = db.cursor()
    query = """
            SELECT Runners.RunnerID, Runners.FirstName, Runners.LastName, %s.Time, %s.Time, %s.Time
            FROM %s
            INNER JOIN Runners on Runners.RunnerID = %s.RunnerID
            WHERE %s.Time IS NOT NULL
            ORDER BY Time
            """ % (table, table, table, table, table, table,)
    mycursor.execute(query)
    df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Time', 'Score', "Difference",])
    count = -1
    record = 0
    for item in df['Score']:
        count = count + 1

        if count is 0:
            record = item
        arr = str(item).split(".")
        if len(str(int(arr[0]) % 60)) is 1:
            end = "0" + str(round(item % 60, 2))
        elif len(arr[1]) is 1:
            end = str(round(item % 60, 2)) + "0"
        else:
            end = str(round(item % 60, 2))
        if len(end) is 4:
            end = "0" + str(round(item % 60, 2)) + "0"
        df['Time'][count] = str(int(item//60)) + ":" + end
        percentage = round(((record / item) * 100.00), 2)
        df['Score'][count] = str(percentage) + "%"
        df['Difference'][count] = "-" + str(round((100 - percentage), 2)) + "%"
    print(df)
    mycursor.close()


def Events():
    print("| 1. 100M")
    print("| 2. 200M")
    print("| 3. 400M")
    print("| 4. 800M")
    print("| 5. 1600M")
    inp = input_validation("| ... ", [1, 2, 3, 4, 5], "int")
    print("\n")

    if inp is 1:
        table = "100M"
    if inp is 2:
        table = "200M"
    if inp is 3:
        table = "400M"
    if inp is 4:
        table = "800M"
    if inp is 5:
        table = "1600M"

    mycursor = db.cursor()
    query = """
            SELECT Runners.RunnerID, Runners.FirstName, Runners.LastName, %s.Time, %s.Date, %s.Location
            FROM %s
            INNER JOIN Runners on Runners.RunnerID = %s.RunnerID
            WHERE %s.Time IS NOT NULL
            ORDER BY Time
            """ % (table, table, table, table, table, table,)
    mycursor.execute(query)
    df = DataFrame(mycursor, columns=['RunnerID', 'FirstName', 'LastName', 'Time', 'Date', 'Location'])
    count = -1
    for item in df['Time']:
        count = count + 1
        arr = str(item).split(".")
        if len(str(int(arr[0]) % 60)) is 1:
            end = "0" + str(round(item % 60, 2))
        elif len(arr[1]) is 1:
            end = str(round(item % 60, 2)) + "0"
        else:
            end = str(round(item % 60, 2))
        if len(end) is 4:
            end = "0" + str(round(item % 60, 2)) + "0"
        df['Time'][count] = str(int(item//60)) + ":" + end
    print(df)
    mycursor.close()


def Delete():
    DisplayAll()
    print("\n")
    mycursor = db.cursor()
    idd = input_validation("Enter the RunnerID that you would like to delete...", get_runners(), "int")
    mycursor.execute("UPDATE Runners SET isDeleted = 1 WHERE RunnerID = %s" % idd)
    Events = ['100M', '200M', '400M', '800M', '1600M']
    for i in Events:
        mycursor.execute("DELETE FROM %s WHERE RunnerID = %s" % (i, idd,))
    db.commit()


def csv():
    mycursor = db.cursor()
    query = '''
                SELECT R.RunnerID, R.FirstName, R.LastName, R.Nationality, R.DOB, R.Gender, R.isDeleted,
                       100M.Time, 100M.Date, 100M.Location,
                       200M.Time, 200M.Date, 200M.Location,
                       400M.Time, 400M.Date, 400M.Location,
                       800M.Time, 800M.Date, 800M.Location,
                       1600M.Time, 1600M.Date, 1600M.Location
                FROM Runners R
                INNER JOIN 100M on R.RunnerID = 100M.RunnerID
                INNER JOIN 200M on R.RunnerID = 200M.RunnerID
                INNER JOIN 400M on R.RunnerID = 400M.RunnerID
                INNER JOIN 800M on R.RunnerID = 800M.RunnerID
                INNER JOIN 1600M on R.RunnerID = 1600M.RunnerID
                '''
    mycursor.execute(query)
    headers = ['RunnerID', 'FirstName', 'LastName', 'Location', 'DOB', 'Gender', 'isDeleted', '100M_Time', '100M_Date', '100M_Location', '200M_Time', '200M_Date', '200M_Location', '400M_Time', '400M_Date', '400M_Location', '800M_Time', '800M_Date', '800M_Location', '1600M_Time', '1600M_Date', '1600M_Location']
    df = DataFrame(mycursor, columns=headers)
    df.to_csv(r'Runners.csv', index = False, header=True)
    print("All data has been exported to a csv in this directory named Runners.csv")


def menu():
    # https://thispointer.com/python-pandas-how-to-display-full-dataframe-i-e-print-all-rows-columns-without-truncation/
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    while(True):
        print("Enter the number of the option you would like to choose...")
        print("| 1. Display")
        print("| 2. Events")
        print("| 3. Analysis")
        print("| 4. Create")
        print("| 5. Update")
        print("| 6. Query")
        print("| 7. Delete")
        print("| 8. CSV")
        print("| 9. Exit")

        try:
            x = input_validation("| ... ", [1, 2, 3, 4, 5, 6, 7, 8, 9], "int")
            print("\n")
        except ValueError:
            print("\n")
            continue

        if x is 1:
            DisplayAll()

        elif x is 2:
            Events()

        elif x is 3:
            Analysis()

        elif x is 4:
            AddRecord()

        elif x is 5:
            Update()

        elif x is 6:
            Query()

        elif x is 7:
            Delete()

        elif x is 8:
            csv()

        elif x is 9:
            break

        print("\n")


# main
db = mysql.connector.connect(
    host="34.94.182.22",
    user="entriken@chapman.edu",
    passwd="FooBar!@#$",
    database="entriken_db"
)

n = 50
cursor = db.cursor()
create_tables()
gen_data(n)
menu()
