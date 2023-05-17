from requests import Session

class API(object):
    def __init__(self, session: Session, base_url: str = 'https://guestwireless.net.usf.edu'):
        self.session = session
        self.headers = {
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
        }
        self.base_url = base_url
    
    def register(self, phone_number: str, send_method: str, dev_latitude: str = None, dev_longitude: str = None):
        resp = self.session.post(
            f'{self.base_url}/Network_Registration/action.php', 
            headers=self.headers,
            data={
                'action': 'Register',
                'phoneNumber': phone_number,
                'sendMethod': send_method,
                'devLatitude': dev_latitude,
                'devLongitude': dev_longitude
            }
        )
        return resp.json()

    def validate(self, validation_code: str, phone_number: str, dev_latitude: str = None, dev_longitude: str = None):
        resp = self.session.post(
            f'{self.base_url}/Network_Registration/action.php', 
            headers=self.headers,
            data={
                'action': 'Validate',
                'validationCode': validation_code,
                'phoneNumber': phone_number,
                'devLatitude': dev_latitude,
                'devLongitude': dev_longitude
            }
        )
        res = resp.json()
        if not res['result'].lower() == 'success':
            raise RuntimeError(res)

        return res
        return self.finalize(
            token = res['token'],
            phoneNumber = res['identifier'],
        )
    
    def finalize(self, token: str, phoneNumber: str, sendMethod: str = 'SMS', host: str = 'mhb-dhcp.net.usf.edu'):
        resp = self.session.post(
            f'https://{host}/cgi-bin/SubmitRegistrationForm_SelfReg',
            headers=self.headers,
            data={
                'token': token,
                'phoneNumber': phoneNumber,
                'type': sendMethod
            }
        )
        res = resp.text
        if '<P>' in res:
            return res.split('<P>')[1]
        return res