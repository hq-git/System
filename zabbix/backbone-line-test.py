#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import threading
import json


url_dict = {
    'api_ha': 'http://bb.liwenbianji.cn:3030/api/Server/status',
    'api_direct': 'http://bb.edanzgroup.com:3000/api/Server/status',
}
interval_time = int(10)
record_dict = {}
thread_list = []
lock = threading.Lock()


def get_status(target):
    while True:
        # Get Sysbb API status
        try:
            ret = requests.get(url_dict[target], timeout=5)
            # print(ret.status_code, ret.content)
            if target in record_dict:
                record_dict[target]['total_times'] += 1
            else:
                record_dict[target] = {'total_times': 1}
        # Failed
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
            if 'success_times' in record_dict[target]:
                record_dict[target]['success_times'] += 1
            else:
                record_dict[target]['success_times'] = 1
        # Update file
        with open('backbone-line-test-result.json', 'w') as f:
            print(record_dict)

            json.dump(record_dict, f)
        # Collect interval
        time.sleep(interval_time)


def run():
    for i in url_dict:
        t = threading.Thread(target=get_status, args=(i,))
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()


if __name__ == '__main__':
    # Get start time
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('%s Start test Sysbb API !'%start_time)
    record_dict['start_time'] = start_time
    # Begin
    run()



