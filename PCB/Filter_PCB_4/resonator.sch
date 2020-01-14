EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 4 10
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Device:L L?
U 1 1 5E300C42
P 4700 3850
AR Path="/5E300C42" Ref="L?"  Part="1" 
AR Path="/5E2D6D86/5E300C42" Ref="L?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E300C42" Ref="L1"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E300C42" Ref="L2"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E300C42" Ref="L3"  Part="1" 
F 0 "L3" V 4890 3850 50  0000 C CNN
F 1 "L0" V 4799 3850 50  0000 C CNN
F 2 "libs:Coilcraft_0603CS" H 4700 3850 50  0001 C CNN
F 3 "~" H 4700 3850 50  0001 C CNN
	1    4700 3850
	0    -1   -1   0   
$EndComp
Text Label 5950 3850 1    50   ~ 0
Vd-R
Text Label 5450 3750 1    50   ~ 0
Vd+
Connection ~ 5950 3850
Wire Wire Line
	5950 3850 6050 3850
Wire Wire Line
	5950 3850 5950 3950
Wire Wire Line
	5850 3850 5950 3850
Wire Wire Line
	5450 3250 5450 3150
Wire Wire Line
	5450 3850 5550 3850
Connection ~ 5450 3850
Wire Wire Line
	5450 3550 5450 3850
$Comp
L power:GND #PWR?
U 1 1 5E300C53
P 5950 4250
AR Path="/5E300C53" Ref="#PWR?"  Part="1" 
AR Path="/5E2D6D86/5E300C53" Ref="#PWR?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E300C53" Ref="#PWR06"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E300C53" Ref="#PWR010"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E300C53" Ref="#PWR014"  Part="1" 
F 0 "#PWR014" H 5950 4000 50  0001 C CNN
F 1 "GND" H 5955 4077 50  0000 C CNN
F 2 "" H 5950 4250 50  0001 C CNN
F 3 "" H 5950 4250 50  0001 C CNN
	1    5950 4250
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5E300C59
P 5950 4100
AR Path="/5E300C59" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E300C59" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E300C59" Ref="R4"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E300C59" Ref="R8"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E300C59" Ref="R12"  Part="1" 
F 0 "R12" H 6020 4146 50  0000 L CNN
F 1 "100k" H 6020 4055 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5880 4100 50  0001 C CNN
F 3 "~" H 5950 4100 50  0001 C CNN
	1    5950 4100
	1    0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5E300C5F
P 5450 3400
AR Path="/5E300C5F" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E300C5F" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E300C5F" Ref="R3"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E300C5F" Ref="R7"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E300C5F" Ref="R11"  Part="1" 
F 0 "R11" H 5520 3446 50  0000 L CNN
F 1 "100k" H 5520 3355 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 5380 3400 50  0001 C CNN
F 3 "~" H 5450 3400 50  0001 C CNN
	1    5450 3400
	1    0    0    -1  
$EndComp
$Comp
L Device:D_Capacitance_ALT D?
U 1 1 5E300C65
P 5700 3850
AR Path="/5E300C65" Ref="D?"  Part="1" 
AR Path="/5E2D6D86/5E300C65" Ref="D?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E300C65" Ref="D4"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E300C65" Ref="D8"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E300C65" Ref="D12"  Part="1" 
F 0 "D12" H 5700 4066 50  0000 C CNN
F 1 "BB202" H 5700 3975 50  0000 C CNN
F 2 "libs:D_SOD-523" H 5700 3850 50  0001 C CNN
F 3 "~" H 5700 3850 50  0001 C CNN
	1    5700 3850
	1    0    0    -1  
$EndComp
Text HLabel 5450 3150 1    50   Input ~ 0
Vpol
Text HLabel 4450 3850 0    50   Input ~ 0
In
Wire Wire Line
	4450 3850 4550 3850
Text HLabel 6050 3850 2    50   Output ~ 0
Out
Text Label 4950 3850 1    50   ~ 0
Vd-L
Connection ~ 4950 3850
Wire Wire Line
	4950 3850 4850 3850
Wire Wire Line
	4950 3850 4950 3950
Wire Wire Line
	5050 3850 4950 3850
$Comp
L power:GND #PWR?
U 1 1 5E1DCDA1
P 4950 4250
AR Path="/5E1DCDA1" Ref="#PWR?"  Part="1" 
AR Path="/5E2D6D86/5E1DCDA1" Ref="#PWR?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E1DCDA1" Ref="#PWR05"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E1DCDA1" Ref="#PWR09"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E1DCDA1" Ref="#PWR013"  Part="1" 
F 0 "#PWR013" H 4950 4000 50  0001 C CNN
F 1 "GND" H 4955 4077 50  0000 C CNN
F 2 "" H 4950 4250 50  0001 C CNN
F 3 "" H 4950 4250 50  0001 C CNN
	1    4950 4250
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R?
U 1 1 5E1DCDA7
P 4950 4100
AR Path="/5E1DCDA7" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E1DCDA7" Ref="R?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E1DCDA7" Ref="R2"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E1DCDA7" Ref="R6"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E1DCDA7" Ref="R10"  Part="1" 
F 0 "R10" H 5020 4146 50  0000 L CNN
F 1 "100k" H 5020 4055 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4880 4100 50  0001 C CNN
F 3 "~" H 4950 4100 50  0001 C CNN
	1    4950 4100
	-1   0    0    -1  
$EndComp
$Comp
L Device:D_Capacitance_ALT D?
U 1 1 5E1DCDAD
P 5200 3850
AR Path="/5E1DCDAD" Ref="D?"  Part="1" 
AR Path="/5E2D6D86/5E1DCDAD" Ref="D?"  Part="1" 
AR Path="/5E2D6D86/5E2F8B0D/5E1DCDAD" Ref="D3"  Part="1" 
AR Path="/5E2D6D86/5E305E91/5E1DCDAD" Ref="D7"  Part="1" 
AR Path="/5E2D6D86/5E3067A0/5E1DCDAD" Ref="D11"  Part="1" 
F 0 "D11" H 5200 4066 50  0000 C CNN
F 1 "BB202" H 5200 3975 50  0000 C CNN
F 2 "libs:D_SOD-523" H 5200 3850 50  0001 C CNN
F 3 "~" H 5200 3850 50  0001 C CNN
	1    5200 3850
	-1   0    0    -1  
$EndComp
Wire Wire Line
	5350 3850 5450 3850
$EndSCHEMATC
