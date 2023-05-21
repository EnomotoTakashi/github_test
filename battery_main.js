const fs = require('fs');
const { equivalent_circuit_model, fn_soc_ocv } = require('./battery_ecm');

const ah = 3;
let soc = 1;
let current = -3;
let dt = 1;
let v1 = 0;
const time_end = 3600;
let loop_num = Math.floor(time_end / dt);

let time_ = 0;
let ccv = fn_soc_ocv(soc);

let time_record_list = [0];
let ccv_record_list = [ccv];
let soc_record_list = [soc];

for (let i = 0; i < loop_num; i++) {
    let result = equivalent_circuit_model(soc, current, dt, v1, ah);
    soc = result.soc;
    ccv = result.ccv;
    hgen = result.hgen;
    v1 = result.v1;
    time_ += dt;
    time_record_list.push(time_);
    ccv_record_list.push(ccv);
    soc_record_list.push(soc);
}

// Prepare data for CSV
let csvContent = "Time,CCV,SOC\n";
for (let i = 0; i < time_record_list.length; i++) {
    csvContent += `${time_record_list[i]},${ccv_record_list[i]},${soc_record_list[i]}\n`;
}

// Write to CSV file
fs.writeFile("output.csv", csvContent, (err) => {
    if (err) {
        console.error(err);
    } else {
        console.log("CSV file has been saved!");
    }
});
