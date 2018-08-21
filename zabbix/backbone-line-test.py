#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import threading
import json
import sys
import logging

url_dict = {
    'api_ha': 'http://bb.liwenbianji.cn:3030/api/Server/status',
    'api_direct': 'http://bb.edanzgroup.com:3000/api/Server/status',
}
interval_time = int(10)


class ApiTest(object):
    '''
    Test Sysbb API line status
    '''
    def __init__(self):
        self.record_dict = None
        self.thread_list = None
        self.lock = threading.Lock()

    def help(self):
        print('Usage: ./backbone-line-test.py OPTION\n \
        print_result   -> Print current result\n \
        start_test     -> Run test script')

    def handle(self):
        '''
        Handle typed in method
        '''
        if sys.argv:
            if len(sys.argv) > 1:
                method_str = sys.argv[1]
                if hasattr(self, method_str):
                    fun = getattr(self, method_str)
                    fun()
                else:
                    print('Invalid method "%s" !' % method_str)
                    self.help()
            else:
                print('Need OPTION !')
                self.help()
        else:
            self.help()

    def start_test(self):
        # Get start time
        start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print('%s Start test Sysbb API !' % start_time)
        # Data initialization
        self.record_dict = {
            'time': {
                'start': '',
                'update': '',
            }
        }
        self.thread_list = []
        self.record_dict['time']['start'] = start_time
        # Begin
        for i in url_dict:
            t = threading.Thread(target=self.__get_status, args=(i,))
            self.thread_list.append(t)
            t.setDaemon(True)
            t.start()

        for t in self.thread_list:
            t.join()

    def __get_status(self, target):
        while True:
            if target in self.record_dict:
                self.record_dict[target]['total_times'] += 1
            else:
                self.record_dict[target] = {'total_times': 1}
            # Get Sysbb API status
            try:
                ret = requests.get(url_dict[target], timeout=5)
                # print(ret.status_code, ret.content)
            # Failed
            except KeyboardInterrupt:
                exit('Collect end !')
            except requests.exceptions.ConnectTimeout as e:
                print('ConnectTimeout', e)
                continue
            except requests.exceptions.ConnectionError as e:
                print('ConnectionError', e)
                continue
            except Exception as e:
                print('unknown error', e)
                continue
            # Judge the return value (1)
            if ret.status_code == 200 and ret.content == b'1':
                if 'success_times' in self.record_dict[target]:
                    self.record_dict[target]['success_times'] += 1
                else:
                    self.record_dict[target]['success_times'] = 1
            # Get update time
            update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            self.record_dict['time']['update'] = update_time
            # Update file
            with open('%s-result.json' % __file__.replace('.py', ''), 'w') as f:
                # print(record_dict)
                json.dump(self.record_dict, f)
                f.flush()
            # Collect interval
            time.sleep(interval_time)

    def print_result(self):
        with open('%s-result.json' % __file__.replace('.py', ''), 'r') as f:
            recorde_dict = json.load(f)
            # recorde_dict = json.dumps(recorde_dict, indent=1)
            # print(recorde_dict)
        print('Time: %s - %s' % (recorde_dict['time']['start'], recorde_dict['time']['update']))
        print('\nDetail:')
        for i in recorde_dict:
            if i != 'time':
                print('-> Name: "%s"  Total_times: %s  Success_times: %s  Failed_percent: %.2f%%\n'
                      % (i,
                         recorde_dict[i]['total_times'],
                         recorde_dict[i]['success_times'],
                         100 - recorde_dict[i]['success_times']/recorde_dict[i]['total_times']*100,))

    def __log_record(self, msg):
        # logging.basicConfig(filename='backbone-test-multithread.log', level=logging.WARN)
        # logging.warning(msg)
        pass


if __name__ == '__main__':

    api_test = ApiTest()
    api_test.handle()



