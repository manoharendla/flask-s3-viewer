import sys

from flask import Flask
from flask_s3up import FlaskS3Up
from flask_s3up.aws.ref import Region

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(message)s'
)

app = Flask(__name__)

# For test, disable template caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['TEMPLATES_AUTO_RELOAD'] = True

# FlaskS3Up Init
s3up = FlaskS3Up(
    app, # Flask app
    namespace='flask-s3up', # namespace be unique
    template_namespace='mdl', # set template
    object_hostname='http://flask-s3up.com', # file's hostname
    allowed_extensions={}, # allowed extension
    config={ # Bucket configs and else
        'profile_name': 'PROFILE_NAME',
        'access_key': None,
        'secret_key': None,
        'region_name': Region.SEOUL.value,
        'endpoint_url': None,
        'bucket_name': 'BUCKET_NAME',
        'cache_dir': '/tmp/flask_s3up',
        'use_cache': True,
        'ttl': 86400,
    }
)

# Init another one
s3up.add_new_one(
    namespace='example',
    object_hostname='http://example.com',
    config={
        'profile_name': 'PROFILE_NAME',
        'region_name': Region.SEOUL.value,
        'bucket_name': 'BUCKET_NAME'
    }
)

# You can see registerd configs
# print(s3up.FLASK_S3UP_BUCKET_CONFIGS)

# You can use boto3's session and client if you want
# print(FlaskS3Up.get_boto_client(S3UP_NAMESPACE))
# print(FlaskS3Up.get_boto_session(S3UP_NAMESPACE))

# Apply FlaskS3Up blueprint
s3up.register()

@app.route('/index')
def index ():
    return 'Your app index page'

# Usage: python example.py test (run debug mode)
if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'test':
            debug = True
    app.run(debug=debug, port=3000)

