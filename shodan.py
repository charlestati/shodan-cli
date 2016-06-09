#!/usr/bin/env python3

import argparse
import json
import requests
from requests.packages import urllib3
from requests.exceptions import HTTPError

SERVER = 'shodan.epitech.eu'
VERSION = 1.1
CERTIFICATE = 'shodan.crt'


def get_payload(endpoint, arguments):
    if endpoint == 'challenge-info':
        if len(arguments) < 1:
            raise ValueError('Not enough arguments')
        return {'name': arguments[0]}
    elif endpoint == 'score':
        if len(arguments) < 2:
            raise ValueError('Not enough arguments')
        return {'chinpokomon': arguments[0], 'flag': arguments[1]}
    return {}


def send_request(endpoint, arguments, team, password):
    if endpoint == 'pwn':
        return  # I ain't no snitch

    try:
        payload = get_payload(endpoint, arguments)
    except ValueError as e:
        print(e)
        return

    url = 'https://{}/api/{}/{}'.format(SERVER, VERSION, endpoint)
    urllib3.disable_warnings()
    if payload:
        r = requests.post(url, verify=CERTIFICATE, auth=(team, password), json=payload)
    else:
        r = requests.get(url, verify=CERTIFICATE, auth=(team, password))

    try:
        r.raise_for_status()
    except HTTPError as e:
        print(e)
        return

    print(json.dumps(r.json(), indent=2, separators=(',', ': ')))


def main():
    parser = argparse.ArgumentParser(description='shodan api')
    parser.add_argument('team', type=str, help='team name')
    parser.add_argument('password', type=str, help='team password')
    parser.add_argument('endpoint', type=str, help='request endpoint')
    parser.add_argument('arguments', type=str, nargs='*', help='request arguments')
    argv = parser.parse_args()

    send_request(argv.endpoint, argv.arguments, argv.team, argv.password)


if __name__ == '__main__':
    main()
