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
CORS(app, resources={r"*": {"origins": "*"}})
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
    return jsonify(contacts_list)

@app.route('/contacts/<int:id>')
def show_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.serialize())

#create a new contact
@app.route('/contacts', methods=['POST'])
def create_contact():
    name = request.json['name']
    phone = request.json['phone']
    email = request.json['email']
    avatar = request.json['avatar']

    contact = Contact(name, phone, email, avatar)
    contact.insert()

    return jsonify(contact.serialize()), 201

#update a contact
@app.route('/contacts/<int:id>', methods=['PATCH'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)

    name = request.json['name']
    phone = request.json['phone']
    email = request.json['email']
    avatar = request.json['avatar']

    contact.name = name
    contact.phone = phone
    contact.email = email
    contact.avatar = avatar

    contact.update()

    return jsonify(contact.serialize())

#delete a contact
@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    contact.delete()

    return jsonify(contact.serialize())

# search for a contact
@app.route('/contacts/search', methods=['GET'])
def search_contact():
    search = request.args.get('q')
    contacts = Contact.query.filter(Contact.name.contains(search)).all()
    return jsonify([contact.serialize() for contact in contacts])

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

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8282)
    