#!/bin/sh
source ~/.bashrc

ori_dir=/home/rsh/Desktop/run_area/hs/recycled_ic/PVignored/
log_dir=./log
sp_dir=./sp_dir
run_dir=./run_dir
#sp_list=('NBUFFX2_RVT' 'NBUFFX2_LVT' 'NBUFFX2_HVT' \
#        'NBUFFX4_RVT' 'NBUFFX4_LVT' 'NBUFFX4_HVT' \
#        'NBUFFX8_RVT' 'NBUFFX8_LVT' 'NBUFFX8_HVT' \
#        'NBUFFX16_RVT' 'NBUFFX16_LVT' 'NBUFFX16_HVT' \
#        'NBUFFX32_RVT' 'NBUFFX32_LVT' 'NBUFFX32_HVT')
sp_list=('NBUFFX16_HVT' 'NBUFFX32_RVT' 'NBUFFX32_LVT' 'NBUFFX32_HVT')
#mkdir $sp_dir
#mkdir $log_dir

py ${ori_dir}/build_path.py >> ${log_dir}/build_path.py.log 2>&1

for sp_file in ${sp_list[@]}; do
#    hs -mt 20 -i ${sp_file}.sp -o ./${sp_file}/${sp_file}.lis &
    hs -mt 20 -i ${sp_dir}/${sp_file}.sp \
            -o ${run_dir}/${sp_file}/${sp_file}.lis &
    mt0_file=${run_dir}/${sp_file}/${sp_file}.mt0
    #monitor mt0 file content
    flag=0
    #max looping time is 3600 seconds, 1 hour 
    loop_time=60
    sleep_time=60
    while [ $flag -lt $loop_time ]; do
        flag=`expr $flag + 1`
        #mt0 file ready or not
        if grep -q "25.0000 1" ${mt0_file}; then
            echo "mt0 file is ready"
            date >> ${log_dir}/stim_trial.py.log 2>&1
            py stim_trial.py ${sp_file}  >> ${log_dir}/stim_trial.py.log 2>&1
#            if [[ $? != 0 ]]; then
            if [ $? -ne 0 ]; then
                PID_hs=$(ps -ef|grep -w 'hs'|grep -w ${sp_file}.sp| grep -v 'bash'|cut -c 10-15)
                kill ${PID_hs} &
                #repeat hs simulation until mt0 file is exact
                hs -mt 20 -i ${sp_dir}/${sp_file}.sp \
                        -o ${run_dir}/${sp_file}/${sp_file}.lis &
                echo "Repeat simulation."
            else
                echo "Exact mt0 file, simulation will go on."
                break
            fi
        else
            echo "mt0 file is not ready"
        fi
        sleep $sleep_time
        done
    done

mkdir ./mt0_dir
#if [ ! `grep -q 'error' ./NBUFFX*/*.lis` ] \
#    && [ ! `grep -q 'failed' ./NBUFFX*/*.mt0` ]; then
#    echo "No error found in lis file"
#else
#    echo "Error found in lis file"
#fi
#if [ ! `grep -q failed ./NBUFFX4_RVT/NBUFFX4_RVT.mt0` ]; then echo "No error found in lis file"; else echo "Error found in lis file"; fi

\cp -rf ${run_dir}/NBUFFX*/*.mt0 mt0_dir
\cp -rf ${run_dir}/NBUFFX*/*.mt0@ra mt0_dir
