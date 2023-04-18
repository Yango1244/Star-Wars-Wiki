from flaskr.backend import Backend


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
    filename = filename.split('.')
    new_filename = filename + "_description.txt"
    f = open(new_filename, "w")
    f.write(description)
    f.close()
    back = Backend()
    back.upload(new_filename, f)


def get_description(wiki_name):
    '''
    Params:
    wiki_name- name of wiki we want description of
    
    get filename
    get txt file from bucket
    return string, error message if no description
    '''
    d_name = wiki_name.split('.')
    d_name = d_name + "_description.txt"
    back = Backend()
    description = back.get_wiki_page(d_name)
    if description is None:
        return None
    f = open(description, 'r')
    content = f.read()
    f.close()
    return content
