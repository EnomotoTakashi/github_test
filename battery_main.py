from battery_ecm_refactor import equivalent_circuit_model, fn_soc_ocv
import matplotlib.pyplot as plt

ah = 3
soc = 1
current = -3
dt = 1
v1 = 0
time_end = 3600
loop_num = int(time_end / dt)

time_ = 0
ccv = fn_soc_ocv(soc)

time_record_list = [0]
ccv_record_list = [ccv]
soc_record_list = [soc]

for i in range(loop_num):
    soc, ccv, hgen, v1 = equivalent_circuit_model(soc, current, dt, v1, ah)
    time_ += dt
    time_record_list.append(time_)
    ccv_record_list.append(ccv)
    soc_record_list.append(soc)

plt.plot(time_record_list, soc_record_list)
plt.show()

plt.plot(time_record_list, ccv_record_list)
plt.show()
