from flask import Flask, request
from celery import Celery


app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task()
def add(a, b):
	return str(a + b)

@celery.task()
def calc(s):
	return str(eval(s))

@app.route('/')
def hello():
	return 'Hello World!\n'

@app.route('/add')
def add_flask():
	a = request.args.get('a')
	b = request.args.get('b')
	result = add.delay(int(a), int(b))
	return result.get()

@app.route('/calc')
def calc_flask():
	result = calc.delay(next(iter(request.args)))
	return result.get()
