import os
import uuid
from flask import current_app, url_for

class BaseStorageProvider:
    def upload_file(self, file, unique_prefix=""):
        """Uploads a file and returns its public URL or identifier path."""
        raise NotImplementedError

    def delete_file(self, file_url_or_path):
        """Deletes a file from the storage repository."""
        raise NotImplementedError

class LocalStorageProvider(BaseStorageProvider):
    def upload_file(self, file, unique_prefix=""):
        ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{unique_prefix}{uuid.uuid4().hex[:10]}{ext}"
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_name)
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        # Return web accessible path for local files
        return url_for('static', filename='uploads/' + unique_name)

    def delete_file(self, file_url_or_path):
        filename = os.path.basename(file_url_or_path)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception:
                pass

class GoogleCloudStorageProvider(BaseStorageProvider):
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from google.cloud import storage
            self._client = storage.Client()
        return self._client

    def upload_file(self, file, unique_prefix=""):
        ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{unique_prefix}{uuid.uuid4().hex[:10]}{ext}"
        
        bucket = self.client.bucket(self.bucket_name)
        blob = bucket.blob(unique_name)
        
        # Reset file pointer to beginning just in case
        file.seek(0)
        
        # Detect content type/mime type
        content_type = file.content_type or 'application/octet-stream'
        
        # Upload using upload_from_file
        blob.upload_from_file(file, content_type=content_type)
        
        # Return public URL of the uploaded blob
        return blob.public_url

    def delete_file(self, file_url_or_path):
        filename = os.path.basename(file_url_or_path)
        try:
            bucket = self.client.bucket(self.bucket_name)
            blob = bucket.blob(filename)
            blob.delete()
        except Exception:
            pass

def get_storage_provider():
    provider_name = current_app.config.get('STORAGE_PROVIDER', 'local').lower()
    if provider_name == 'gcs':
        bucket_name = current_app.config.get('GCS_BUCKET_NAME')
        if not bucket_name:
            raise ValueError("GCS_BUCKET_NAME configuration is required when STORAGE_PROVIDER is 'gcs'!")
        return GoogleCloudStorageProvider(bucket_name)
    return LocalStorageProvider()
