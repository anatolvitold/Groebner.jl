# Additional validation; the upstream SHA routine only retains its last basis polynomial.
import Nemo
include("../layman_parser.jl")

function full_basis_signature(text)
    ring, basis = parse_system_naive(text)
    field = string(Nemo.characteristic(Nemo.base_ring(ring)))
    variables = string.(Nemo.gens(ring))
    # The parser constructs canonical Nemo polynomials in the same explicit
    # degrevlex order. Compare every coefficient and monomial, allowing only a
    # permutation of the output basis, not omitted elements or rescaling.
    return (field, variables, sort(string.(basis)))
end

function compare_full_bases(reference, candidate)
    full_basis_signature(reference) == full_basis_signature(candidate)
end

if abspath(PROGRAM_FILE) == @__FILE__
    length(ARGS) >= 2 || error("usage: validate.jl REFERENCE_OUTPUT CANDIDATE_OUTPUT ...")
    reference = read(first(ARGS), String)
    for candidate in ARGS[2:end]
        compare_full_bases(reference, read(candidate, String)) || error("Full basis mismatch: $candidate")
        println("Full basis matches: $candidate")
    end
end
