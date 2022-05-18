from storages.backends.gcloud import GoogleCloudStorage

storage = GoogleCloudStorage()

class Upload():
    @staticmethod
    def upload_file(file, filename):
        try:
            path = storage.save(filename, file)
            return storage.url(path)
        except Exception as e:
            print('Failed to upload')
