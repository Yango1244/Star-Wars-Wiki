from flaskr.backend import Backend
from flask import Flask
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
    new_filename = filename + "_description.txt"
    blob_filename = filename + "/description.txt"
    f = open(new_filename, "w")
    print("writing description file")
    f.write(description)
    print(f)
    f.close()
    back = Backend()
    back.upload(blob_filename, f)

def get_description(wiki_name):
    '''
    Params:
    wiki_name- name of wiki we want description of
    
    get filename
    get txt file from bucket
    return string, error message if no description
    '''
    d_name,ext = wiki_name.split('.')
    d_name = d_name + "_description.txt"
    back = Backend()
    description = back.get_wiki_page(d_name)
    if description is None:
        return None
    f = open(description, 'r')
    print(f)
    content = f.read()
    f.close()
    return content
     
