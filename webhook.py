# adapted from https://ogma-dev.github.io/posts/simple-flask-webhook/

import os
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify

from vcontrollers import SNESController

active_controllers = {}

def handle_post(data):
    print(data)
    id = data.get('cid', None)
    if id in active_controllers.keys():
        active_controllers[id].combo(data)
        return jsonify({'status':'success'}), 200
    else:
        return jsonify({'status':'invalid controller id'}), 401

def temp_token():
    '''generates a random token of 48 hex characters'''
    import binascii
    temp_token = binascii.hexlify(os.urandom(24))
    return temp_token.decode('utf-8')

WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN')
CLIENT_AUTH_TIMEOUT = 24 # in Hours

app = Flask(__name__)

authorised_clients = {}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('verify_token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            # add user to authorised clients list
            print('Added', request.remote_addr, 'to authorized list')
            authorised_clients[request.remote_addr] = datetime.now()
            return jsonify({'status':'success'}), 200
        else:
            return jsonify({'status':'bad token'}), 401

    elif request.method == 'POST':
        client = request.remote_addr
        if client in authorised_clients:
            if datetime.now() - authorised_clients.get(client) > timedelta(hours=CLIENT_AUTH_TIMEOUT):
                # client is too old. Kick out of authorized list
                print('Removed', client, 'from authorized list')
                authorised_clients.pop(client)
                return jsonify({'status':'authorisation timeout'}), 401
            else:
                # valid client sent something. Print it
                return handle_post(request.json)
        else:
            return jsonify({'status':'not authorised'}), 401

    else:
        abort(400)

if __name__ == '__main__':
    if WEBHOOK_VERIFY_TOKEN is None:
        print('WEBHOOK_VERIFY_TOKEN has not been set in the environment.\nGenerating random token...')
        token = temp_token()
        print('Token: %s' % token)
        WEBHOOK_VERIFY_TOKEN = token

    # instantiate the device
    c = SNESController()
    active_controllers[c.id] = c
    print('Listing Active controller IDs:')
    for i in active_controllers.keys():
        print(i)

    app.run()
    print('done runnin\'')
    # clean up when done
    c.destroy()
