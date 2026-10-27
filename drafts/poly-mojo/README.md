# Poly Mojo benchmark contribution

**Status: published-package validation complete; ready for upstream submission.**

The implementation is on `feat/poly-mojo` in
[`anatolvitold/Groebner.jl`](https://github.com/anatolvitold/Groebner.jl/tree/feat/poly-mojo).
The prepared code commit is `a2b398491a72ec137f0fb61d216ca06dd27f642b`.
The proposed PR targets `sumiya11/Groebner.jl:master`, currently at
`751c90b0dd9415bab2b56980b0b34b59497ff856` (Groebner.jl 0.10.12).
This `drafts/poly-mojo` branch preserves review materials separately from the
implementation. Neither the draft materials nor benchmark results belong in the
upstream code diff.

The owner has authorized submission after `poly_mojo==1.0.1` reaches the community
channel and the pinned package passes fresh-installation checks. No additional
approval is needed for that submission. No upstream Groebner.jl PR or issue has
been opened.

- [PR title](title.txt) and [PR description](pull-request.md)
- [Validation record](validation.md)
- [Complete three-suite comparison](comparison-120/README.md)
- [Pinned release environment](https://github.com/anatolvitold/Groebner.jl/tree/feat/poly-mojo/scripts/benchmark_different_software/generate/polymojo/environment)
- [Remaining release and submission steps](submission.md)
- [Machine-readable state](submission-state.json)
- [Separate fingerprint issue draft](fingerprint-issue.md)

## Contribution scope

The code provides the ordinary `polymojo` backend and a separate optional
`polymojocertified` backend, a cached bridge built against installed packages,
exact interchange, certificate verification reporting, full-basis comparison,
tests, and setup instructions. The library is never rebuilt by the adapter.

Small compatibility fixes support the current Groebner.jl single-thread API,
suite-2 Chandra examples, and Singular's degree reverse lexicographic ordering
keyword. Full-basis comparison now optionally normalizes nonzero scalar factors
for reference tools that emit primitive integer polynomials. Its default remains
strict coefficient comparison.

The full comparison ran ordinary Poly Mojo only. All 86 upstream cases were
attempted with four backends, and every completed output with another completed
backend matched after monic normalization. Local process-group watchdogs,
progress changes, report tables, and fingerprint migrations are not part of the
upstream contribution.

## Package status

Community-channel Poly Mojo 1.0.1 and APN Mojo 1.0.2, both build `hb0f4dca_0`,
are installed and verified with Mojo 1.2.0 in the code branch's pinned environment.
All 74 focused checks and three suite-0 smoke runs pass. Setup discovers the
installed modules directly; no library source checkout or build is required.

The [release validation records](release-checks/) are separate from the earlier
source-based benchmark results, which were not rerun for this packaging step.

Commits use Anatoly Vitold Stankyavichyus `<anatolyvitold@outlook.com>`.
