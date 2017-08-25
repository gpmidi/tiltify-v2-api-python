import requests

#curl https://tiltify.com/api_test/v2/campaign?donations=true -H "Authorization: Token token=test_479c924413fe9168952891e9a36"

class TiltifyAPI:
    url = 'https://tiltify.com/api_test/v2/campaign?donations=true'
    donations_url = url + '/donations'

    def __init__(self, api_key):
        self._api_key = api_key

    def get_donations(self, limit=None):
        headers = {'Authorization': 'Token token={}'.format(self._api_key)}
        response = requests.get(url=self.donations_url, headers=headers)
        print(response)
        print(response.text)


if __name__ == '__main__':
    key = 'test_479c924413fe9168952891e9a36'
    tiltify = TiltifyAPI(api_key=key)
    tiltify.get_donations()
