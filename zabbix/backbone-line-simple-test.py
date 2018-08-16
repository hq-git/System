#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import json


url = 'http://bb.liwenbianji.cn:3030/api/Server/status'
interval_time = int(10)
record_dict = {}


def get_status(url):
    while True:
        # Get Sysbb API status
        try:
            ret = requests.get(url, timeout=5)
            # print(ret.status_code, ret.content)
            if url in record_dict:
                record_dict[url]['total_times'] += 1
            else:
                record_dict[url] = {'total_times': 1}
            raise ConnectionError('Who wan yi')
        # Failed
        except ConnectionError as e:
            print(e)
            continue
        except requests.ConnectionError as e:
            print('ConnectionError', e)
            continue
        except requests.ConnectTimeout as e:
            print('ConnectTimeout', e)
            continue
        except Exception as e:
            print('unknown error', e)
            continue
        # Judge the return value (1)
        if ret.status_code == 200 and ret.content == b'1':
            if 'success_times' in record_dict[url]:
                record_dict[url]['success_times'] += 1
            else:
                record_dict[url]['success_times'] = 1
        # Update file
        with open('backbone-line-simple-test-result.json', 'w') as f:
            print(record_dict)
            json.dump(record_dict, f)
        # Collect interval
        time.sleep(interval_time)


if __name__ == '__main__':
    # Get start time
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('%s Start test Sysbb API !'%start_time)
    record_dict['start_time'] = start_time
    # Begin
    get_status(url)



