# Remaining submission steps

The owner has authorized publishing `feat/poly-mojo` and these review materials
to `anatolvitold/Groebner.jl`. They have also authorized the upstream PR after
Poly Mojo 1.0.1 is available from the community channel and the installed-package
checks pass. Do not request approval again for those steps.

1. Check the channel package, not just the GitHub tag or recipe PR:

   ```sh
   pixi search 'poly_mojo==1.0.1' --channel https://repo.prefix.dev/modular-community --platform linux-64 --json
   ```

   The publication PR is `modular/modular-community#431`. At preparation time
   it is open; the package index lists only 1.0.0. If package lookup fails, do not
   interpret a network error as proof of absence.

2. In the code branch, complete `release-environment.toml.in` with version
   `1.0.1` at `scripts/benchmark_different_software/generate/polymojo/environment/pixi.toml`.
   Resolve and commit the lockfile there. Use a new installation prefix and
   clear `POLY_MOJO_PATH`, `POLY_MOJO_DRIVER`, and `MOJO_COMMAND` overrides so setup
   discovers the installed modules in `lib/mojo`. Record the resolved build
   identifiers and package hashes, and confirm Mojo 1.2.0 / APN Mojo 1.0.2.

3. Build the bridge once using the installed packages. Repeat setup and confirm
   it returns the same executable without compilation. Run the tests and suite-0
   checks listed in the adapter README, including both supported certificate
   modes. Verify exact QQ and prime-field output agreement with Groebner.jl.
   No full-suite rerun is needed unless the package contents or checks reveal a
   material difference from the source build already benchmarked.

4. Update the adapter's installation instructions with the pinned environment,
   and replace the PR draft's pending-package section with actual installation
   evidence. Update `validation.md` and `submission-state.json`. Keep the large
   benchmark outputs and review-only materials off the contribution branch.

5. Confirm the upstream base, review the final diff, and push with commits under
   Anatoly Vitold Stankyavichyus `<anatolyvitold@outlook.com>`. Open the PR against
   `sumiya11/Groebner.jl:master` using the prepared title and body:

   ```sh
   gh pr create --repo sumiya11/Groebner.jl --base master \
     --head anatolvitold:feat/poly-mojo \
     --title 'Add optional Poly Mojo comparison backends' \
     --body-file /path/to/drafts/poly-mojo/pull-request.md
   ```

   Attach the created PR to the Codex task and record its URL. If GitHub denies
   this integration permission to open it, preserve the pushed branch and final
   description and provide a compare link; do not claim submission succeeded.

The separate fingerprint issue remains a draft. It is not part of this PR and
should not be submitted as an incidental action.
