# Validation record

Updated October 26, 2026 (America/New_York). This record covers precompiled
source packages with library source identical to GitHub v1.0.1. Validation of
the installed community-channel 1.0.1 package remains pending.

## Versions and artifacts

- Upstream base: `751c90b0dd9415bab2b56980b0b34b59497ff856` (Groebner.jl 0.10.12).
- Poly Mojo source: `72c92234ba9f0b85a7d8d4476ccb61cb6573716e`.
- Poly Mojo shared build: `ec17910c475346c48fe52accb564eeab`.
- GitHub v1.0.1: `650780c9335bc5687bb864a0778f242d6abbdf2f`; `src/`, build scripts,
  and lockfile match the benchmark source revision.
- Mojo 1.2.0 (`2016d0cd`), Julia 1.10.2, AbstractAlgebra 0.51.2,
  Nemo 0.57.1, PrettyTables 2.4.0.
- Singular.jl 0.28.19 / Singular_jll 404.101.510+0; msolve 0.11.0.
- Linux x86-64. The Julia archive's libopenlibm executable-stack flag had
  previously been cleared for compatibility with this environment's kernel.

The bridge was built once against the existing library packages and reused.
Its SHA-256 is `606f2f88baf75716fc6468601690dd0a81c86f0d4b920a1e5566dcb73d59b082`.
No library rebuild occurred. Earlier repeated setup and a simulated installed
`CONDA_PREFIX/lib/mojo` layout returned the same cached executable. That
simulation used links to source-built artifacts, not an actual channel install.

## Focused checks

The following checks were rerun while preparing the fork submission:

| Check | Passing assertions |
|---|---:|
| Python setup/cache | 7 |
| Real Mojo bridge: coefficients, fields, dimensions, modes, malformed input | 32 |
| Complete-basis comparator, including optional scalar normalization | 15 |
| Optional backends, suite-2 loading, and native reports | 19 |
| **Total** | **73** |

[Logs](checks/) are retained in this review branch. The new normalization checks
accept rational and finite-field scalar multiples while rejecting changed
polynomials, missing or duplicated elements, different fields, and variable
orders. Default strict comparison continues to reject rescaling.

Suite-0 CLI smoke runs passed in ordinary Poly Mojo, certified Poly Mojo, and
Singular modes, with one worker and two measured repetitions. Earlier Groebner.jl
suite-0 checks also passed. These smoke runs are integration checks, not performance
claims. The normalized comparison CLI matched the existing rational Cyclic 7
outputs from msolve and Poly Mojo without rerunning the algorithms.

The real bridge tests cover QQ; primes 7, 1031, and 1073741827; rational numerators
larger than 64 bits; 2-, 3-, 9-, and 17-variable inputs; both modes; and truncated
input rejection. Successful bases are compared in full against Groebner.jl.
Certified checks replay retained proof evidence and check the Gröbner criterion.
Cache tests cover discovery, missing dependencies, compiler versions, invalidation,
failed builds, and concurrent setup. Report tests include missing case results
and operation of other backends without a Mojo setting.

## All three upstream suites

[Full report and per-case data](comparison-120/README.md).

All 86 problems were attempted across four backends (344 combinations), using
ordinary Poly Mojo only. Runs were sequential with one thread and the upstream
120-second timeout plus 10-second grace for the entire case process, including
warm-up, three measured repetitions, and output. A sampled 16 GiB process-group
RSS guard applied to all backends. Recorded timings are minima of three.

| Backend | Completed | Timed out |
|---|---:|---:|
| Poly Mojo | 61 | 25 |
| Groebner.jl | 63 | 23 |
| msolve | 64 | 22 |
| Singular `std` | 26 | 60 |

No worker errors or memory-limit stops occurred. The driver hash stayed unchanged,
and no new cgroup OOM events occurred. All 210 completed outputs with another
completed backend matched after complete-basis monic normalization. Of Poly Mojo's
61 outputs, 59 matched peers; rational `eco 13` and `chandra 12` had no completed
external peer. Large-prime `Cholera` (Groebner.jl only) and `katsura 12` (msolve only)
likewise lack peer comparisons. These four completions are not independently
cross-checked and are excluded from shared-output timing ratios.

Post-run output validation was separate from timing. Three initial checks were
interrupted by a slow Julia SHA String input path. Only those output checks were
repeated using equivalent byte-vector hashing; all digests cover the same bytes.
No timed benchmark was repeated as part of that repair.

The runner's msolve timing includes process startup, parsing, and output; library
compute timers exclude conversion and output. Completion limits apply to the
whole process, not to each individual computation. These differences and all
failures/timeouts are retained in the report.

## Remaining installation check

Pin `poly_mojo==1.0.1` after community publication, generate the release lockfile,
and rerun the focused tests against a fresh installed package without source
fallbacks. Record the exact resolved package builds. The full-suite source results
remain valid evidence for that source revision; they are not an installed-package
benchmark and should not be relabeled as one.

The older bundled Groebner.jl 0.7 environment retains its original single-thread
call path but has not been revalidated. The tested submission target is the current
0.10.12 checkout. No broad compatibility claim is made for the older environment.

The owner has authorized submission after the package check. The separate
fingerprint issue and reference-fingerprint migration remain outside this PR.
