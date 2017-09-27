#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

#generate buf.sp file
def path_gen(input_file,tar_dir,gate,stage):
    width = len(str(stage)) + 1
    output_file=tar_dir+gate+'.sp'
    input_handle=open(input_file,'r')
    output_handle=open(output_file,'w')
    str1=[]
    str2=[]
    
    for line in input_handle.readlines()[:-1]:
        word=line.split()
        if len(word) == 2 and word[1] == '"./calibration_path_stim.sp"':
            new_line=line.replace('calibration_path',gate)
            output_handle.write(new_line)
        elif len(word) == 6 and word[-1] == 'NBUFFX32_HVT':
            new_line=line.replace('NBUFFX32_HVT',gate)
            output_handle.write(new_line)
            print 'NBUFFX32_HVT is replaced with '+gate
        else:
            output_handle.write(line)
    input_handle.close()

    for i in range(stage):
        i_str=str(i)
        in_node=str(i).zfill(width)
        out_node=str(i+1).zfill(width)
        str1.append('X'+i_str+' vdd vss S'+i_str+' '+in_node+' '+out_node)
        #str1.append('X%s vdd vss S%s %s %s'%(i_str,i_str,in_node,out_node))
        str2.append(' calibration_stage'+'\n')
        #X0 vdd vss S0 000 001
        output_handle.writelines(str1[i]+str2[i])
    print 'Calibration path stage is %s'%(stage)
    output_handle.write('.END')
    output_handle.close()

#generate buf_stim.sp file
def stim_gen(input_file,tar_dir,duty,gate,stage,start,stop):
    #clock_cycle = 2 * pulse_width
    cycle = 2 * duty
    #number width 001~100
    width = len(str(stage)) + 1
    output_file=tar_dir+gate+'_stim.sp'
    input_handle=open(input_file,'r')
    output_handle=open(output_file,'w')
    num_sel_range = stop - start
    print 'Number of selected %s ranges from %s to %s'%(gate,start,stop)
#    sim_stop = str(num_sel_range+10)+'ns'
    sim_stop = str(cycle*num_sel_range+10)+'ns' #2ns
    pin_vol = 'v('+str(stage).zfill(width)+')'
    str1=[]
    str2=[]
    str3=[]
    str4=[]
    str5=[]
    
    for line in input_handle.readlines():
        word=line.split()
        if len(word) == 3 and word[0] == '.tran':
            new_line=line.replace('50ns',sim_stop)
            output_handle.write(new_line)
            print 'Simulation stop time is modified to '+sim_stop
        elif len(word) == 13 and word[0] == 'v000':
            word[-3] = str(duty)+'ns'
            word[-2] = str(cycle)+'ns'
            new_line=' '.join(word[:])
            output_handle.write(new_line)
            print 'Clock cycle 1ns is modified to '+str(cycle)+'ns'
        else:
            output_handle.write(line)
    input_handle.close()
    
    for i in range(stage):
        #str1.append('vS'+str(i)+' S'+str(i)+' 0 PWL ')
        str1.append('vS%s S%s 0 PWL '%(i,i))
        #trial of num_sel
        trial = cycle*(i-start) #2ns
        if start <= i <= stop:
            str2.append('(0ns 0 %sns 0 %sns 1.05) \n'%(trial+0.999,trial+1))
            #vS0 S0 0 PWL (0ns 0 0.999ns 0 1ns 1.05)
        elif i < start:
            str2.append('(0ns 1 %s 1) \n'%sim_stop)
            #vS49 S49 0 PWL (0ns 1 50ns 1)
        elif i > stop:
            str2.append('(0ns 0 %s 0) \n'%sim_stop)
            #vS49 S49 0 PWL (0ns 0 50ns 0)
        else:
            print False
        output_handle.writelines(str1[i]+str2[i])
    for i in range(num_sel_range):
        str3.append('.measure tran delay_sel_%s \n'%(str(i+start).zfill(width)))
        str4.append('+ trig v(000) val = 0.525 rise = %s \n'%(i+1))
        str5.append('+ targ %s val = 0.525 rise = %s \n'%(pin_vol,i+1))
        output_handle.writelines(str3[i]+str4[i]+str5[i])
    output_handle.close()

#These will only be executed when run directly
#These will not be executed when imported
if __name__ == '__main__':
    ori_dir = '/home/rsh/Desktop/run_area/hs/recycled_ic/PVignored/'
    design = 'calibration_path'
    tar_dir = ori_dir+design+'/sp_dir/'
    ori_sp = ori_dir+design+'.sp'
    ori_stim = ori_dir+design+'_stim.sp'
    #pulse width of clock stimulus (ns)
    pw = 2
    #number of calibration path stage
    num_stage = 50
    #initial number of selected buffer
    num_sel_start = 30
    #final number of selected buffer
    num_sel_stop = 40
    
    buf_type=['NBUFFX2_RVT','NBUFFX2_LVT','NBUFFX2_HVT',\
              'NBUFFX4_RVT','NBUFFX4_LVT','NBUFFX4_HVT',\
              'NBUFFX8_RVT','NBUFFX8_LVT','NBUFFX8_HVT',\
              'NBUFFX16_RVT','NBUFFX16_LVT','NBUFFX16_HVT',\
              'NBUFFX32_RVT','NBUFFX32_LVT','NBUFFX32_HVT']

    if not os.path.exists(tar_dir):
        os.makedirs(tar_dir)
    
    for i,buf in enumerate(buf_type):
        path_gen(ori_sp,tar_dir,buf,num_stage)
        stim_gen(ori_stim,tar_dir,pw,buf,num_stage,num_sel_start,num_sel_stop)

