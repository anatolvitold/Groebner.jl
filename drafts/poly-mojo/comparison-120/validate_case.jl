# Validation is outside the benchmark timings. msolve and Singular may emit
# primitive rational polynomials rather than monic ones; normalize scalar factors.
import Nemo, SHA
include("../scripts/benchmark_different_software/generate/layman_parser.jl")
function signature(path)
    ring, basis = parse_system_naive(read(path, String))
    canonical = sort([string(iszero(f) ? f : Nemo.divexact(f, Nemo.leading_coefficient(f))) for f in basis])
    descriptor = string(Nemo.characteristic(Nemo.base_ring(ring))) * "\n" * join(string.(Nemo.gens(ring)), ",") * "\n"
    # Julia 1.10 SHA on String/CodeUnits is very slow on large bases; a byte
    # vector produces the identical digest through its efficient copy path.
    digest = SHA.bytes2hex(SHA.sha256(Vector{UInt8}(codeunits(descriptor * join(canonical, "\n") * "\n"))))
    (length(basis), digest)
end
length(ARGS) % 2 == 0 || error("Expected BACKEND OUTPUT pairs")
for i in 1:2:length(ARGS)
    backend, path = ARGS[i:i+1]
    try
        count, digest = signature(path)
        println(backend, '\t', "parsed", '\t', count, '\t', digest)
    catch err
        println(backend, '\t', "parse-error", '\t', 0, '\t', "-")
        showerror(stderr, err, catch_backtrace())
        println(stderr)
    end
    flush(stdout)
    GC.gc()
end
