#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import json


url = 'http://bb.liwenbianji.cn:3030/api/Server/status'
interval_time = int(10)
record_dict = {
    'time': {
            'start': '',
            'update': '',
            }
}


def get_status(url_str):
    while True:
        if url_str in record_dict:
            record_dict[url_str]['total_times'] += 1
        else:
            record_dict[url_str] = {'total_times': 1}
        # Get Sysbb API status
        try:
            ret = requests.get(url_str, timeout=5)
            # print(ret.status_code, ret.content)
        # Failed
        except KeyboardInterrupt:
            exit('Collect end !')
        except requests.exceptions.ConnectTimeout as e:
            # print('ConnectTimeout', e)
            continue
        except requests.exceptions.ConnectionError as e:
            # print('ConnectionError', e)
            continue
        except Exception as e:
            # print('unknown error', e)
            continue
        # Judge the return value (1)
        if ret.status_code == 200 and ret.content == b'1':
            if 'success_times' in record_dict[url_str]:
                record_dict[url_str]['success_times'] += 1
            else:
                record_dict[url_str]['success_times'] = 1
        # Get update time
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        record_dict['time']['update'] = update_time
        # Update file
        with open('%s-result.json' % __file__.replace('.py', ''), 'w') as f:
            # print(record_dict)
            json.dump(record_dict, f)
        # Collect interval
        time.sleep(interval_time)


if __name__ == '__main__':
    # Get start time
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print('%s Start test Sysbb API !'%start_time)
    record_dict['time']['start'] = start_time
    # Begin
    get_status(url)



