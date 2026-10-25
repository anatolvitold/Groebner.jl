# Validation record

Prepared locally on October 25, 2026. This validates the contribution against
precompiled source packages; it is not a validation of a published release.

## Versions and artifacts

- Upstream base: `751c90b0dd9415bab2b56980b0b34b59497ff856` (Groebner.jl 0.10.12).
- Poly Mojo source: `72c92234ba9f0b85a7d8d4476ccb61cb6573716e`.
- Poly Mojo shared build: `ec17910c475346c48fe52accb564eeab`.
- Mojo 1.2.0 (`2016d0cd`), Julia 1.10.2, AbstractAlgebra 0.51.2,
  Nemo 0.57.1, PrettyTables 2.4.0.
- Linux x86-64. The old Julia archive's libopenlibm executable-stack flag had
  previously been cleared for compatibility with this environment's kernel.

The contribution compiled one bridge against the existing library packages.
No library rebuild was performed. Repeated setup and a simulated installed
`CONDA_PREFIX/lib/mojo` layout resolved the same cached executable. The latter
used links to the source-built artifacts; it does not replace a real package
installation test.

## Passing checks

| Check | Assertions |
|---|---:|
| Python setup/cache tests | 7 |
| Real Mojo bridge, coefficients, fields, dimensions, and modes | 32 |
| Complete-basis comparator | 7 |
| Optional backend, suite-2 loading, and native reports | 19 |
| **Total** | **65** |

The bridge tests cover QQ; primes 7, 1031, and 1073741827; rational numerators
larger than 64 bits; 2-, 3-, 9-, and 17-variable inputs; ordinary and certified
computation; and truncated input rejection. Every successful test basis is
compared in full against Groebner.jl, and certified runs replay and check proof
evidence.

The cache tests cover discovery from an installation prefix, missing dependencies,
wrong compiler versions, cache invalidation, failed builds, and concurrent setup.
The report tests cover both individual and combined verification columns, missing
case results, and operation of other backends without a Mojo setting.

The upstream suite-0 CLI is exercised in ordinary Poly Mojo, certified Poly Mojo,
and Groebner.jl modes, with one worker and two measured repetitions. These are
integration checks, not new comparative performance claims. Their native reports
and complete logs are retained in the local review packet.

## Earlier independent pilot

The preserved prototype used the unchanged upstream cases:

- Suite 1: dummy, Cyclic 7, Henrion 5, Reimer 6.
- Suite 3: dummy, Cyclic 7, Henrion 6, Reimer 6.

All 24 case/backend combinations completed without timeouts; all 16 Poly Mojo
outputs matched the complete Groebner.jl bases. This is subset evidence, not a
full-suite ranking. The contribution removes the pilot-only case filter and
retains no performance tables in its source changes.

## Before upstream submission

1. Select the intended published `poly_mojo` release, including its compatible
   dependency builds. Complete the release environment template and generate a
   lockfile; document the exact release in the contribution.
2. Install it in a fresh environment and rerun the checks above. Replace the
   source-build evidence with package-installation evidence in the PR description.
3. Broaden independent validation across suites 1–3 with explicit time/memory
   limits and retained failures/timeouts; cross-check with a second backend such
   as Singular. Loading the small-prime suite and checking its field is already
   covered, but its entire Gröbner workload has not been run here.
4. The compatibility path for the older bundled Groebner.jl 0.7 environment has
   been preserved but not separately exercised. Validate it if retained in the
   final submission; current Groebner.jl 0.10.12 is the tested reference.
5. Obtain approval to contact upstream or open the PR. A maintainer decision is
   still needed on the existing comparison runner as the preferred target.

The separate fingerprint issue has a verified two-basis reproducer. Its fix and
reference-fingerprint migration are outside this backend contribution.
