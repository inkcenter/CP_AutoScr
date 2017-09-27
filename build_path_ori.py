#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

design = 'calibration_path'
sp_dir = './'+design+'/'
ori_sp = './'+design+'.sp'
ori_stim = './'+design+'_stim.sp'

num_stage = 50
num_sel_start = 20
num_sel_stop = 30
#num_sel_range = num_sel_stop - num_sel_start
#sim_stop = str(num_sel_range+10)+'ns'
#buf_type = 'NBUFFX32_HVT'
#pin_vol = 'v('+str(num_stage).zfill(3)+')'
#tar_sp = sp_dir+buf_type+'.sp'
#tar_stim = sp_dir+buf_type+'_stim.sp'

buf_type=['NBUFFX2_RVT','NBUFFX2_LVT','NBUFFX2_HVT',\
          'NBUFFX4_RVT','NBUFFX4_LVT','NBUFFX4_HVT',\
          'NBUFFX8_RVT','NBUFFX8_LVT','NBUFFX8_HVT',\
          'NBUFFX16_RVT','NBUFFX16_LVT','NBUFFX16_HVT',\
          'NBUFFX32_RVT','NBUFFX32_LVT','NBUFFX32_HVT']

tar_sp=[]
tar_stim=[]

for i in range(len(buf_type)):
    tar_sp.append(sp_dir+buf_type[i]+'.sp')
    tar_stim.append(sp_dir+buf_type[i]+'_stim.sp')

def path_gen(input_file,output_file,gate): 
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

    for i in range(num_stage):
        i_str=str(i)
        in_node=str(i).zfill(3)
        out_node=str(i+1).zfill(3)
        str1.append('X'+i_str+' vdd vss S'+i_str+' '+in_node+' '+out_node)
        #str1.append('X%s vdd vss S%s %s %s'%(i_str,i_str,in_node,out_node))
        str2.append(' calibration_stage'+'\n')
        #X0 vdd vss S0 000 001
        output_handle.writelines(str1[i]+str2[i])
    output_handle.write('.END')
    output_handle.close()

def stim_gen(input_file,output_file,start,stop):
    input_handle=open(input_file,'r')
    output_handle=open(output_file,'w')
    num_sel_range = stop - start
    sim_stop = str(num_sel_range+10)+'ns'
    pin_vol = 'v('+str(num_stage).zfill(3)+')'
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
#        elif len(word) == 9 and word[2] == 'v(050)':
#            new_line=line.replace('v(050)',pin_vol)
#            output_handle.write(new_line)
#            print 'v(050) is replaced with '+pin_vol
        else:
            output_handle.write(line)
    input_handle.close()
    
    for i in range(num_stage):
        #str1.append('vS'+str(i)+' S'+str(i)+' 0 PWL ')
        str1.append('vS%s S%s 0 PWL '%(i,i))
        if start-1 < i < stop:
            str2.append('(0ns 0 %sns 0 %sns 1.05) \n'%(i+0.999,i+1))
            #vS0 S0 0 PWL (0ns 0 0.999ns 0 1ns 1.05)
        else:
            str2.append('(0ns 0 %s 0) \n'%sim_stop)
            #vS49 S49 0 PWL (0ns 0 50ns 0)
        output_handle.writelines(str1[i]+str2[i])
    for i in range(num_sel_range):
        str3.append('.measure tran delay_sel_%s \n'%i)
        str4.append('+ trig v(000) val = 0.525 rise = %s \n'%(i+1))
        str5.append('+ targ %s val = 0.525 rise = %s \n'%(pin_vol,i+1))
        output_handle.writelines(str3[i]+str4[i]+str5[i])
    output_handle.close()


if not os.path.exists(sp_dir):
       os.makedirs(sp_dir)

for i,buf in enumerate(buf_type):
    path_gen(ori_sp,tar_sp[i],buf)
    stim_gen(ori_stim,tar_stim[i],num_sel_start,num_sel_stop)

