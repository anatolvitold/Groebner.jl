# Local resource accounting around the unchanged upstream benchmark operations.
const RUN_MEMORY_LIMIT = parse(Int, get(ENV, "BENCHMARK_MEMORY_LIMIT", string(16 * 2^30)))
const RUN_PAGE_SIZE = ccall(:getpagesize, Cint, ())

function process_group_rss(pid)
    total = 0
    for entry in readdir("/proc")
        all(isdigit, entry) || continue
        try
            record = read("/proc/$entry/stat", String)
            fields = split(record[findlast(')', record) + 1:end])
            parse(Int, fields[3]) == pid || continue
            total += parse(Int, fields[22]) * RUN_PAGE_SIZE
        catch
            # A process may exit between listing and reading its stat file.
        end
    end
    total
end

function stop_process_group(proc)
    ccall(:kill, Cint, (Cint, Cint), -proc.pid, Base.SIGKILL)
    wait(proc.julia_process)
end

function record_case(path, proc, status)
    elapsed = (time_ns() - proc.start_time) / 1e9
    open(path, "a") do io
        println(io, proc.problem_name, '\t', status, '\t', elapsed, '\t',
                proc.peak_rss[], '\t', proc.julia_process.exitcode, '\t',
                proc.julia_process.termsignal)
    end
    @info "Case finished" problem=proc.problem_name status elapsed peak_rss=proc.peak_rss[]
    flush(stdout)
end
