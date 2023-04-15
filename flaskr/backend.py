"""Provides interface for google cloud storage buckets."""
import os
import glob
import zipfile
from hashlib import blake2s
from google.cloud import storage
from flask import Flask, request
from pathlib import Path
import requests
import math
from io import BytesIO


UPLOAD_FOLDER = './temp_files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Backend:
    """Provides interface for google cloud storage buckets."""

    def __init__(self, storage_client=storage.Client()):
        self.cur_client = storage_client
        self.content_bucket_name = 'fantasticwikicontent'
        self.user_bucket_name = 'fantasticuserinfo'
        self.content_bucket = self.cur_client.get_bucket(
            self.content_bucket_name)
        self.user_bucket = self.cur_client.get_bucket(self.user_bucket_name)
        self.character_bucket = self.cur_client.get_bucket('fantastic_starwars_characters')
        self.character_list = []

    def get_wiki_page(self, name):
        """Provides the page blob of a page from the name."""
        blobs = self.cur_client.list_blobs(self.content_bucket_name)

        for item in blobs:
            if item.name == name:
                return item
        return None

    def get_all_page_names(self):
        """Provides a list of all wiki pages in the database"""
        blobs = self.cur_client.list_blobs(self.content_bucket_name)
        other_blobs = self.cur_client.list_blobs(self.content_bucket_name)
        files = [blob.name for blob in blobs]
        file_names = [Path(blob.name).stem for blob in other_blobs]
        return files, file_names

    def upload(self, file_name, file_obj):
        """Uploads a file object to the database"""
        ALLOWED_EXTENSIONS = {'md', 'jpg', 'png', 'gif', 'jpeg'}

        # Function to check file format
        def allowed_file(filename):
            return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        # Function to remove all files from temp
        def clean_temp():
            temp_files = glob.glob("./temp_files/*")
            for file in temp_files:
                os.remove(file)

        # Fails if no file submitted
        if file_name == '':
            return "Failure"

        # Extracts zip and puts each file in bucket if format for all is correct
        elif file_name.rsplit('.', 1)[1].lower() == 'zip':
            all_allowed = True

            with zipfile.ZipFile(file_obj, "r") as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)

            for file_name in os.listdir(UPLOAD_FOLDER):
                if not allowed_file(file_name) or file_name == '':
                    all_allowed = False

            if all_allowed is not False:
                for file_name in os.listdir(UPLOAD_FOLDER):
                    blob = self.content_bucket.blob(file_name)
                    blob.upload_from_filename(UPLOAD_FOLDER + file_name)

                clean_temp()
                return "Success"

            elif all_allowed is False:
                clean_temp()
                return "Failure"

        # Accepts file with right format and puts in bucket
        else:
            if allowed_file(file_name):
                file_obj.save(
                    os.path.join(app.config['UPLOAD_FOLDER'], file_name))
                blob = self.content_bucket.blob(file_name)
                blob.upload_from_filename(UPLOAD_FOLDER + file_name)

                clean_temp()
                return "Success"

            else:
                clean_temp()
                return "Failure"

    def sign_up(self, username, password):
        """Adds user data if it does not exist along with a hashed password."""
        # We first check if a blob already exists with that name
        user_blob = self.user_bucket.get_blob(username)

        if user_blob:
            # If there is then we can't add the new user
            return False

        user_blob = self.user_bucket.blob(username)
        # We create a blob with our hashed password
        hashed_password = blake2s(
            (password + username + "fantastic").encode('ASCII'))
        user_blob.upload_from_string(hashed_password.hexdigest())
        return True

    def sign_in(self, username, password):
        """Checks if a password, when hashed, matches the password in the user bucket."""
        # We first check if a blob already exists with that name
        user_blob = self.user_bucket.get_blob(username)

        if user_blob:
            hashed_password = blake2s(
                (password + username +
                 "fantastic").encode('ASCII')).hexdigest()
            with user_blob.open() as file:
                correct_hash = file.read()
                # We compare the hash in the database with the hash of the password attempt
                return correct_hash == hashed_password
        else:
            # If the user doesn't exist then we can't log the user in
            return False

    def get_image(self, name):
        """Provides an image from the database"""
        # get image from gcs bucket
        # download to static folder
        # return url to be used in jinja template
        bucket = self.content_bucket
        blob = bucket.blob(name)
        blob.download_to_filename("flaskr/static/" + name)
        return "../static/" + name


    def get_character_names(self):
        character_names = [Path(blob.name).stem for blob in self.character_bucket.list_blobs() if blob.name.endswith(("png", "jpg", "jpeg"))]
        return character_names

    def request_maker(self):
        # Calls the API one time so that we can get every character in the Star Wars universe
        if self.character_list == []:
            data_list = []
            for number in range(1, 10):
                response = requests.get(f"https://swapi.dev/api/people/?page={number}")
                if response.status_code != 200:
                    continue
                else:
                    #Entire page
                    data = response.json()
                    #List of dictionaries for each character - only one page
                    filtered_data = data["results"]
                    data_list.append(filtered_data)

            self.character_list = data_list
            
            return self.character_list
        else:
            #IF the API has already been called, we can just access the information directly, no need to use the API again.
            return self.character_list
    def get_character_image(self,name):

        blob = self.character_bucket.get_blob(name+str('.png'))
        if blob is None:
            print('empty')
            return BytesIO()
        with blob.open('rb') as f:
            output = f.read()
            return BytesIO(output)

        
        

        
       
   


