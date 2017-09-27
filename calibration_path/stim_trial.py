#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
sys.path.append('/home/rsh/Desktop/run_area/hs/recycled_ic/PVignored/')
import string
import re

from build_path import path_gen
from build_path import stim_gen

def get_stage(input_file):
    input_handle=open(input_file,'r')
    line_list=input_handle.readlines()
    if re.search('targ',line_list[-1]):
        word = line_list[-1].split()
        num_list = re.findall(r'[\d]+',word[2])
        stage = int(num_list[0])
    return stage

def trial_range(input_file,stage):
    num_label=[]
    start=0
    stop=50
    width = len(str(stage)) + 1
    exact_flag=0

    input_handle=open(input_file,'r')
    line_list=input_handle.readlines()
    num_line=len(line_list)
    if num_line < 5:
        print 'invalid mt0 file\nstim.sp file will not be modified'
    else:
        print 'valid mt0 file'
    for line in line_list:
        word = line.split()
        #mt0 line #4
        if re.search('delay_sel',word[0]):
            for label in word[:-2]: #'temper' & 'alter#' ignored
                num_label.append(int(label[-width:]))
            start = num_label[0]
            stop = num_label[-1] + 1
            num_sel_range = stop - start
            print "'1' in last stimulus ranges from %d to %d"%(start,stop)
        elif re.match('failed',word[0]):
            return False
        #mt0 line #5
        elif re.match(r'[\d]\.[\d]{3}e\-[\d]{2}',word[0]):
            #string to float
            ori_data = map(string.atof,word[:-2]) #25.0000 & 1 ignored
            data = [second*1e9 for second in ori_data] #second to nano-second
            print "num_sel=%d, delay_calibration=%f"%(start,data[0])
            print "num_sel=%d, delay_calibration=%f"%(stop,data[-1])
            #delay=5 must in data range, or modify the selection range and length
            if 'failed' in data:
                print "Warning! 'failed' found in data"
                #shorten the selection range
                num_sel_range = num_sel_range/2
                stop = start + 10
            elif data[0] > 5:
                #stop remains original value to extend selection range
                start -= num_sel_range/2
                #shorten the length of calibration path
                if start < 0:
                    stage -= 5 #stage = stage - 5
                    start = 0
                    stop = 10
            elif data[-1] < 5:
                #start remains original value to extend selection range
                stop += num_sel_range/2
                #extend the length of calibration path
                if stop > stage:
                    stage += 5
                    stop = 50
                    start = 40
            elif 4.9 < data[-2] <= 5.0 and data[-1] >= 5.0:
                exact_flag=1 #exactly! inform shell to go on hspice simulation
            else:
                for i,delay in enumerate(data):
                    if 4.9 < delay < 5.0 and data[i+1] >= 5.0:
                        stop = num_label[i+1] + 1
                        #10 is an appropriate range, which could be modified
                        start = stop - 10
            print "'1' in next stimulus ranges from %d to %d"%(start,stop)
    input_handle.close()
    
    if exact_flag:
        return exact_flag
    else:
        return stage, start, stop

if __name__ == '__main__':
    #set up
    design = 'calibration_path'
    ori_dir = '/home/rsh/Desktop/run_area/hs/recycled_ic/PVignored/'
    run_dir = ori_dir+design+'/run_dir/'
    tar_dir = ori_dir+design+'/sp_dir/'
    tar_dir_list = ['./'+'NBUFFX8_RVT'+'/']
    ori_sp = ori_dir+design+'.sp'
    ori_stim = ori_dir+design+'_stim.sp'
    #initial pulse width of clock stimulus (ns)
    pw = 2
    #initial number of calibration path stage
    trial_stage = 50
    width = len(str(trial_stage)) + 1
#    start=0
#    stop=50
    if (len(sys.argv) < 2):
    #    buf_type=['NBUFFX2_RVT','NBUFFX2_LVT','NBUFFX2_HVT',\
    #              'NBUFFX4_RVT','NBUFFX4_LVT','NBUFFX4_HVT',\
    #              'NBUFFX8_RVT','NBUFFX8_LVT','NBUFFX8_HVT',\
    #              'NBUFFX16_RVT','NBUFFX16_LVT','NBUFFX16_HVT',\
    #              'NBUFFX32_RVT','NBUFFX32_LVT','NBUFFX32_HVT']
        buf_type = ['NBUFFX4_LVT']
    else:
        #sys.argv[1]=${sp_file} in run.sh
        buf_type = sys.argv[1:]
        
    for buf in buf_type:
        stim_file = tar_dir+buf+'_stim.sp'
        stage = get_stage(stim_file)
        mt0_file = run_dir+buf+'/'+buf+'.mt0'
        flag = trial_range(mt0_file,stage)
        if flag == 1:
            print 'Exact mt0 file!'
            sys.exit(0)
        else:
            trial_stage,trial_start,trial_stop = flag
            path_gen(ori_sp,tar_dir,buf,trial_stage)
            stim_gen(ori_stim,tar_dir,pw,buf,trial_stage,trial_start,trial_stop)
            sys.exit(1)
    


