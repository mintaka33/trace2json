import os
import signal
import subprocess
import trace2json
import time

app_cmd = 'ffmpeg -hwaccel vaapi -hwaccel_output_format vaapi -i ~/test.264 -f null -'
app_cmd = 'h264encode'

logfile = 'tmp.log'
cmd = 'sudo trace-cmd list | grep i915 >' + logfile
os.system(cmd)

with open(logfile, 'rt') as f:
    lines = f.readlines()
os.system('rm ' + logfile)

trace_cmd = ''
trace_cmd += 'sudo trace-cmd record '
for l in lines:
    if l == lines[-1]:
        c = '-e "' + l.strip() + '"'
    else:
        c = '-e "' + l.strip() + '" '
    trace_cmd += c
trace_cmdlist = trace_cmd.split(' ') 
print(trace_cmdlist)

with open('trace.sh', 'wt') as f:
    f.writelines(trace_cmd)
os.system('chmod +x trace.sh')

trace_proc = subprocess.Popen(trace_cmdlist, shell=True)

os.system(app_cmd)
time.sleep(10)
trace_proc.terminate()
#os.kill(trace_proc.pid, signal.SIGINT)

drm_logfile = 'drm.log'
trace_report = 'trace-cmd report >' + drm_logfile
os.system(trace_report)

trace2json.execute(drm_logfile)

print('done')