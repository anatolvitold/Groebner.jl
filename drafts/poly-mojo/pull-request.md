The existing cross-software benchmark runner can now run Poly Mojo on its
rational and prime-field systems. `polymojo` measures ordinary reduced-basis
computation; the separate optional `polymojocertified` backend includes proof
generation and reports certificate verification in an additional column.

The bridge calls Poly Mojo's public API, preserves exact coefficients, variable
order, and degree reverse lexicographic order, and follows the runner's warm-up
and minimum-of-repetitions timing protocol. It compiles once against installed,
precompiled packages and is cached across fields, variable counts, and modes.
Existing backends require no Mojo installation. Library compilation, input
conversion, and output serialization are outside computation timings.

The contribution includes setup/cache tests, bridge and reporting tests, and an
optional complete-basis comparator independent of the existing fingerprints.
Strict comparison checks every coefficient and monomial; `--normalize-monic`
also accepts nonzero scalar multiples from reference tools such as msolve.
Small compatibility changes support the current Groebner.jl single-thread API,
suite-2 Chandra examples, and Singular's ordering keyword. Benchmark system
definitions and existing fingerprint behavior are unchanged.

Validation used Linux x86-64, Mojo 1.2.0, Julia 1.10.2, and Groebner.jl 0.10.12:

- Setup/cache, exact interchange, both certificate modes, full-basis comparison,
  backend registration, and native reporting checks; suite-0 CLI smoke runs.
- All 86 problems from suites 1–3 with ordinary Poly Mojo, Groebner.jl, msolve
  0.11.0, and Singular.jl 0.28.19 (`Singular.std`). Runs were sequential with one
  thread, three measured repetitions, the upstream 120-second timeout plus its
  10-second grace for each whole case process, and a common 16 GiB RSS guard.
- Completed cases: Poly Mojo 61/86, Groebner.jl 63/86, msolve 64/86, Singular 26/86.
  Remaining cases timed out; there were no worker errors or memory-limit stops.
- All 210 completed outputs with a completed peer matched across their full
  bases after monic normalization. Of Poly Mojo's 61 completions, 59 matched a
  reference; rational `eco 13` and `chandra 12` had no completed external peer.

Detailed results, settings, validation exceptions, and reproducibility records
are preserved in the [review branch](https://github.com/anatolvitold/Groebner.jl/blob/drafts/poly-mojo/drafts/poly-mojo/comparison-120/README.md).
These are local results, not an upstream-reviewed performance ranking. In
particular, the upstream msolve timer includes process startup and I/O, while
library-backend computation timers exclude conversion and output.

## Pending package check — remove before submission

The intended package is community-channel `poly_mojo==1.0.1` with Mojo 1.2.0 and
APN Mojo 1.0.2. It is not yet available. Current evidence uses precompiled source
packages at `72c92234ba9f0b85a7d8d4476ccb61cb6573716e`; the library source, build
scripts, and lockfile are identical to the published GitHub v1.0.1 release.

Before opening this PR, add the resolved release environment and lockfile,
validate a clean package installation without source-package overrides, and
replace this section with the actual package/build and check results. Submission
after those checks has been authorized by the repository owner.
