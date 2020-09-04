import requests
import json
import time
import pandas as pd

url = dict(
    sign_in='https://api.timeular.com/api/v3/developer/sign-in',
    list_activities='https://api.timeular.com/api/v3/activities',
    currentTracking='https://api.timeular.com/api/v3/tracking'
)

auth = json.dumps(
    dict(
        apiKey="NTMzNjNfYjk3MTMwM2E4YWM0NDZmMWE5ZWYxZGNkNmE1NzYzNmY=",
        apiSecret="MDdlZjNjNmI4ODIzNGI4ZWExNjg1MDNjNDhjMjY1YTI="
    )
)

token = json.loads(requests.post(url=url['sign_in'], data=auth).text)['token']

headers = dict(
        Authorization=f'Bearer {token}'
)

r = requests.get(url=url['list_activities'], headers=headers)
# print(json.loads(r.text)['activities'])
l1 = list()
keep = ['id', 'name', 'color']
for a in json.loads(r.text)['activities']:
    temp_dict = dict()
    for key in a.keys():
        if key in keep:
            temp_dict.update({key: a[key]})
    l1.append(temp_dict)

activities = pd.DataFrame(l1).set_index('id')

op = 'go'
while op != 'stop':
    r = requests.get(url=url['currentTracking'], headers=headers)
    current_tracking = json.loads(r.text)['currentTracking']

    if current_tracking:
        color = activities.at[current_tracking['activityId'], 'color']
        activity = activities.at[current_tracking['activityId'], 'name']
        print(activity,color)
    else:
        print("Nothing is happening")


    time.sleep(15)
