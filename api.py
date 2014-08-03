from event import X10Event
from flask import Flask
from flask import g
from flask import jsonify as j

app = Flask(__name__)
daemon = None

def run_api(d, port=5000):
    global daemon
    daemon = d
    app.run(host='0.0.0.0', port=port)

@app.before_request
def before_request():
    g._daemon = daemon

@app.route('/on/<house>/<int:unit>', methods=['GET', 'POST'])
def on(house, unit=X10Event.UNIT_ALL):
    result = {'success': g._daemon.on(house, unit)}
    return j(**result)

@app.route('/off/<house>/<int:unit>', methods=['GET', 'POST'])
def off(house, unit=X10Event.UNIT_ALL):
    result = {'success': g._daemon.off(house, unit)}
    return j(**result)
