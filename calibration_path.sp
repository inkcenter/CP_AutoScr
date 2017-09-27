CALIBRATION PATH AGING DELAY TEST
.include "/home/rsh/Desktop/project/b19/hs/scripts/saed32nm_rlh_vt_copy.spf"
.include "./calibration_path_stim.sp"
vvdd vdd 0 1.05
.global vss
vvss vss 0 0
.temp 25
 
.lib "/home/rsh/Desktop/project/b19/hs/scripts/saed32nm.lib" TT
.OPTIONS LIST NODE 
*.OPTIONS POST PROBE
*.PROBE tran v(S*) v(0*)
.OPTION MEASFORM=1

.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_rvt.sp"
.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_lvt.sp"
.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_hvt.sp"

*.mosra reltotaltime='60*30day' RelMode=0 simmode=2 lin=60
.mosra reltotaltime='6*30day' RelMode=0 simmode=2 lin=25

.subckt calibration_stage VDD VSS SEL A Y
Xbuf VDD VSS A tmp NBUFFX32_HVT
Xmux VDD VSS SEL A tmp Y MUX21X1_LVT
.ends

.END
