# TODO(Project 1): Implement Backend according to the requirements.
from google.cloud import storage

class Backend:

    def __init__(self):
        self.content_bucket_name = 'fantasticwikicontent'
        self.user_bucket_name = 'fantasticuserinfo'
        self.cur_client = storage.Client()
        
        
    def get_wiki_page(self, name):
        pass

    def get_all_page_names(self):

        blobs = self.cur_client.list_blobs(self.content_bucket_name)
        
        return blobs
        
    def upload(self):
        pass

    def sign_up(self):
        pass

    def sign_in(self):
        pass

    def get_image(self):
        pass


