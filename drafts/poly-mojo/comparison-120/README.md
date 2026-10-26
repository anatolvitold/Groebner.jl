# Groebner.jl upstream suites: local comparison

All 86 upstream problems in suites 1–3 were attempted with four backends (344 case/backend combinations). These are local measurements, not an upstream-reviewed result.

## Method

- Sources: contribution `aa1a0d617c54336d7867aef494647f657b147a86`, based on Groebner.jl upstream `751c90b0dd9415bab2b56980b0b34b59497ff856`; Poly Mojo `72c92234ba9f0b85a7d8d4476ccb61cb6573716e`. The existing Mojo 1.2.0 library packages and bridge were reused. No case recompiles Poly Mojo. Published package pin is still pending.
- Groebner.jl 0.10.12; Singular.jl 0.28.19 / Singular_jll 404.101.510+0; msolve 0.11.0; Julia 1.10.2. Exact dependencies are in `Manifest.toml`.
- The upstream backends call `Groebner.groebner(...; tasks=1)` and `Singular.std(...; complete_reduction=true)`. msolve uses `-g 2 -c 0`, additionally `-l 44` over finite fields. These results describe those settings; Singular is the upstream `std` backend.
- One case and one backend at a time; single-thread settings. Xeon Platinum 8573C VM, 4-CPU quota, 32 GiB memory. A common sampled process-group RSS guard stops cases above 16 GiB.
- Upstream `--timeout=120` plus its 10-second grace applies to the **whole case process**: loading/JIT, warm-up, three repetitions, and output. A timeout therefore does not prove that a single computation takes more than 120 seconds. No partial results are counted as completed.
- Timings are seconds, minimum of three repetitions. Julia and Poly Mojo perform one untimed warm-up. Conversion/loading and output are outside their compute timing. The unchanged msolve timing wraps each fresh executable, including startup, input parsing, and output; this particularly affects very small cases.
- Poly Mojo uses ordinary mode (`certify=False`, `trace=False`). The certified backend is excluded.
- After all timed passes, every completed output is parsed with Nemo and compared across backends using all coefficients and monomials, allowing basis permutation and nonzero scalar normalization to monic form. Canonical SHA-256 covers the complete normalized basis, field, and variable order. This is cross-implementation agreement; it is not a substitute for a proof certificate.
- Local runner compatibility/resource changes and scripts are retained here; the clean contribution and local PR draft are unchanged. No PR or issue was published.

## Completion counts

| Suite | Problems | Backend | Completed | Timeout | Memory limit | Error | Full-basis matches |
|---|---:|---|---:|---:|---:|---:|---:|
| GF(1073741827) | 35 | Groebner.jl | 26 | 9 | 0 | 0 | 25 |
| GF(1073741827) | 35 | Singular | 12 | 23 | 0 | 0 | 12 |
| GF(1073741827) | 35 | msolve | 26 | 9 | 0 | 0 | 25 |
| GF(1073741827) | 35 | Poly Mojo | 21 | 14 | 0 | 0 | 21 |
| GF(1031) | 27 | Groebner.jl | 20 | 7 | 0 | 0 | 20 |
| GF(1031) | 27 | Singular | 8 | 19 | 0 | 0 | 8 |
| GF(1031) | 27 | msolve | 20 | 7 | 0 | 0 | 20 |
| GF(1031) | 27 | Poly Mojo | 20 | 7 | 0 | 0 | 20 |
| QQ | 24 | Groebner.jl | 17 | 7 | 0 | 0 | 17 |
| QQ | 24 | Singular | 6 | 18 | 0 | 0 | 6 |
| QQ | 24 | msolve | 18 | 6 | 0 | 0 | 18 |
| QQ | 24 | Poly Mojo | 20 | 4 | 0 | 0 | 18 |

## Ordinary Poly Mojo speed on shared verified completions

Ratios are competitor compute time divided by ordinary Poly Mojo compute time. Above 1 means Poly Mojo is faster. Each comparison uses its own jointly completed, matching-output subset and excludes the trivial `dummy` case; these subsets may differ. Timeouts are excluded from ratios and remain visible above.

| Suite | Compared with | Shared cases | Poly Mojo faster | Geometric mean ratio |
|---|---|---:|---:|---:|
| GF(1073741827) | Groebner.jl | 20 | 13 | 1.02974× |
| GF(1073741827) | Singular | 9 | 9 | 14.9333× |
| GF(1073741827) | msolve | 20 | 18 | 1.91975× |
| GF(1031) | Groebner.jl | 19 | 9 | 0.974707× |
| GF(1031) | Singular | 7 | 7 | 24.9649× |
| GF(1031) | msolve | 19 | 19 | 3.04623× |
| QQ | Groebner.jl | 16 | 16 | 3.50054× |
| QQ | Singular | 5 | 5 | 13.3741× |
| QQ | msolve | 17 | 17 | 3.57983× |

## Which implementations finish the same problems?

All 86 cases, including the three trivial control cases. These counts describe outcomes under the common whole-process deadline, not standalone algorithm limits.

| Compared with Poly Mojo | Both completed | Only Poly Mojo completed | Only competitor completed | Neither completed |
|---|---:|---:|---:|---:|
| Groebner.jl | 58 | 3 | 5 | 20 |
| Singular | 24 | 37 | 2 | 23 |
| msolve | 59 | 2 | 5 | 20 |

## Validation exceptions

| Suite | Problem | Backend | Validation |
|---|---|---|---|
| GF(1073741827) | Cholera | Groebner.jl | no-cross-check |
| GF(1073741827) | katsura 12 | msolve | no-cross-check |
| QQ | eco 13 | Poly Mojo | no-external-reference |
| QQ | chandra 12 | Poly Mojo | no-external-reference |

All 210 completed outputs with another completed backend matched. The exceptions above each have only one completed backend, so no independent output comparison was available. A completion without such a comparison is reported separately from a matched result.

## All cases: GF(1073741827)

| Problem | Groebner.jl | Singular | msolve | Poly Mojo |
|---|---:|---:|---:|---:|
| dummy | 0.000213658 | 2.0108e-05 | 0.00802698 | 9.655e-06 |
| cyclic 7 | 0.0481298 | 1.58314 | 0.108307 | 0.0439882 |
| cyclic 8 | 0.787092 | timeout | 1.11737 | 0.726847 |
| cyclic 9 | timeout | timeout | timeout | timeout |
| katsura 10 | 0.575982 | timeout | 0.861967 | 0.911742 |
| katsura 11 | 3.8064 | timeout | 4.48515 | 7.19793 |
| katsura 12 | timeout | timeout | 31.9981 | timeout |
| katsura 13 | timeout | timeout | timeout | timeout |
| eco 11 | 0.215487 | timeout | 0.38985 | 0.20376 |
| eco 12 | 1.28226 | timeout | 1.99033 | 1.30611 |
| eco 13 | 5.58892 | timeout | 10.7883 | 9.49882 |
| eco 14 | timeout | timeout | timeout | timeout |
| noon 7 | 0.114542 | 0.389442 | 0.272962 | 0.0793447 |
| noon 8 | 0.899804 | 3.60924 | 1.4049 | 0.63808 |
| noon 9 | 7.38129 | timeout | 13.578 | 7.03029 |
| noon 10 | timeout | timeout | timeout | timeout |
| henrion 5 | 0.0015762 | 0.00937419 | 0.0104083 | 0.00122554 |
| henrion 6 | 0.0242184 | 0.318463 | 0.0510621 | 0.0193298 |
| henrion 7 | 1.47757 | timeout | 2.547 | 1.4407 |
| henrion 8 | timeout | timeout | timeout | timeout |
| reimer 6 | 0.026778 | 11.2736 | 0.0547441 | 0.0225036 |
| reimer 7 | 0.436259 | timeout | 0.924495 | 0.44735 |
| reimer 8 | 11.4397 | timeout | 23.4369 | 16.4961 |
| Cholera | 23.9986 | timeout | timeout | timeout |
| HIV2 | 0.889807 | timeout | 7.44349 | timeout |
| NFkB (w.) | timeout | timeout | timeout | timeout |
| Goodwin (w.) | timeout | timeout | timeout | timeout |
| yang1 | 11.0179 | timeout | 36.0084 | timeout |
| bayes148 | 14.6259 | 5.28609 | 30.5538 | timeout |
| gametwo2 | 8.32003 | timeout | 9.01498 | 7.95619 |
| jason210 | 3.02186 | 1.9211 | 4.73247 | 1.5535 |
| alea6 | 0.0751126 | 4.4272 | 0.116458 | 0.0560553 |
| mayr42 | timeout | timeout | timeout | timeout |
| BIOMD0000000103 | 0.115437 | 15.0784 | 0.199512 | timeout |
| BIOMD0000000123 | 0.556447 | 3.47786 | 1.22215 | 0.58016 |

## All cases: GF(1031)

| Problem | Groebner.jl | Singular | msolve | Poly Mojo |
|---|---:|---:|---:|---:|
| dummy | 8.0099e-05 | 3.9806e-05 | 0.00793893 | 9.25e-06 |
| cyclic 7 | 0.0384234 | 1.38174 | 0.132178 | 0.0374606 |
| cyclic 8 | 0.527138 | timeout | 1.88833 | 0.685363 |
| cyclic 9 | timeout | timeout | timeout | timeout |
| katsura 10 | 0.483687 | timeout | 2.45637 | 0.79326 |
| katsura 11 | 2.93071 | timeout | 18.3972 | 6.43939 |
| katsura 12 | timeout | timeout | timeout | timeout |
| katsura 13 | timeout | timeout | timeout | timeout |
| eco 11 | 0.188947 | timeout | 0.691023 | 0.188283 |
| eco 12 | 1.01139 | timeout | 4.91462 | 1.24444 |
| eco 13 | 4.69034 | timeout | 36.4394 | 9.54176 |
| eco 14 | timeout | timeout | timeout | timeout |
| noon 7 | 0.115189 | 0.400715 | 0.19048 | 0.0727119 |
| noon 8 | 1.12859 | 3.7626 | 1.32004 | 0.576602 |
| noon 9 | 11.2111 | timeout | 11.092 | 5.33934 |
| noon 10 | timeout | timeout | timeout | timeout |
| henrion 5 | 0.00165785 | 0.00871919 | 0.0109585 | 0.00101108 |
| henrion 6 | 0.0205646 | 0.306626 | 0.054683 | 0.0176683 |
| henrion 7 | 1.42626 | timeout | 3.27845 | 1.30471 |
| henrion 8 | timeout | timeout | timeout | timeout |
| reimer 6 | 0.0232966 | 10.4016 | 0.0551005 | 0.0194344 |
| reimer 7 | 0.348705 | timeout | 1.09942 | 0.382522 |
| reimer 8 | 9.42144 | timeout | 33.2582 | 13.332 |
| chandra 11 | 0.320879 | 19.1422 | 0.861307 | 0.336517 |
| chandra 12 | 1.45464 | timeout | 4.66538 | 1.86878 |
| chandra 13 | 9.62416 | timeout | 25.6084 | 10.6998 |
| chandra 14 | timeout | timeout | timeout | timeout |

## All cases: QQ

| Problem | Groebner.jl | Singular | msolve | Poly Mojo |
|---|---:|---:|---:|---:|
| dummy | 0.00070801 | 3.0759e-05 | 0.012059 | 6.6662e-05 |
| cyclic 7 | 0.475382 | timeout | 0.7516 | 0.176905 |
| cyclic 8 | 11.724 | timeout | 23.5981 | 5.44628 |
| katsura 9 | 1.698 | timeout | 1.93366 | 0.565223 |
| katsura 10 | 11.7603 | timeout | 15.664 | 4.57622 |
| katsura 11 | timeout | timeout | timeout | timeout |
| eco 10 | 0.293796 | timeout | 0.451762 | 0.0773655 |
| eco 11 | 2.36786 | timeout | 2.83407 | 0.502444 |
| eco 12 | 17.9428 | timeout | 21.9839 | 3.08262 |
| eco 13 | timeout | timeout | timeout | 23.2538 |
| noon 7 | 0.535427 | 0.815626 | 0.399866 | 0.139011 |
| noon 8 | 4.30734 | 9.00468 | 2.79761 | 1.0786 |
| noon 9 | timeout | timeout | 21.3395 | 9.30112 |
| henrion 6 | 0.439549 | 3.41708 | 0.429815 | 0.121994 |
| henrion 7 | timeout | timeout | timeout | timeout |
| reimer 6 | 0.181275 | timeout | 0.208046 | 0.0594926 |
| reimer 7 | 3.82588 | timeout | 4.36546 | 1.25718 |
| reimer 8 | timeout | timeout | timeout | timeout |
| chandra 9 | 0.461522 | 2.46809 | 0.490424 | 0.20125 |
| chandra 10 | 2.22177 | 19.7004 | 2.01507 | 0.774711 |
| chandra 11 | 8.97718 | timeout | 8.6293 | 2.90329 |
| chandra 12 | timeout | timeout | timeout | 14.0989 |
| chandra 13 | timeout | timeout | timeout | timeout |
| ipp | 24.0122 | timeout | 8.56028 | 2.2965 |

## Release correspondence

The v1.0.1 release (`650780c9335bc5687bb864a0778f242d6abbdf2f`) was published during this run. Its library source, build scripts, and lockfile are identical to the benchmark source commit; the original benchmark binary and environment were retained throughout.

Full precision is in [`results.csv`](results.csv) and [`results.json`](results.json). Validation details are in [`validation.tsv`](validation.tsv). The large raw inputs, outputs, timings, samples, and worker logs remain in the local comparison workspace; they are not included in this review branch. The retained orchestration scripts and Julia Manifest record that workspace, including absolute paths; adapt those paths and resolve the checkout path before reproducing the run. These scripts are review evidence, not part of the proposed upstream patch.
