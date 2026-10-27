The cross-software benchmark runner can now run Poly Mojo on its existing rational and prime-field systems. `polymojo` measures ordinary reduced-basis computation; the separate optional `polymojocertified` backend includes proof generation and reports certificate verification in an additional column.

The bridge uses Poly Mojo's public API, exact coefficients, the input variable order, and degree reverse lexicographic order. It follows the runner's warm-up and minimum-of-repetitions protocol. It compiles once against installed packages and caches the executable across fields, variable counts, certificate modes, and setup invocation paths. Existing backends require no Mojo installation.

A checked-in Pixi manifest and lockfile install community-channel **Poly Mojo 1.0.1**, **APN Mojo 1.0.2**, and **Mojo 1.2.0** on Linux x86-64. No library source build is required. Input conversion, output serialization, compilation, and certificate verification are outside computation timers; certified computation includes certificate construction.

The contribution includes setup/cache tests, bridge and reporting tests, and an optional complete-basis comparator independent of the existing fingerprints. Strict comparison checks every coefficient and monomial; `--normalize-monic` accepts nonzero scalar multiples from reference tools such as msolve. Small compatibility fixes cover the current Groebner.jl single-thread API, suite-2 Chandra examples, and Singular's ordering keyword. Benchmark polynomial definitions and existing fingerprints are unchanged.

Validation:

- Fresh installation of `poly_mojo-1.0.1-hb0f4dca_0` and `apn_mojo-1.0.2-hb0f4dca_0`, without source-package overrides; bridge package hashes match the installed modules.
- 74 focused assertions: 8 setup/cache tests, 32 real-bridge checks, 15 complete-basis comparisons, and 19 runner/report checks. Repeated setup reuses the executable, including invocation through Pixi's relative task path.
- Suite-0 CLI smoke runs with ordinary Poly Mojo, certified Poly Mojo, and Groebner.jl; exact QQ and prime-field reference comparisons and certificate checks.
- Separately, an earlier source-based comparison attempted all 86 problems in suites 1–3 with four backends. Poly Mojo completed 61, Groebner.jl 63, msolve 64, and Singular `std` 26 under the upstream 120-second whole-case timeout plus 10-second grace. All 210 completed outputs with a completed peer matched after monic normalization. Poly Mojo's rational `eco 13` and `chandra 12` had no completed external peer.

[Validation records and the earlier comparison](https://github.com/anatolvitold/Groebner.jl/blob/drafts/poly-mojo/drafts/poly-mojo/validation.md) distinguish the installed-package checks from the source-based measurements. The full comparison was not rerun for this packaging step. Its timings are local measurements, and the upstream msolve timer includes process startup and I/O while library computation timers exclude conversion and output.
