from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import time
from models import setup_db, Contact


app = Flask(__name__)
#CORS allow origin from www.leadyaa.com only
CORS(app, resources={r"*": {"origins": "https://www.leadyaa.com"}})
setup_db(app)

@app.route('/')
def show_all():
    time.sleep(1)
    contacts = Contact.query.order_by(Contact.id).all()
    # generate 3 random numbers between 1 and the number of contacts
    random_numbers = random.sample(range(1, len(contacts)), 3)
    # create a list of contacts
    contacts_list = []
    for number in random_numbers:
        contacts_list.append(contacts[number].format())
    # return the list of contacts
    return jsonify({
        'success': True,
        'contacts': contacts_list
    }), 200

@app.route('/contacts/search', methods=['GET'])
def search_contact():
    search = request.args.get('q')
    # search for a contact case insensitive
    contacts = Contact.query.filter(Contact.name.ilike(f'%{search}%')).all()
    # return not found if no contacts are found
    if not contacts:
        return jsonify({
            'success': False,
            'message': 'No contacts found'
        }), 404
    else:
        # return contacts
        return jsonify({
            'success': True,
            'data': [contact.serialize() for contact in contacts],
            'message': 'Contacts found'
        }), 200


@app.errorhandler(404)
def page_not_found(e):
    # your processing here
    return jsonify({
        'success': False,
        'message': 'Not found'
    }), 404
