import os
import json

from app import app



@app.route('/v1/api/<token>')
def auth(token):
    ...

@app.route('/page_idx=<int:index>')
def get_posts(index):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "static/data", "posts.json")
    with open(json_url, 'r') as file:
        data = json.load(file)
    return data
