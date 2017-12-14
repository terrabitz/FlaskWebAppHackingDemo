import requests
import random
import string


class WebAppCli:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url

    def session_demo_create_user(self, username):
        suffix = '/login_demo'
        password = 'test'

        data = {'username': username, 'password': password}
        r = requests.post(self.base_url + suffix, data=data)

    def create_rand_users(self, num_users, username_length=8):
        for i in range(num_users):
            rand_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(username_length))
            self.session_demo_create_user(rand_string)


if __name__ == '__main__':
    web_app_cli = WebAppCli()
    #web_app_cli.session_demo_create_user('test')
    web_app_cli.create_rand_users(20)