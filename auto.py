import os
import trace2json

#app_cmd = 'ffmpeg -hwaccel vaapi -hwaccel_output_format vaapi -i ~/test.264 -f null -'
app_cmd = 'h264encode'

logfile = 'tmp.log'
cmd = 'sudo trace-cmd list | grep i915 >' + logfile
os.system(cmd)

with open(logfile, 'rt') as f:
    lines = f.readlines()
os.system('rm ' + logfile)

trace_cmd_start = ''
trace_cmd_start += 'sudo trace-cmd start '
for l in lines:
    c = '-e "' + l.strip() + '" '
    trace_cmd_start += c

os.system('sudo trace-cmd reset')
os.system(trace_cmd_start)

os.system(app_cmd)

os.system('sudo trace-cmd stop')
os.system('sudo trace-cmd extract -o trace.dat')
os.system('sudo trace-cmd reset')

drm_logfile = 'drm.log'
trace_report = 'trace-cmd report trace.dat >' + drm_logfile
os.system(trace_report)

trace2json.execute(drm_logfile)

print('done')