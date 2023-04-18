"""Provides interface for google cloud storage buckets."""
import os
import glob
import zipfile
from hashlib import blake2s
from google.cloud import storage
from flask import Flask, request
from pathlib import Path

UPLOAD_FOLDER = './temp_files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check file format
def allowed_file(filename, extensions):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in extensions

# Function to remove all files from temp
def clean_temp():
    temp_files = glob.glob("./temp_files/*")
    for file in temp_files:
        os.remove(file)

class Backend:
    """Provides interface for google cloud storage buckets."""

    def __init__(self, storage_client=storage.Client()):
        self.cur_client = storage_client
        self.content_bucket_name = 'fantasticwikicontent'
        self.user_bucket_name = 'fantasticuserinfo'
        self.content_bucket = self.cur_client.bucket(self.content_bucket_name)
        self.user_bucket = self.cur_client.bucket(self.user_bucket_name)
        self.userphoto_bucket_name = 'fantasticuserphotos'
        self.userbio_bucket_name = 'fantasticuserbio'
        self.content_bucket = self.cur_client.bucket(self.content_bucket_name)
        self.user_bucket = self.cur_client.bucket(self.user_bucket_name)
        self.userphoto_bucket = self.cur_client.get_bucket(self.userphoto_bucket_name)
        self.userbio_bucket = self.cur_client.get_bucket(self.userbio_bucket_name)

        

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

    def get_users(self):
        blobs = self.cur_client.list_blobs(self.user_bucket_name)
        users = [blob.name for blob in blobs]
        return users

    def get_profile_pic(self, username):
        blobs = self.cur_client.list_blobs(self.userphoto_bucket_name)
        for item in blobs:
            if username + "_profilepic.jpg" == item.name:
                return "https://storage.cloud.google.com/fantasticuserphotos/" + username + "_profilepic"
        
        return "https://storage.cloud.google.com/fantasticuserphotos/default.png"

    def get_banner_pic(self, username):
        blobs = self.cur_client.list_blobs(self.userphoto_bucket_name)
        for item in blobs:
            if username + "_bannerpic.jpg" == item.name:
                return "https://storage.cloud.google.com/fantasticuserphotos/" + username + "_bannerpic"
        
        return "https://storage.cloud.google.com/fantasticuserphotos/default_banner.jpg"

    def get_bio(self, username):
        blobs = self.cur_client.list_blobs(self.userbio_bucket_name)
        for item in blobs:
            if item.name == username:
                return item.download_as_string().decode('utf-8')
        
        return "No bio"


    def upload(self, file_name, file_obj):
        """Uploads a file object to the database"""
        ALLOWED_EXTENSIONS = {'md', 'jpg', 'png', 'gif', 'jpeg'}

        # Fails if no file submitted
        if file_name == '':
            return "Failure"

        # Extracts zip and puts each file in bucket if format for all is correct
        elif file_name.rsplit('.', 1)[1].lower() == 'zip':
            all_allowed = True

            with zipfile.ZipFile(file_obj, "r") as zip_ref:
                zip_ref.extractall(UPLOAD_FOLDER)

            for file_name in os.listdir(UPLOAD_FOLDER):
                if not allowed_file(file_name, ALLOWED_EXTENSIONS) or file_name == '':
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
            if allowed_file(file_name, ALLOWED_EXTENSIONS):
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

    def change_profile(self, username, new_pass, pic_file_name, pic_file_obj, banner_file_name, banner_file_obj, bio):
        ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpeg'}

        if pic_file_name != "" and not allowed_file(pic_file_name, ALLOWED_EXTENSIONS):
            return "Failure"
        
        if banner_file_name != "" and not allowed_file(banner_file_name, ALLOWED_EXTENSIONS):
            return "Failure"

        if new_pass != "":
            user_blob = self.user_bucket.blob(username)
            hashed_password = blake2s(
                (new_pass + username + "fantastic").encode('ASCII'))
            user_blob.upload_from_string(hashed_password.hexdigest())

        if pic_file_name != "":
            pic_file_obj.save(
                os.path.join(app.config['UPLOAD_FOLDER'], pic_file_name))

            blob = self.userphoto_bucket.blob(username + "_profilepic")
            blob.upload_from_filename(UPLOAD_FOLDER + pic_file_name)

            clean_temp()

        if banner_file_name != "":
            banner_file_obj.save(
                os.path.join(app.config['UPLOAD_FOLDER'], banner_file_name))

            blob = self.userphoto_bucket.blob(username + "_bannerpic")
            blob.upload_from_filename(UPLOAD_FOLDER + banner_file_name)

            clean_temp()


        if bio != "":
            blob = self.userbio_bucket.blob(username)
            blob.upload_from_string(bio)

        return "Success"



        

        
            
        


            


