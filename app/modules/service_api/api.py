import requests
import secret


class ServiceApi:
    """ Api for FaceRecognition_REST-API service.
        Contains methods for specific request with name same as endpoint.
        Authorisation is handled via bearer token.
    """
    def __init__(self, host: str = '127.0.0.1', port: int = 5000, bearer_token: str = secret.TOKEN):
        self.headers = {"Authorization": f"Bearer {bearer_token}"}
        self.host = host
        self.port = port

    @property
    def server_name(self):
        return f'http://{self.host}:{self.port}'

    def request(self, method: str, url: str, params: dict = None):
        """ Makes request with given method.
            Args:
                method: HTTP method e.g. 'GET', 'POST'
                url: url string in format /<url>/
                params: dict of query args
            Returns:
                request.Response object, error
        """
        url = self.server_name + url
        try:
            response = requests.request(method, url, headers=self.headers, params=params)
        except requests.RequestException as error:
            return None, str(error)
        return response, None

    def post(self, url: str, params: dict = None):
        """ POST request.
            Args:
                url: url string in format /<url>/
                params: dict of query args
            Returns:
                request.Response object, error (str)
        """
        return self.request('POST', url, params)

    def get(self, url: str, params: dict = None):
        """ GET request.
            Args:
                url: url string in format /<url>/
                params: dict of query args
            Returns:
                request.Response object, error (str)
        """
        return self.request('GET', url, params)

    def kill(self):
        return self.get('/kill/')

    def restart(self):
        return self.get('/restart/')

    def members_get(self, member_id: int = None, user_id: str = None):
        if member_id:
            return self.get('/members/get/' + f'{member_id}/')
        elif user_id:
            return self.get('/members/get/', params=dict(user_id=user_id))
        else:
            return self.get('/members/get/')
