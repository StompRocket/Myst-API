from bottle import get, run, request
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
import json


ip_api = "http://ipinfo.io/json/127.0.0.1"
ds_api = "https://api.darksky.net/forecast/{key}/{latitude},{longitude}"

def load_config ( ):
	with open('config.json', 'r') as cfg:
		config = cfg.read()
		cfg.close()
	print(config)
	return json.loads(config)

@get('/<lat>/<long>/forecast')
def get_forecast(lat, long):
	cfg = load_config()
	res = urlopen(ds_api.format(key = cfg['keys'][0], latitude = lat, longitude = long)).read()
	daily = json.loads(res)['daily']['data']

	data = []
	for i, _ in enumerate(daily):
		data.append(
			{
				"summary": daily[i]['summary'],
				"high": daily[i]['temperatureHigh'],
				"low": daily[i]['temperatureLow']
			}
		)
	return json.dumps(data)

run(host='localhost', port=8080)