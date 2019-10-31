import os
import sys

outjson = []
outjson.append('''{"ph":"M", "name":"benchmark_app", "pid":5880, "tid":139832523343680, "args":{"name":"DRM event"}},\n''')
prefix = '"ph":"X", "pid":5880, "tid":139832523343680'

exec_req = {}
with open("tmp3.log", "rt") as f:
    for line in f:
        seg = line.split()
        proc = seg[0].split('-')
        if proc[0] == "benchmark_app":
            name = '"name":"' + seg[3] + '"'
            ts = '"ts":' + seg[2].strip(':').replace('.', '')
            dur = '"dur":' + '0'
            jsonline = '    {' + prefix + ", " + name + ", " + ts + ", " + dur + "}, \n"
            outjson.append(jsonline)

        if line.find('ctx=81') > 0:
            seqno = line[line.find('seqno='):].split(',')[0].split('=')[1]
            if seqno in exec_req.keys():
                exec_req.get(seqno).append(line)
            else:
                exec_req[seqno]=[]
                exec_req.get(seqno).append(line)
            tmp = exec_req.get(seqno)

execjson = []
execjson.append('''{"ph":"M", "name":"thread_name", "pid":4497, "tid":94119680249856, "args":{"name":"Render Engine"}},\n''')
prefix = '"ph":"X", "pid":4497, "tid":94119680249856'

for seqno in exec_req.keys():
    reqin = reqout = ''
    eventlist = exec_req[seqno]
    for line in eventlist:
        if line.find("i915_request_in") > 0:
            reqin = line
        elif line.find("i915_request_out") > 0:
            reqout = line
        if len(reqin) > 0 and len(reqout) > 0:
            seg = reqin.split()
            name = '"name":"' + seqno + '"'
            stamp_in = reqin.split()[2].strip(':').replace('.', '')
            stamp_out = reqout.split()[2].strip(':').replace('.', '')
            ts = '"ts":' + stamp_in
            dur = '"dur":' + str(int(stamp_out) - int(stamp_in))
            jsonline = '    {' + prefix + ", " + name + ", " + ts + ", " + dur + "}, \n"
            execjson.append(jsonline)
            break
        
with open("out.json", 'wt') as f:
    f.writelines('[\n')
    f.writelines(execjson)
    f.writelines(outjson)
