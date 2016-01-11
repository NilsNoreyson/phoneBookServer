import subprocess, shlex, shutil
import time
import re
import copy
from threading import Thread
import Queue


class BTLE_PHONE:
    def __init__(self, device_mac):
        self.device_mac = device_mac
        self.last_command = None
        self.scan_thread = Thread(target=self.check_phone_signals)
        self.do_scan = True
        self.scan_thread.start()

        self.queue = Queue.Queue()


    def stop_thread(self):
        self.do_scan = False
        self.scan_thread.join()

    def get_last_command(self):
        #last_cmd = copy.copy(self.last_command)
        last_cmd = self.queue.get()
        #self.last_command = None
        return last_cmd

    def check_dev(self):
        cmd = 'hciconfig lestates'
        arg = shlex.split(cmd)

        out = subprocess.check_output(arg)
        output =  out.split('\n')
        if output:
            match = re.match('(^.*):\t' ,output[0])
            hci_dev = match.groups()[0]
            is_up =  output[2].strip().startswith('UP')

            if not(is_up):
                cmd = 'hciconfig {0} up'.format(hci_dev)
                print 'run sudo "{0}" '.format(cmd)

    def check_phone_signals(self):
        cmd = 'gatttool --device={0} -t random --char-read --uuid=2221 --listen'.format(self.device_mac)

        print(cmd)
        arg = shlex.split(cmd)
        print(arg)
        data_old = [0,0,0]
        last_index = 0
        while self.do_scan:
            try:
                out = subprocess.check_output(arg)
            except:
                out = ''
                pass
            if 'value:' in out:
                data = out.split('value:')[1]
                data =  [int(d,16) for d in data.strip().split(' ')]
                if data[0]==0 :
                    print 'sleep'
                    time.sleep(1)
                    data = []
                else:
                    if last_index == data[2]:
                        pass
                    else:
                        self.last_command = data
                        self.queue.put(data)
                        last_index = data[2]
        return True

if __name__ == '__main__':
    ble = BTLE_PHONE('EE:A7:8B:BB:45:D4')
    while True:
        out= ble.get_last_command()
        if out:
            print out
        time.sleep(0.1)
    # time.sleep(4)
    # ble.stop_thread()