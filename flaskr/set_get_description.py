from flaskr.backend import Backend
from flask import Flask
from werkzeug.datastructures import FileStorage
import os

UPLOAD_FOLDER = './temp_files/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def set_description(description, filename):
    '''
    Params:
    Description- str, description of uploaded wiki
    Filename- str, filename of uploaded wiki
    create txt file with original filename + _description
    add description to txt file
    close file
    upload file to gcs bucket
    '''
    filename, ext = filename.split('.')
    new_filename = filename + "_description.md"
    blob_filename = filename + "/description.md"
    file = open(new_filename, "w")
    file.write(description)
    file.close()
    filestorage_obj = FileStorage(stream = open(new_filename, 'rb'), filename= new_filename)
    back = Backend()
    back.upload(new_filename, filestorage_obj)


def get_description(wiki_name):
    '''
    Params:
    wiki_name- name of wiki we want description of
    
    get filename
    get txt file from bucket
    return string, error message if no description
    '''
    d_name = wiki_name + "_description.md"
    back = Backend()
    description = back.get_description_from_bucket(d_name)
    return description

