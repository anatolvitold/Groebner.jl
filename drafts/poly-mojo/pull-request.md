The cross-software benchmark runner can now run Poly Mojo on its existing rational
and prime-field polynomial systems. The optional `polymojo` backend measures
ordinary reduced-basis computation; `polymojocertified` includes retained proof
generation and reports certificate verification separately.

The bridge uses Poly Mojo's public API and preserves input coefficients, variable
order, degree reverse lexicographic order, and the runner's warm-up/minimum timing
protocol. A setup helper compiles one executable against installed, precompiled
packages and caches it across fields, variable counts, and modes. Existing
backends do not require Mojo.

Both the individual and combined reports expose verification time without adding
it to computation time or treating it as a fastest-computation candidate. Raw
per-repetition timings are retained. An optional complete-basis comparator checks
all coefficients and monomials against a reference backend, independently of the
runner's existing fingerprint files.

Small compatibility changes support a pre-instantiated Julia environment and
the current Groebner.jl single-thread keyword while retaining the older bundled
environment path. Four existing suite-2 Chandra calls use the current `Examples`
namespace; their polynomial definitions are unchanged. Existing fingerprint logic
is unchanged. The backend tests are optional and documented alongside setup.

Validation on Linux x86-64 with Mojo 1.2.0, Groebner.jl 0.10.12, and Julia 1.10.2:

- 7 Python setup/cache tests, including concurrent setup and failed compilation.
- 32 real-bridge assertions covering QQ, GF(7), GF(1031), GF(1073741827), large
  rational coefficients, 9/17 variables, both modes, and truncated input.
- 7 complete-basis comparison assertions.
- Both backends through the upstream suite-0 CLI, followed by 19 registration,
  suite-loading, and standard-report assertions, including missing results.
- An earlier eight-case upstream pilot completed in both Poly Mojo modes and
  Groebner.jl; all 16 Poly Mojo outputs matched complete reference bases. This was
  a selected subset, not a full-suite ranking.

## Draft release gate — remove only after completing it

This draft currently uses precompiled packages from Poly Mojo source revision
`72c92234ba9f0b85a7d8d4476ccb61cb6573716e`. The intended published package version
has not been selected or validated. Before submission, replace this section with
the exact community-channel release/build, add its pinned environment and lockfile,
and repeat the checks against that installed package in a fresh environment.

The broader suites and a second reference backend such as Singular remain
additional pre-submission validation. Submission requires the owner's approval.
