import requests
import argparse

p = argparse.ArgumentParser()
p.add_argument('-m', '--mode', help='First use [r]egister, then [v]alidate. Or just use [i]nteractive. Usage: -m/--mode r/v/i', required=True)
p.add_argument('-p', '--phone', help='Use in register mode. Usage: -p/--phone 5551236969')
p.add_argument('-s', '--session', help='Use in validate mode. Usage: -s/--session PHPSESSID')
p.add_argument('-c', '--code', help='Use in validate mode. Usage: -c/--code example-balls27')

args = p.parse_args()
if args.mode.lower() == 'r':
    if not args.phone:
        p.error('In register mode, -p/--phone is required')
elif args.mode.lower() == 'v':
    if not args.code:
        p.error('In validate mode, -c/--code is required')
    if not args.session:
        p.error('In validate mode, -s/--session is required')

session = requests.Session()

if args.mode.lower() == 'i':
    args.phone = input('Phone number: ')

if args.mode.lower() in ('r', 'i'):
    register_resp = session.post(
        'https://guestwireless.net.usf.edu/Network_Registration/action.php', 
        headers={
            'Sec-Ch-Ua': '"Not A;Brand";v="99", "Chromium";v="96"',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Origin': 'https://guestwireless.net.usf.edu',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://guestwireless.net.usf.edu/Network_Registration/'
        },
        data={
            'action': 'Register',
            'phoneNumber': args.phone,
            'sendMethod': 'SMS',
            'devLatitude': None,
            'devLongitude': None
        }
    )

    print('Response:', register_resp.json())
    print('Session ID (for -s/--session):', register_resp.cookies['PHPSESSID'])
    print('Command to validate:', 'python3 usf-guest-registration.py -m v -s', register_resp.cookies['PHPSESSID'], '-c <code>')

if args.mode.lower() == 'i':
    args.code = input('SMS Code: ')

if atgs.mode.lower() in ('v', 'i'):
    validate_resp = session.post(
        'https://guestwireless.net.usf.edu/Network_Registration/action.php', 
        headers={
            'Sec-Ch-Ua': '"Not A;Brand";v="99", "Chromium";v="96"',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Origin': 'https://guestwireless.net.usf.edu',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://guestwireless.net.usf.edu/Network_Registration/'
        },
        data={
            'action': 'Validate',
            'validationCode': args.code,
            'phoneNumber': None,
            'devLatitude': None,
            'devLongitude': None
        }
    )

    validate_data = validate_resp.json()
    if not validate_data['result'] == 'SUCCESS':
        if args.mode.lower() == 'i':
            input(f'Error: {validate_data}. Press [Enter] to exit...')
        else:
            print(f'Error: {validate_data}')
        exit(1)
    token = validate_data['token']
    print(f'Recieved token [{token}] for phone number:', validate_data['identifier'])

    selfreg = session.post(
        'https://guestwireless.net.usf.edu/cgi-bin/SubmitRegistrationForm_SelfReg', 
        headers={
            'Sec-Ch-Ua': '"Not A;Brand";v="99", "Chromium";v="96"',
            'X-Requested-With': 'XMLHttpRequest',
            'Sec-Ch-Ua-Mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            'Sec-Ch-Ua-Platform': '"Linux"',
            'Origin': 'https://guestwireless.net.usf.edu',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://guestwireless.net.usf.edu/Network_Registration/'
        },
        data={
            'token': token,
            'phoneNumber': validate_data['identifier'],
            'type': 'SMS'
        }
    )

    print('Response:\n\n', selfreg.text)