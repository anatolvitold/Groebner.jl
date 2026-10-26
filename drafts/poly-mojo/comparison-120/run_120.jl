include("../scripts/benchmark_different_software/one_script_to_run_them_all.jl")
root = joinpath(@__DIR__, "comparison-120")
backends = ("polymojo", "groebner", "msolve", "singular")
open(joinpath(root, "cases.tsv"), "w") do io
    println(io, "suite\tfield\tproblem")
    for suite in 1:3
        benchmark = get_benchmark_suite(suite)
        for (name, _) in benchmark.systems
            println(io, suite, '\t', benchmark.name, '\t', name)
        end
    end
end
open(joinpath(root, "passes.tsv"), "w") do passes
    println(passes, "suite\tbackend\tstatus\tfinished_utc")
    for suite in 1:3, backend in backends
        args = Dict{String,Any}("backend"=>backend, "suite"=>suite, "nruns"=>3,
            "nworkers"=>1, "timeout"=>120, "validate"=>"yes",
            "bpolymojo"=>ENV["POLY_MOJO_DRIVER"], "bmsolve"=>joinpath(@__DIR__, "msolve"))
        logfile = joinpath(root, "logs", "suite-$suite-$backend.log")
        println("Starting suite $suite / $backend at $(now(UTC)) UTC; log: $logfile")
        flush(stdout)
        status = "completed"
        open(logfile, "w") do io
            redirect_stdio(stdout=io, stderr=io) do
                with_logger(Logging.ConsoleLogger(io, Logging.Info)) do
                    try
                        check_args(args)
                        populate_benchmarks(args)
                        names = run_benchmarks(args)
                        collect_timings(args, names)
                    catch err
                        status = "runner-error"
                        showerror(io, err, catch_backtrace())
                        println(io)
                    end
                end
            end
        end
        println(passes, suite, '\t', backend, '\t', status, '\t', now(UTC))
        flush(passes)
        println("Finished suite $suite / $backend: $status at $(now(UTC)) UTC")
        flush(stdout)
        status == "completed" || error("Runner failed; inspect $logfile before continuing")
    end
end
println("All 12 upstream passes finished.")
