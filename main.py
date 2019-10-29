import requests
import json
from config import USER, PASSWORD, DEVICES_INFO

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'X-Requested-With': 'XMLHttpRequest',
    'X-Prototype-Version': '1.7',
    'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'http://192.168.1.1',
    'Connection': 'keep-alive',
    'Referer': 'http://192.168.1.1/homeAuthentication.html',
}

params = (
    ('username', USER),
    ('password', PASSWORD),
)

s = requests.Session()

# print s.cookies.get_dict()

response = s.post('http://192.168.1.1/authenticate', headers=headers, params=params)

response = response.json()

contextID = response['data']['contextID']
headers['X-Context'] = contextID

data = '{"parameters":{"expression":{"usbM2M":"usb && wmbus and .Active==true","usb":"printer && physical and .Active==true","usblogical":"volume && logical and .Active==true","eth":"eth && edev and .Active==true","wifi":"wifi && edev and .Active==true","dect":"voice && dect && handset && physical"}}}'

response = s.post('http://192.168.1.1/sysbus/Devices:get', headers=headers, data=data)
response = response.json()

wifiDevices = [d['Key'] for d in response['status']['wifi']]
for person in DEVICES_INFO.keys():
    print "{}: {}".format(person, "YES" if any(device in wifiDevices for device in DEVICES_INFO[person]) else "NO")
