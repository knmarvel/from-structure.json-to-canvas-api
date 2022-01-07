import json
import requests
# run pip install slugify to make this app work
from slugify import slugify

# Fill in the following variables:

# download your structure.json and put the link below
json_file = ""
# get your course number from canvas, make sure you use it as a string
course_number = ""
# get your access token from https://my.kenzie.academy/profile/settings
my_canvas_access_token = ""
# ask kenzie studio for the subdomain
subdomain = ""

with open(json_file) as f:
    data = f.read()

dict_data = json.loads(data)
pages_list = []

modules = dict_data["modules"]
for mod in modules:
    for sub in mod["submodules"]:
        if "sections" in sub.keys():
            for s in sub['sections']:
                if "pages" in s.keys():
                    pages_list = pages_list + s["pages"]

for page in pages_list:
    if type(page) != "string":
        token = my_canvas_access_token
        URL = f"https://my.kenzie.academy/api/v1/courses/{course_number}/pages/{slugify(page['title'])}"
        path = page['path']
        request_header = {"Authorization": f"Bearer {token}"}
        r = requests.put(URL, headers=request_header, json={
            'wiki_page':
                {
                    'title': page['title'],
                    'body': f'<p><iframe style="width: 100%; height: 1024px;" src="https://{subdomain}.kenzie.studio{path}/index.html" width="100%" height="1024px" allowfullscreen="allowfullscreen" webkitallowfullscreen="webkitallowfullscreen" mozallowfullscreen="mozallowfullscreen"></iframe></p>'
                }
            })
        print(r)

