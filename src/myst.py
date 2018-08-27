from bottle import get, run, request

api = "https://api.darksky.net/forecast/{key}/{latitude},{longitude}"

def load_config ( ):
	with open('config.json', 'r') as cfg:
		config = json.loads(cfg.read())
		cfg.close()
	return config

@get('/auto/forecast')
def get_forecast():
	ip = request.environ.get('REMOTE_ADDR')
	print(ip)

run(host='localhost', port=8080)