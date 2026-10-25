# Comparison fingerprints do not cover every basis polynomial

Draft only. This is a separate upstream correctness report, not part of the
Poly Mojo backend contribution. No issue has been submitted.

`scripts/benchmark_different_software/generate/basis_certificate.jl` accepts an
accumulator in `hash_polynomial(poly, h)` but does not use it. `get_certificate`
then overwrites `h` on each iteration. As a result, the fingerprint depends on
the last sorted normalized polynomial and the low byte of the basis size, rather
than all basis elements.

From the repository root, with the benchmark Julia environment active:

```julia
include("scripts/benchmark_different_software/generate/basis_certificate.jl")
a = "x,y\n0\nx+y,\ny^2-1\n"
b = "x,y\n0\nx-y,\ny^2-1\n"
ra, pa = parse_system_naive(a)
rb, pb = parse_system_naive(b)
@assert string.(pa) != string.(pb)
@assert compute_basis_validation_certificate(a) == compute_basis_validation_certificate(b)
```

Verified at upstream commit `751c90b0dd9415bab2b56980b0b34b59497ff856`, using Julia
1.10.2 and Nemo 0.57.1. Both return:

```text
440724ee198a3fdf0fe098373551799656ee0e4cfa03c77bed096d6699d1af0a
```

Suggested fix: hash an unambiguous encoding of the entire canonical basis,
including the field and ordered variables, and version the fingerprint format.
Regenerate expected fingerprints from independently checked reference outputs.
Also consider making `--validate=yes` report missing reference fingerprints
without creating them from the candidate under test; leave reference creation to
the explicit update mode.

The Poly Mojo draft uses an additional full-basis comparator while preserving
the existing fingerprint behavior. Changing stored fingerprints is a separate
review and migration decision.
