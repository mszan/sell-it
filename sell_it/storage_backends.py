from storages.backends.gcloud import GoogleCloudStorage

"""
Modify django-storages for GCloud to set static, media folder in a bucket.
Found at https://stackoverflow.com/a/56884027/13273250
"""
class GoogleCloudMediaStorage(GoogleCloudStorage):
    """
    GoogleCloudStorage suitable for Django's Media files.
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'media'
        super(GoogleCloudMediaStorage, self).__init__(*args, **kwargs)


class GoogleCloudStaticStorage(GoogleCloudStorage):
    """
    GoogleCloudStorage suitable for Django's Static files
    """

    def __init__(self, *args, **kwargs):
        kwargs['location'] = 'static'
        super(GoogleCloudStaticStorage, self).__init__(*args, **kwargs)