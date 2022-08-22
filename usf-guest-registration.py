import requests

session = requests.Session()

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
        'phoneNumber': input('Phone (without +1): '),
        'sendMethod': 'SMS',
        'devLatitude': None,
        'devLongitude': None
    }
)

print('Response:', register_resp.json())
print('Session ID:', register_resp.cookies['PHPSESSID'])

code = input('SMS Code: ')

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
        'validationCode': code,
        'phoneNumber': None,
        'devLatitude': None,
        'devLongitude': None
    }
)

validate_data = validate_resp.json()
if not validate_data['result'] == 'SUCCESS':
    input(f'Error: {validate_data}. Press [Enter] to exit...')
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

print(selfreg.text)