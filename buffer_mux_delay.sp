BUFFER AND MULTIPLEXER AGING DELAY TEST
.include "/home/rsh/Desktop/project/b19/hs/scripts/saed32nm_rlh_vt_copy.spf"
.include "./buffer_mux_delay_stim.sp"
vvdd vdd 0 1.05
.global vss
vvss vss 0 0
.temp 25
 
.lib "/home/rsh/Desktop/project/b19/hs/scripts/saed32nm.lib" TT
.OPTIONS LIST NODE POST
.OPTION MEASFORM=1

.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_rvt.sp"
.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_lvt.sp"
.include "/home/rsh/Desktop/project/b19/hs/scripts/mosra_model_hvt.sp"

.mosra reltotaltime='60*30day' RelMode=0 simmode=2 lin=60

X2_R vdd vss X2_R/A X2_R/Y NBUFFX2_RVT
X2_L vdd vss X2_L/A X2_L/Y NBUFFX2_LVT
X2_H vdd vss X2_H/A X2_H/Y NBUFFX2_HVT

X4_R vdd vss X4_R/A X4_R/Y NBUFFX4_RVT
X4_L vdd vss X4_L/A X4_L/Y NBUFFX4_LVT
X4_H vdd vss X4_H/A X4_H/Y NBUFFX4_HVT

X8_R vdd vss X8_R/A X8_R/Y NBUFFX8_RVT
X8_L vdd vss X8_L/A X8_L/Y NBUFFX8_LVT
X8_H vdd vss X8_H/A X8_H/Y NBUFFX8_HVT

X16_R vdd vss X16_R/A X16_R/Y NBUFFX16_RVT
X16_L vdd vss X16_L/A X16_L/Y NBUFFX16_LVT
X16_H vdd vss X16_H/A X16_H/Y NBUFFX16_HVT

X32_R vdd vss X32_R/A X32_R/Y NBUFFX32_RVT
X32_L vdd vss X32_L/A X32_L/Y NBUFFX32_LVT
X32_H vdd vss X32_H/A X32_H/Y NBUFFX32_HVT

Xm2x1_R vdd vss Xm2x1_R/S0 Xm2x1_R/A1 Xm2x1_R/A2 Xm2x1_R/Y
+MUX21X1_RVT
Xm2x2_R vdd vss Xm2x2_R/A2 Xm2x2_R/S0 Xm2x2_R/A1 Xm2x2_R/Y
+MUX21X2_RVT
Xm4x1_R vdd vss Xm4x1_R/S0 Xm4x1_R/S1
+Xm4x1_R/A2 Xm4x1_R/A1 Xm4x1_R/A4 Xm4x1_R/A3 Xm4x1_R/Y
+MUX41X1_RVT
Xm4x2_R vdd vss Xm4x2_R/S0 Xm4x2_R/S1
+Xm4x2_R/A2 Xm4x2_R/A1 Xm4x2_R/A4 Xm4x2_R/A3 Xm4x2_R/Y
+MUX41X2_RVT

Xm2x1_L vdd vss Xm2x1_L/S0 Xm2x1_L/A1 Xm2x1_L/A2 Xm2x1_L/Y
+MUX21X1_LVT
Xm2x2_L vdd vss Xm2x2_L/A2 Xm2x2_L/S0 Xm2x2_L/A1 Xm2x2_L/Y
+MUX21X2_LVT
Xm4x1_L vdd vss Xm4x1_L/S0 Xm4x1_L/S1
+Xm4x1_L/A2 Xm4x1_L/A1 Xm4x1_L/A4 Xm4x1_L/A3 Xm4x1_L/Y
+MUX41X1_LVT
Xm4x2_L vdd vss Xm4x2_L/S0 Xm4x2_L/S1
+Xm4x2_L/A2 Xm4x2_L/A1 Xm4x2_L/A4 Xm4x2_L/A3 Xm4x2_L/Y
+MUX41X2_LVT

Xm2x1_H vdd vss Xm2x1_H/S0 Xm2x1_H/A1 Xm2x1_H/A2 Xm2x1_H/Y
+MUX21X1_HVT
Xm2x2_H vdd vss Xm2x2_H/A2 Xm2x2_H/S0 Xm2x2_H/A1 Xm2x2_H/Y
+MUX21X2_HVT
Xm4x1_H vdd vss Xm4x1_H/S0 Xm4x1_H/S1
+Xm4x1_H/A2 Xm4x1_H/A1 Xm4x1_H/A4 Xm4x1_H/A3 Xm4x1_H/Y
+MUX41X1_HVT
Xm4x2_H vdd vss Xm4x2_H/S0 Xm4x2_H/S1
+Xm4x2_H/A2 Xm4x2_H/A1 Xm4x2_H/A4 Xm4x2_H/A3 Xm4x2_H/Y
+MUX41X2_HVT

.END
