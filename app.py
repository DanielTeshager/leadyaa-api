import os
import re
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import csv
import time
from sqlalchemy.sql.operators import endswith_op
from models import setup_db, Contact


app = Flask(__name__)
#add CORS
#cors allow origin from www.leadyaa.com
CORS(app)
setup_db(app)

@app.route('/')
# allow CORS
def show_all():
    time.sleep(1)
    # return 4 random contacts
    contacts = Contact.query.order_by(Contact.id).all()
    # generate 3 random numbers between 1 and the number of contacts
    random_numbers = random.sample(range(1, len(contacts)), 3)
    # create a list of contacts
    contacts_list = []
    for number in random_numbers:
        contacts_list.append(contacts[number].format())
    # add correct headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://www.leadyaa.com'
    }
    # return the list of contacts
    return jsonify({
        'success': True,
        'contacts': contacts_list
    }), 200, headers




# search for a contact
#cors allow origin from www.leadyaa.com
@app.after_request
@app.route('/contacts/search', methods=['GET'])
def search_contact():
    search = request.args.get('q')
    contacts = Contact.query.filter(Contact.name.contains(search)).all()
    # return not found if no contacts are found
    if not contacts:
        return jsonify({
            'success': False,
            'message': 'No contacts found'
        }), 404
    else:
        # return contacts
        headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://www.leadyaa.com'
        }
        return jsonify({
            'success': True,
            'data': [contact.serialize() for contact in contacts],
            'message': 'Contacts found'
        }), 200, headers


#only uncomment this if you want to insert new data to db

# def read_csv_file(file_name):
#     with open(file_name,'r') as csv_file:
#         # csv_reader = csv.reader(csv_file, delimiter=',')
#         csv_reader = csv.DictReader(csv_file, delimiter=',')
#         for row in csv_reader:
#            contact = Contact(row['name'], row['branch'], row['city'], row['kifle_ketema'], row['direction'], row['building'], row['flat'], row['phone'])
#            contact.insert()
#            print(contact.name)

# read_csv_file('address_data.csv')
# sys.exit(0)
