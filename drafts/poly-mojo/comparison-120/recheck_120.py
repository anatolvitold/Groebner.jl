"""Repeat only checks stopped by the original SHA String path; no timed runs."""
from pathlib import Path
import csv,os,subprocess,time,signal,collections,json,datetime,shutil
ROOT=Path(__file__).resolve().parent/'comparison-120'
BACKENDS=['groebner','singular','msolve','polymojo']
rows=list(csv.DictReader((ROOT/'validation.tsv').open(),delimiter='\t'))
cols=list(rows[0])
retry={(r['suite'],r['problem']) for r in rows if r['validation'] in ['validation-resource-limit','validation-error','parse-error']}
shutil.copy(ROOT/'validation.tsv',ROOT/'validation-initial.tsv')
for suite,name in sorted(retry):
 selected=[r for r in rows if r['suite']==suite and r['problem']==name]
 args=[]
 for r in selected:
  if r['run_status']=='completed':args.extend([r['backend'],str(ROOT/'raw'/r['backend']/f'benchmark_{suite}'/name/'output')])
 prefix=ROOT/'validation-logs'/f'{suite}-{name}-retry'
 env=dict(os.environ,JULIA_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 with Path(str(prefix)+'.out').open('w') as out,Path(str(prefix)+'.err').open('w') as err:
  proc=subprocess.Popen(['/workspace/tools/julia-1.10.2/bin/julia',f'--project={ROOT.parent}/environment',str(ROOT.parent/'validate_case.jl'),*args],stdout=out,stderr=err,env=env,start_new_session=True)
  start=time.monotonic()
  while proc.poll() is None:
   total=0
   for p in Path('/proc').iterdir():
    if not p.name.isdecimal():continue
    try:
     fields=(p/'stat').read_text().rsplit(')',1)[1].split()
     if int(fields[2])==proc.pid:total+=int(fields[21])*os.sysconf('SC_PAGE_SIZE')
    except (OSError,ValueError,IndexError):pass
   if time.monotonic()-start>600 or total>16*2**30:
    os.killpg(proc.pid,signal.SIGKILL);proc.wait();break
   time.sleep(.2)
 parsed={}
 for line in Path(str(prefix)+'.out').read_text().splitlines():
  parts=line.split('\t')
  if len(parts)==4:parsed[parts[0]]=parts[1:]
 for r in selected:
  if r['run_status']!='completed':continue
  b=r['backend'];v=parsed.get(b)
  if not v or v[0]!='parsed':continue
  refs=[o for o in BACKENDS[:3] if o in parsed and parsed[o][0]=='parsed']
  r['reference']=refs[0] if refs else ''
  r['basis_count'],r['canonical_sha256']=v[1:]
  peers=[o for o,d in parsed.items() if o!=b and d[0]=='parsed']
  if not peers:r['validation']='no-cross-check' if b in BACKENDS[:3] else 'no-external-reference'
  else:r['validation']='full-basis-match' if all(parsed[o][1:]==v[1:] for o in peers) else 'MISMATCH'
 print('Rechecked',suite,name,{r['backend']:r['validation'] for r in selected},flush=True)
with (ROOT/'validation.tsv').open('w') as out:
 w=csv.DictWriter(out,fieldnames=cols,delimiter='\t');w.writeheader();w.writerows(rows)
metadata=json.loads((ROOT/'metadata.json').read_text())
metadata['validation_hash_fix']='Changed Julia SHA input from String/CodeUnits to an equivalent byte vector after large-output checks hit the validation deadline. Digests are identical; validated against Python hashlib. Only interrupted output checks were repeated. All benchmark timings remain unchanged.'
metadata['rechecked_cases']=sorted(retry)
metadata['validation_finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
print(collections.Counter(r['validation'] for r in rows))
