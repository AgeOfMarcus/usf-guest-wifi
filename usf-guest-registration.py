import requests
import argparse
import pickle
import os
# api.py
from api import API

def save_session(session: requests.Session, fn: str):
    with open(fn, 'wb') as f:
        pickle.dump(session, f)

p = argparse.ArgumentParser()
p.add_argument('-m', '--mode', help='First use [r]egister, then [v]alidate. Or just use [i]nteractive. Usage: -m/--mode r/v/i', required=True)
p.add_argument('-p', '--phone', help='Use in register mode. Usage: -p/--phone 5551236969')
p.add_argument('-s', '--session', help='File to store session data in. Usage: -s/--session session.pkl. Default: session.pkl', default='session.pkl')
p.add_argument('-c', '--code', help='Use in validate mode. Usage: -c/--code example-balls27')

args = p.parse_args()
if args.mode.lower() == 'r':
    if not args.phone:
        p.error('In register mode, -p/--phone is required')
elif args.mode.lower() == 'v':
    if not args.code:
        p.error('In validate mode, -c/--code is required')

if os.path.exists(args.session):
    with open(args.session, 'rb') as f:
        session = pickle.load(f)
else:
    session = requests.Session()
api = API(session)

if args.mode.lower() == 'i':
    args.phone = input('Phone number: ')

if args.mode.lower() in ('r', 'i'):
    register_resp = api.register(args.phone, 'SMS')
    save_session(api.session, args.session)

    print('Response:', register_resp)
    print('Command to validate:', 'python usf-guest-registration.py -m v -s', args.session, '-c <code>')

if args.mode.lower() == 'i':
    args.code = input('SMS Code: ')

if args.mode.lower() in ('v', 'i'):
    validate_data = api.validate(args.code, args.phone)

    if not validate_data['result'] == 'SUCCESS':
        if args.mode.lower() == 'i':
            input(f'Error: {validate_data}. Press [Enter] to exit...')
        else:
            print(f'Error: {validate_data}')
        exit(1)
    token = validate_data['token']
    print(f'Recieved token [{token}] for phone number:', validate_data['identifier'])

    selfreg = api.finalize(token, validate_data['identifier'])

    print('Response:\n\n', selfreg)