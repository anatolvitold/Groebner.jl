### Summary

This PR adds optional benchmark backends for [Poly Mojo](https://github.com/Spellbound-Mojo/poly_mojo) — a polynomial arithmetic and Gröbner basis library written in Mojo — to Groebner.jl's cross-software benchmark harness (`scripts/benchmark_different_software/`).

Two backends are introduced:
- `polymojo`: Computes standard reduced Gröbner bases over $\mathbb{Q}$ and native prime fields ($\text{degrevlex}$).
- `polymojocertified`: Includes certificate generation in the timed run and reports certificate verification in a dedicated supplementary column.

Existing backends require no Mojo installation. The PR also includes the small harness compatibility fixes listed below.

---

### What's Changed

1. **Poly Mojo Driver & Runner Integration**:
   - Bridges Poly Mojo’s public `polynomials.groebner` API following Groebner.jl's warm-up and minimum-of-repetitions protocol.
   - Compiles once and caches the binary across fields, variables, and certificate modes (`generate/polymojo/build.py`). Compilation and I/O are kept outside computation timers.
   - Pre-configured Pixi environment (`pixi.toml` / `pixi.lock`) installs precompiled packages (`poly_mojo 1.0.1`, `apn_mojo 1.0.2`, `mojo 1.2.0` on Linux x86-64) without requiring manual source builds.

2. **Validation & Testing Tooling**:
   - Added a full basis comparator (`validate.jl`) that checks coefficient fields, variable order, and all monomials/coefficients, with an optional `--normalize-monic` flag to compare against tools that emit primitive integer bases (e.g., msolve over $\mathbb{Q}$).
   - 74 focused assertions passed, covering build caching, adapter I/O, validation, and table reporting; ordinary, certified, and Groebner.jl suite-0 smoke runs also passed against the published packages.

3. **Harness Compatibility Fixes**:
   - Supports both `tasks=1` and `threaded=:no` across Groebner.jl versions.
   - Fixes `Groebner.Examples.chandran` references in suite 2.
   - Updates Singular's ring ordering keyword (`ordering=:degrevlex`).

---

### Quick Start

From the repository root on Linux x86-64, with Pixi and Julia installed (local validation used Julia 1.10.2):

```bash
# 1. Install and activate the pinned Poly Mojo environment
pixi install --locked --manifest-path scripts/benchmark_different_software/generate/polymojo/environment/pixi.toml
eval "$(pixi shell-hook --manifest-path scripts/benchmark_different_software/generate/polymojo/environment/pixi.toml --shell bash)"

# 2. Build the driver once against the precompiled library packages
export POLY_MOJO_DRIVER="$(python scripts/benchmark_different_software/generate/polymojo/build.py)"

# 3. Prepare a shared Julia environment using this checkout and PrettyTables 2
JULIA_NUM_PRECOMPILE_TASKS=1 julia scripts/benchmark_different_software/generate/polymojo/setup.jl
export BENCHMARK_JULIA_ENV="$PWD/.local/environment"
export JULIA_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1

# 4. Start with the two small smoke cases
julia scripts/benchmark_different_software/one_script_to_run_them_all.jl polymojo --suite=0 --nworkers=1 --nruns=2 --validate=no
julia scripts/benchmark_different_software/one_script_to_run_them_all.jl polymojocertified --suite=0 --nworkers=1 --nruns=2 --validate=no
```

For the full suites, use `--suite=1` for GF(1073741827), `--suite=2` for GF(1031), or `--suite=3` for QQ, with the desired repetition count and timeout. `--validate=no` disables the harness's fingerprint comparison; the certified backend still checks every certificate. See the [adapter README](https://github.com/anatolvitold/Groebner.jl/blob/feat/poly-mojo/scripts/benchmark_different_software/generate/polymojo/README.md) for output comparisons and timing details.

[Validation records](https://github.com/anatolvitold/Groebner.jl/blob/drafts/poly-mojo/drafts/poly-mojo/validation.md) distinguish the published-package checks from the earlier source-based full-suite measurements.
