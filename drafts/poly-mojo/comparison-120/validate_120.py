#!/usr/bin/env python3
"""Post-run output checks; does not generate inputs or measure algorithms."""
from pathlib import Path
import csv, os, signal, subprocess, time, json
ROOT=Path(__file__).resolve().parent/'comparison-120'
BACKENDS=['groebner','singular','msolve','polymojo']
CASES=list(csv.DictReader((ROOT/'cases.tsv').open(),delimiter='\t'))
JULIA='/workspace/tools/julia-1.10.2/bin/julia'
ENV=dict(os.environ, JULIA_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
LOGS=ROOT/'validation-logs'; LOGS.mkdir(exist_ok=True)

def rss_group(pid):
    total=0
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal(): continue
        try:
            fields=(proc/'stat').read_text().rsplit(')',1)[1].split()
            if int(fields[2])==pid: total+=int(fields[21])*os.sysconf('SC_PAGE_SIZE')
        except (OSError,ValueError,IndexError): pass
    return total

statuses={}
for suite in [1,2,3]:
    for backend in BACKENDS:
        p=ROOT/'raw'/backend/f'benchmark_{suite}'/'status.tsv'
        statuses[suite,backend]={r['problem']:r['status'] for r in csv.DictReader(p.open(),delimiter='\t')}
with (ROOT/'validation.tsv').open('w') as out:
    cols=['suite','problem','backend','run_status','validation','reference','basis_count','canonical_sha256']
    writer=csv.DictWriter(out,fieldnames=cols,delimiter='\t');writer.writeheader()
    for index,case in enumerate(CASES,1):
        suite=int(case['suite']);name=case['problem'];args=[]
        for backend in BACKENDS:
            if statuses[suite,backend].get(name)=='completed':
                path=ROOT/'raw'/backend/f'benchmark_{suite}'/name/'output'
                args.extend([backend,str(path)])
        parsed={};failure='not-completed'
        if args:
            prefix=LOGS/f'{suite}-{name}'
            start=time.monotonic()
            with prefix.with_suffix('.out').open('w') as stdout, prefix.with_suffix('.err').open('w') as stderr:
                proc=subprocess.Popen([JULIA,f'--project={ROOT.parent}/environment',str(ROOT.parent/'validate_case.jl'),*args],stdout=stdout,stderr=stderr,env=ENV,start_new_session=True)
                while proc.poll() is None:
                    if time.monotonic()-start > 180 or rss_group(proc.pid)>16*2**30:
                        failure='validation-resource-limit'
                        os.killpg(proc.pid,signal.SIGKILL);proc.wait();break
                    time.sleep(.2)
            for line in prefix.with_suffix('.out').read_text().splitlines():
                fields=line.split('\t')
                if len(fields)==4:parsed[fields[0]]=fields[1:]
            if proc.returncode and failure=='not-completed':failure='validation-error'
        references=[b for b in BACKENDS[:3] if b in parsed and parsed[b][0]=='parsed']
        reference=references[0] if references else ''
        for backend in BACKENDS:
            status=statuses[suite,backend].get(name,'missing')
            verdict='not-completed'; count=''; digest=''
            if status=='completed':
                data=parsed.get(backend)
                if data is None:verdict=failure
                elif data[0]!='parsed':verdict=data[0]
                else:
                    _,count,digest=data
                    peers=[b for b,d in parsed.items() if b!=backend and d[0]=='parsed']
                    if not peers:verdict='no-cross-check' if backend in BACKENDS[:3] else 'no-external-reference'
                    elif all(parsed[b][1:]==data[1:] for b in peers):verdict='full-basis-match'
                    else:verdict='MISMATCH'
            writer.writerow(dict(suite=suite,problem=name,backend=backend,run_status=status,validation=verdict,reference=reference,basis_count=count,canonical_sha256=digest))
        out.flush()
        print(f'Validated {index}/{len(CASES)}: suite {suite}, {name}; {len(parsed)} outputs; reference={reference or "none"}',flush=True)
print('Post-run validation finished.',flush=True)
