from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from database.models import setup_db, Contact, db
from unittest import TestCase

#create test case
class TestApp(TestCase):
    def setUp(self):
        #create the flask app
        self.app = Flask(__name__)
        setup_db(self.app)
        self.client = self.app.test_client()
        self.api = Api(self.app)
        CORS(self.app)

    def tearDown(self):
        pass

    def test_show_all(self):
        #create a contact
        contact = Contact(name="test", phone="123", email="dani.d@gmail.com", avatar="test")
        contact.insert()

        #get all contacts
        response = self.client.get('/contacts')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [contact.serialize()])

    def test_create_contact(self):
        #create a contact
        response = self.client.post('/contacts', json={
            "name": "test",
            "phone": "123",
            "email": "dan.g@gmail.com",
            "avatar": "test"
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            "name": "test",
            "phone": "123",
            "email": "dan.g@gmail.com",
            "avatar": "test"
        })

    def test_patch_contact(self):
        #create a client
        contact = Contact(name="test", phone="123", email="" , avatar="test")
        #patch a contact
        response = self.client.patch('/contacts/1', json={
            "name": "test",
            "phone": "123",
            "email": "jimy@mail.com",
            "avatar": "test"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "name": "test",
            "phone": "123",
            "email": "jimy@mail.com",
            "avatar": "test"
        })

    def test_delete_contact(self):
        #create a client    
       # contact = Contact(name="test", phone="123", email="" , avatar="test")
        #delete a contact
        response = self.client.delete('/contacts/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "name": "test",
            "phone": "123",
            "email": "" ,
            "avatar": "test"
        })


