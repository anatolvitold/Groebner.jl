# Poly Mojo benchmark contribution

**Status: prepared for the owner's fork; upstream submission awaits the community-channel Poly Mojo 1.0.1 package and its installation checks.**

The implementation is on `feat/poly-mojo` in
[`anatolvitold/Groebner.jl`](https://github.com/anatolvitold/Groebner.jl/tree/feat/poly-mojo).
The prepared code commit is `b91758e99feb4b9d0693d05f0b0a93812e60cbc8`.
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
- [Release environment template](release-environment.toml.in)
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

The GitHub v1.0.1 release is published, but that is distinct from the community
channel package. The channel update is
[modular/modular-community#431](https://github.com/modular/modular-community/pull/431).
At preparation time it is open, and the package manager lists Poly Mojo 1.0.0.
Do not use that older package: it targets Mojo 1.1 and APN Mojo 1.0.1.

The intended environment is Poly Mojo 1.0.1, Mojo 1.2.0, and APN Mojo 1.0.2.
The template is deliberately not a resolved manifest or lockfile. The current
tests and comparisons used precompiled source packages with library source
identical to v1.0.1; they do not substitute for testing the installed release.

Commits use Anatoly Vitold Stankyavichyus `<anatolyvitold@outlook.com>`.
