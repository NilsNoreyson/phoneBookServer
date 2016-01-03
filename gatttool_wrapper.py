import subprocess, shlex, shutil
import time
cmd = 'gatttool --device=EE:A7:8B:BB:45:D4 -t random --char-read --uuid=2221 --listen'
arg = shlex.split(cmd)
print(arg)
data_old = [0,0,0]
while True:
    while True:
        out = subprocess.check_output(arg)
        if 'value:' in out:
            data = out.split('value:')[1]
            data =  [int(d,16) for d in data.strip().split(' ')]
            if data==data_old:
                pass
            else:
                print data
                data_old = data
            if data[0]==0 :
                time.sleep(1)
                data = []
                break

