# Poly Mojo contribution draft

**Status: prepared locally for review; release pin and upstream submission pending.**

The implementation is on `feat/poly-mojo` at
`aa1a0d617c54336d7867aef494647f657b147a86`, in the local worktree
`/workspace/groebner-contribution`. Its upstream base is
`751c90b0dd9415bab2b56980b0b34b59497ff856`; the proposed PR target is
[`sumiya11/Groebner.jl:master`](https://github.com/sumiya11/Groebner.jl/tree/master).

This `drafts/poly-mojo` branch holds review material separately from the code.
Neither branch has been pushed. No upstream PR, issue, or message has been sent.
The original prototype and its pilot results remain in `/workspace/groebner-local`.

- [PR title](title.txt)
- [PR description](pull-request.md)
- [Validation and outstanding work](validation.md)
- [Release environment template](release-environment.toml.in)
- [Separate fingerprint issue draft](fingerprint-issue.md)

## Contribution scope

The code branch contains two optional backends, a package-aware cached bridge
build, exact input/output conversion, separate native verification reporting,
full-basis comparison, tests, and user instructions. It also contains small
compatibility changes for current Groebner.jl and loading suite 2. The pilot's
case-selection option, progress/log changes, result tables, and global
fingerprint behavior changes are excluded.

Validation passed 65 assertions and suite-0 integration runs for both Poly Mojo
modes and Groebner.jl. The library packages were reused; the bridge was built once
for this checkout. See the validation record for the exact scope and limitations.

## Release and approval gates

The intended published Poly Mojo version is still **TBD**. Do not substitute the
recipe's version number without verifying the actual package and its contents.
The `.toml.in` file is an explicit template, not a usable lockfile or a claimed
published release. After publication:

1. Fill the exact release version, add the completed environment to the code
   branch, and generate its lockfile.
2. Test the installed release in a fresh environment, broaden independent
   validation, and update the PR text and evidence.
3. Obtain approval before creating a public fork, contacting the maintainer, or
   submitting the PR. Confirm the preferred integration location with upstream
   when contact is authorized.

The fingerprint issue is a separate proposal. Its reproducible failure is
recorded, but no fingerprint migration is included in the backend PR.

## Local preservation

- `/workspace/groebner-integration.bundle`: implementation and draft branches.
- `/workspace/groebner-review/`: patch, logs, manifests, validation metadata,
  smoke outputs, and the earlier pilot's structured results.
- `/workspace/groebner-review.tar.gz`: portable copy of that evidence.
- `/workspace/groebner-integration-RESTORE.md`: restore commands.

Commits use Anatoly Vitold Stankyavichyus `<anatolyvitold@outlook.com>`.
