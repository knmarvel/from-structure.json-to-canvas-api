import json
import requests
# run pip install slugify to make this app work
from slugify import slugify

# Fill in the following variables:

# download your structure.json and put the link below
json_file = ""
# get your course number from canvas
course_number = "230"
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


def request_maker(title, path):
    page_json = {
        "url": slugify(title),
        "title": title,
        "hide_from_students": True,
        "editing_roles": "teachers",
        "body": f"<p><iframe id='gatsby' style='width: 100%; height: 1024px;' src='{subdomain}.kenzie.studio{path}' width='100%' height='1024px' allowfullscreen='allowfullscreen' webkitallowfullscreen='webkitallowfullscreen' mozallowfullscreen='mozallowfullscreen'></iframe></p>",
        "published": False,
        "front_page": False,
        "locked_for_user": False,
        }
    return json.dumps(page_json)


page_requests = []
for page in pages_list:
    if type(page) != "string":
        URL = f"https://my.kenzie.academy/api/v1/courses/{course_number}/pages/{slugify(page['title'])}"
        print(URL)
        request_body = request_maker(page['title'], page['path'])
        request_header = {"Authorization": f"Bearer {my_canvas_access_token}"}
        r = requests.put(URL, headers=request_header, data=request_body)
        print(r.status_code)
