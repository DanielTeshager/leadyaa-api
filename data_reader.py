import csv
import os
from models import Contact, db
#read csv file and insert data into databasejuu
def read_csv_file(file_name):
    with open(file_name,'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
           contact = Contact(row[0], row[1])
           contact.insert()
           print(contact.name)

read_csv_file('all_data.csv')