from google.cloud import storage
from app.config import settings
from PIL import Image
import hashlib

class GCStorage:
    def __init__(self):
        # self.client = storage.Client.from_service_account_json(settings.google_application_credentials)
        self.client = storage.Client()
        self.bucket = self.client.get_bucket(settings.bucket_name)

    async def upload_file(self, file, folder):
        #get format
        format = file.filename.split('.')[-1]
        #hash filename
        filename = hashlib.md5(file.filename.encode()).hexdigest()


        #upload to gcs
        blob = self.bucket.blob(f'{folder}/{filename}.{format}')
        blob.upload_from_file(file.file)
        blob.make_public()
        return blob.public_url

    def download_file(self, blob_name, file_name):
        blob = self.bucket.blob(blob_name)
        blob.download_to_filename(file_name)