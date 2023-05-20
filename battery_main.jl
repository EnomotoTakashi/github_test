include("battery_ecm.jl")

function main()
    ah = 3.0
    soc = 1.0
    current = -3.0
    dt = 1.0
    v1 = 0.0
    time_end = 3600.0
    loop_num = Int(time_end / dt)

    time_ = 0.0
    ccv = fn_soc_ocv(soc)

    time_record_list = [0.0]
    ccv_record_list = [ccv]
    soc_record_list = [soc]

    for i in 1:loop_num
        soc, ccv, hgen, v1 = equivalent_circuit_model(soc, current, dt, v1, ah)
        time_ += dt
        push!(time_record_list, time_)
        push!(ccv_record_list, ccv)
        push!(soc_record_list, soc)
    end

    open("result.csv", "w") do fout
        for i = 1:length(time_record_list)
            println(fout, "$(time_record_list[i]),$(soc_record_list[i]),$(ccv_record_list[i])")
        end
    end
end

main()
