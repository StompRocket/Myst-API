from bottle import get, run, request
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import HTTPError
import json

ds_api = "https://api.darksky.net/forecast/{key}/{latitude},{longitude}"

def load_config ( ):
	with open('config.json', 'r') as cfg:
		config = cfg.read()
		cfg.close()
	return json.loads(config)

def write_config( config ):
	with open('config.json', 'w+') as cfg:
		cfg.write(json.dumps(config))
		cfg.close()

def choose_key ( config ):
	key_len = len(config['keys'])
	last_key = config['last-key']
	if key_len > 1:
		if last_key >= key_len:
			config['last-key'] = 0
			write_config()
			return config['keys'][0]
		else:
			config['last-key'] = last_key + 1
			return config['keys'][config['last-key']]
	else:
		return config['keys'][0]

@get('/<lat>/<long>/forecast')
def get_forecast(lat, long):
	cfg = load_config()
	key = choose_key( cfg )
	print("using key %s for request" % key)
	res = urlopen(ds_api.format(key = key, latitude = lat, longitude = long)).read()
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