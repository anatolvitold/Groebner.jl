#!/bin/bash
set -euo pipefail
cd /workspace/groebner-comparison
export PATH=/workspace/tools/julia-1.10.2/bin:$PATH
export BENCHMARK_JULIA_ENV=/workspace/groebner-comparison/.local/environment
export BENCHMARK_RESULTS=results/comparison-120
export BENCHMARK_PROGRESS=no
export BENCHMARK_MEMORY_LIMIT=17179869184
export JULIA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export POLY_MOJO_DRIVER=/workspace/groebner-contribution/scripts/benchmark_different_software/results/polymojo-build/80dff17dfaa10e22dd43c24f/driver
export MODULAR_HOME=/workspace/poly_mojo/.pixi/envs/default/share/max
julia .local/run_120.jl
python .local/validate_120.py
python .local/report_120.py
python - <<'PY'
from pathlib import Path
import json,hashlib,datetime
root=Path('.local/comparison-120')
m=json.loads((root/'metadata.json').read_text())
m['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
m['driver_sha256_after']=hashlib.sha256(Path(m['driver']).read_bytes()).hexdigest()
assert m['driver_sha256']==m['driver_sha256_after']
m['memory_events_after']=Path('/sys/fs/cgroup/memory.events').read_text()
(root/'metadata.json').write_text(json.dumps(m,indent=2)+'\n')
print('DONE: all timed passes, output comparisons, and report generation completed.',flush=True)
PY
