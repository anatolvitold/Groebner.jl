#!/usr/bin/env python3
from pathlib import Path
import csv, json, math, collections, datetime, hashlib
ROOT=Path(__file__).resolve().parent/'comparison-120'
BACKENDS=['groebner','singular','msolve','polymojo']
LABELS={'groebner':'Groebner.jl','singular':'Singular','msolve':'msolve','polymojo':'Poly Mojo'}
FIELDS={1:'GF(1073741827)',2:'GF(1031)',3:'QQ'}
cases=list(csv.DictReader((ROOT/'cases.tsv').open(),delimiter='\t'))
validation={(int(r['suite']),r['problem'],r['backend']):r for r in csv.DictReader((ROOT/'validation.tsv').open(),delimiter='\t')}
rows=[]
for suite in [1,2,3]:
 for backend in BACKENDS:
  folder=ROOT/'raw'/backend/f'benchmark_{suite}'
  statuses={r['problem']:r for r in csv.DictReader((folder/'status.tsv').open(),delimiter='\t')}
  for c in [c for c in cases if int(c['suite'])==suite]:
   name=c['problem'];status=statuses.get(name,{'status':'missing'})
   r={'suite':suite,'field':FIELDS[suite],'problem':name,'backend':backend,**status}
   r.update({k:v for k,v in validation[suite,name,backend].items() if k not in ['suite','problem','backend','run_status']})
   timing=folder/name/'timings'
   r['compute_seconds']=None
   if status['status']=='completed' and timing.exists():
    t=dict(line.split(',',1) for line in timing.read_text().splitlines()[1:])
    r['compute_seconds']=float(t['total_time'])
   rows.append(r)
assert len(rows)==344
(ROOT/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
keys=list(dict.fromkeys(k for r in rows for k in r))
with (ROOT/'results.csv').open('w') as out:
 w=csv.DictWriter(out,fieldnames=keys);w.writeheader();w.writerows(rows)
by={(r['suite'],r['problem'],r['backend']):r for r in rows}
def fmt(x):return '—' if x is None else f'{x:.6g}'
def timing(r):return fmt(r['compute_seconds']) if r['status']=='completed' else r['status']
def eligible(a,b):
 return all(r['status']=='completed' and r['compute_seconds'] and r['validation']=='full-basis-match' for r in [a,b]) and a['canonical_sha256']==b['canonical_sha256']
def geom(values):return math.exp(sum(map(math.log,values))/len(values)) if values else None
lines=['# Groebner.jl upstream suites: local comparison','',
'All 86 upstream problems in suites 1–3 were attempted with four backends (344 case/backend combinations). These are local measurements, not an upstream-reviewed result.','',
'## Method','',
'- Sources: contribution `aa1a0d617c54336d7867aef494647f657b147a86`, based on Groebner.jl upstream `751c90b0dd9415bab2b56980b0b34b59497ff856`; Poly Mojo `72c92234ba9f0b85a7d8d4476ccb61cb6573716e`. The existing Mojo 1.2.0 library packages and bridge were reused. No case recompiles Poly Mojo. Published package pin is still pending.',
'- Groebner.jl 0.10.12; Singular.jl 0.28.19 / Singular_jll 404.101.510+0; msolve 0.11.0; Julia 1.10.2. Exact dependencies are in `Manifest.toml`.',
'- The upstream backends call `Groebner.groebner(...; tasks=1)` and `Singular.std(...; complete_reduction=true)`. msolve uses `-g 2 -c 0`, additionally `-l 44` over finite fields. These results describe those settings; Singular is the upstream `std` backend.',
'- One case and one backend at a time; single-thread settings. Xeon Platinum 8573C VM, 4-CPU quota, 32 GiB memory. A common sampled process-group RSS guard stops cases above 16 GiB.',
'- Upstream `--timeout=120` plus its 10-second grace applies to the **whole case process**: loading/JIT, warm-up, three repetitions, and output. A timeout therefore does not prove that a single computation takes more than 120 seconds. No partial results are counted as completed.',
'- Timings are seconds, minimum of three repetitions. Julia and Poly Mojo perform one untimed warm-up. Conversion/loading and output are outside their compute timing. The unchanged msolve timing wraps each fresh executable, including startup, input parsing, and output; this particularly affects very small cases.',
'- Poly Mojo uses ordinary mode (`certify=False`, `trace=False`). The certified backend is excluded.',
'- After all timed passes, every completed output is parsed with Nemo and compared across backends using all coefficients and monomials, allowing basis permutation and nonzero scalar normalization to monic form. Canonical SHA-256 covers the complete normalized basis, field, and variable order. This is cross-implementation agreement; it is not a substitute for a proof certificate.',
'- Local runner compatibility/resource changes and scripts are retained here; the clean contribution and local PR draft are unchanged. No PR or issue was published.','',
'## Completion counts','',
'| Suite | Problems | Backend | Completed | Timeout | Memory limit | Error | Full-basis matches |','|---|---:|---|---:|---:|---:|---:|---:|']
for suite in [1,2,3]:
 n=sum(int(c['suite'])==suite for c in cases)
 for b in BACKENDS:
  rr=[r for r in rows if r['suite']==suite and r['backend']==b];counts=collections.Counter(r['status'] for r in rr)
  matched=sum(r['validation']=='full-basis-match' for r in rr)
  lines.append(f"| {FIELDS[suite]} | {n} | {LABELS[b]} | {counts['completed']} | {counts['timeout']} | {counts['memory-limit']} | {counts['error']} | {matched} |")
lines+=['','## Ordinary Poly Mojo speed on shared verified completions','',
'Ratios are competitor compute time divided by ordinary Poly Mojo compute time. Above 1 means Poly Mojo is faster. Each comparison uses its own jointly completed, matching-output subset and excludes the trivial `dummy` case; these subsets may differ. Timeouts are excluded from ratios and remain visible above.','',
'| Suite | Compared with | Shared cases | Poly Mojo faster | Geometric mean ratio |','|---|---|---:|---:|---:|']
ratios=[]
for suite in [1,2,3]:
 for b in BACKENDS[:3]:
  vals=[]
  for c in cases:
   if int(c['suite'])!=suite or c['problem']=='dummy':continue
   a=by[suite,c['problem'],'polymojo'];other=by[suite,c['problem'],b]
   if eligible(a,other):vals.append(other['compute_seconds']/a['compute_seconds'])
  rec={'suite':suite,'competitor':b,'shared_cases':len(vals),'poly_mojo_faster':sum(v>1 for v in vals),'geometric_mean_competitor_over_poly':geom(vals)};ratios.append(rec)
  lines.append(f"| {FIELDS[suite]} | {LABELS[b]} | {len(vals)} | {rec['poly_mojo_faster']} | {fmt(geom(vals))}× |")
(ROOT/'speed-ratios.json').write_text(json.dumps(ratios,indent=2)+'\n')
lines+=['','## Which implementations finish the same problems?','',
'All 86 cases, including the three trivial control cases. These counts describe outcomes under the common whole-process deadline, not standalone algorithm limits.','',
'| Compared with Poly Mojo | Both completed | Only Poly Mojo completed | Only competitor completed | Neither completed |',
'|---|---:|---:|---:|---:|']
completion_pairs=[]
for b in BACKENDS[:3]:
 counts=collections.Counter()
 for c in cases:
  suite=int(c['suite']);name=c['problem']
  pair=(by[suite,name,'polymojo']['status']=='completed',by[suite,name,b]['status']=='completed')
  counts[pair]+=1
 rec={'competitor':b,'both_completed':counts[True,True],'only_poly_mojo_completed':counts[True,False],'only_competitor_completed':counts[False,True],'neither_completed':counts[False,False]}
 completion_pairs.append(rec)
 lines.append(f"| {LABELS[b]} | {rec['both_completed']} | {rec['only_poly_mojo_completed']} | {rec['only_competitor_completed']} | {rec['neither_completed']} |")
(ROOT/'completion-pairs.json').write_text(json.dumps(completion_pairs,indent=2)+'\n')
issues=[r for r in rows if r['status']=='completed' and r['validation']!='full-basis-match']
lines+=['','## Validation exceptions','']
if not issues:lines+=['All completed outputs matched another implementation after full-basis normalization.']
else:
 lines+=['| Suite | Problem | Backend | Validation |','|---|---|---|---|']
 for r in issues:lines.append(f"| {r['field']} | {r['problem']} | {LABELS[r['backend']]} | {r['validation']} |")
 if all(r['validation'] in ['no-cross-check','no-external-reference'] for r in issues):
  matched=sum(r['validation']=='full-basis-match' for r in rows)
  lines+=['',f'All {matched} completed outputs with another completed backend matched. The exceptions above each have only one completed backend, so no independent output comparison was available. A completion without such a comparison is reported separately from a matched result.']
for suite in [1,2,3]:
 lines+=['',f'## All cases: {FIELDS[suite]}','',
 '| Problem | Groebner.jl | Singular | msolve | Poly Mojo |',
 '|---|---:|---:|---:|---:|']
 for c in [c for c in cases if int(c['suite'])==suite]:
  name=c['problem'];rr=[by[suite,name,b] for b in BACKENDS]
  lines.append('| '+name+' | '+' | '.join(timing(r) for r in rr)+' |')
metadata=json.loads((ROOT/'metadata.json').read_text())
if 'release_note' in metadata:
 lines+=['','## Release correspondence','','The v1.0.1 release (`650780c9335bc5687bb864a0778f242d6abbdf2f`) was published during this run. Its library source, build scripts, and lockfile are identical to the benchmark source commit; the original benchmark binary and environment were retained throughout.']
lines+=['','Raw statuses, generated inputs, outputs, timings, samples, and worker logs are under [`raw/`](raw/). Full precision is in [`results.csv`](results.csv) and [`results.json`](results.json). Validation details are in [`validation.tsv`](validation.tsv).', '']
(ROOT/'README.md').write_text('\n'.join(lines))
print('Report written:',ROOT/'README.md')
print(json.dumps({'counts':{b:dict(collections.Counter(r['status'] for r in rows if r['backend']==b)) for b in BACKENDS},'validation':dict(collections.Counter(r['validation'] for r in rows)),'ratios':ratios},indent=2))
