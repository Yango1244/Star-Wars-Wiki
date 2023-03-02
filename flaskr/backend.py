# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage
from hashlib import blake2s

class Backend:

    def __init__(self):
        self.cur_client = storage.Client()
        self.content_bucket = self.cur_client.get_bucket('fantasticwikicontent')
        self.user_bucket = self.cur_client.get_bucket('fantasticuserinfo')
        
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):

        blobs = self.cur_client.list_blobs(self.content_bucket_name)
        
        return blobs
        
    def upload(self):
        pass

    def sign_up(self, username, password):
        user_blob = self.user_bucket.get_blob(username)

        if (user_blob):
            return 
        else:
            user_blob = self.user_bucket.blob(username)
            hashed_password = blake2s((password + username + "fantastic").encode('ASCII'))
            user_blob.upload_from_string(hashed_password)

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


