# TODO(Project 1): Implement Backend according to the requirements.
import os
from google.cloud import storage
from hashlib import blake2s
import base64
import io
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/project/flaskr/uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class Backend:
    def __init__(self):
        self.cur_client = storage.Client()
        self.content_bucket_name = 'fantasticwikicontent'
        self.user_bucket_name = 'fantasticuserinfo'
        self.content_bucket = self.cur_client.get_bucket(self.content_bucket_name)
        self.user_bucket = self.cur_client.get_bucket(self.user_bucket_name)
        
        
    def get_wiki_page(self, name):
        blobs = self.cur_client.list_blobs(self.content_bucket_name)
        
        for item in blobs:
            if item.name == name:
                return item
        return None

    def get_all_page_names(self):

        blobs = self.cur_client.list_blobs(self.content_bucket_name)
        files = [blob.name for blob in blobs]
        return files
        
    
    def upload(self, file):
        ALLOWED_EXTENSIONS = {'txt'}
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if allowed_file(file) and file != '':
            blob = self.content_bucket.blob(file)
            blob.upload_from_filename(file)
            return("Success")
            




    def sign_up(self, username, password):
        user_blob = self.user_bucket.get_blob(username)

        if (user_blob):
            return False
        
        user_blob = self.user_bucket.blob(username)
        hashed_password = blake2s((password + username + "fantastic").encode('ASCII'))
        user_blob.upload_from_string(hashed_password.hexdigest())
        return True

    def sign_in(self, username, password):
        user_blob = self.user_bucket.get_blob(username)

        if (user_blob):
            hashed_password = blake2s((password + username + "fantastic").encode('ASCII')).hexdigest()
            with user_blob.open() as f:
                correct_hash = f.read()
                return correct_hash == hashed_password
        else:
            return False

    def get_image(self):
        pass


