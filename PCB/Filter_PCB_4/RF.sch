EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 10
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
L Connector:Conn_Coaxial J1
U 1 1 5E2E993F
P 2250 4050
AR Path="/5E2E993F" Ref="J1"  Part="1" 
AR Path="/5E2D6D86/5E2E993F" Ref="J1"  Part="1" 
F 0 "J1" H 2250 4300 50  0000 C CNN
F 1 "Conn_Coaxial" H 2250 4200 50  0000 C CNN
F 2 "libs:SMA_generic_EdgeMount" H 2250 4050 50  0001 C CNN
F 3 " ~" H 2250 4050 50  0001 C CNN
	1    2250 4050
	-1   0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5E2E9945
P 2250 4250
AR Path="/5E2E9945" Ref="#PWR0101"  Part="1" 
AR Path="/5E2D6D86/5E2E9945" Ref="#PWR01"  Part="1" 
F 0 "#PWR01" H 2250 4000 50  0001 C CNN
F 1 "GND" H 2255 4077 50  0000 C CNN
F 2 "" H 2250 4250 50  0001 C CNN
F 3 "" H 2250 4250 50  0001 C CNN
	1    2250 4250
	1    0    0    -1  
$EndComp
Wire Wire Line
	2450 4050 2850 4050
Wire Wire Line
	9100 4050 9500 4050
$Comp
L Connector:Conn_Coaxial J2
U 1 1 5E2E9A2C
P 9700 4050
AR Path="/5E2E9A2C" Ref="J2"  Part="1" 
AR Path="/5E2D6D86/5E2E9A2C" Ref="J2"  Part="1" 
F 0 "J2" H 9700 4300 50  0000 C CNN
F 1 "Conn_Coaxial" H 9700 4200 50  0000 C CNN
F 2 "libs:SMA_generic_EdgeMount" H 9700 4050 50  0001 C CNN
F 3 " ~" H 9700 4050 50  0001 C CNN
	1    9700 4050
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E2E9A32
P 9700 4250
AR Path="/5E2E9A32" Ref="#PWR0102"  Part="1" 
AR Path="/5E2D6D86/5E2E9A32" Ref="#PWR02"  Part="1" 
F 0 "#PWR02" H 9700 4000 50  0001 C CNN
F 1 "GND" H 9705 4077 50  0000 C CNN
F 2 "" H 9700 4250 50  0001 C CNN
F 3 "" H 9700 4250 50  0001 C CNN
	1    9700 4250
	1    0    0    -1  
$EndComp
Text Label 9500 4050 2    50   ~ 0
RFout
Text Label 2450 4050 0    50   ~ 0
RFin
$Sheet
S 2850 3750 550  400 
U 5E2F86AC
F0 "inv0" 50
F1 "inverter.sch" 50
F2 "Vpol" I L 2850 3850 50 
F3 "In" I L 2850 4050 50 
F4 "Out" O R 3400 4050 50 
$EndSheet
$Sheet
S 3800 3750 550  400 
U 5E2F8B0D
F0 "res0" 50
F1 "resonator.sch" 50
F2 "Vpol" I L 3800 3850 50 
F3 "In" I L 3800 4050 50 
F4 "Out" O R 4350 4050 50 
$EndSheet
$Sheet
S 4750 3750 550  400 
U 5E305E8C
F0 "inv1" 50
F1 "inverter.sch" 50
F2 "Vpol" I L 4750 3850 50 
F3 "In" I L 4750 4050 50 
F4 "Out" O R 5300 4050 50 
$EndSheet
$Sheet
S 5700 3750 550  400 
U 5E305E91
F0 "res1" 50
F1 "resonator.sch" 50
F2 "Vpol" I L 5700 3850 50 
F3 "In" I L 5700 4050 50 
F4 "Out" O R 6250 4050 50 
$EndSheet
$Sheet
S 6650 3750 550  400 
U 5E30679B
F0 "inv2" 50
F1 "inverter.sch" 50
F2 "Vpol" I L 6650 3850 50 
F3 "In" I L 6650 4050 50 
F4 "Out" O R 7200 4050 50 
$EndSheet
$Sheet
S 7600 3750 550  400 
U 5E3067A0
F0 "res2" 50
F1 "resonator.sch" 50
F2 "Vpol" I L 7600 3850 50 
F3 "In" I L 7600 4050 50 
F4 "Out" O R 8150 4050 50 
$EndSheet
$Sheet
S 8550 3750 550  400 
U 5E3071CF
F0 "inv3" 50
F1 "inverter.sch" 50
F2 "Vpol" I L 8550 3850 50 
F3 "In" I L 8550 4050 50 
F4 "Out" O R 9100 4050 50 
$EndSheet
Text HLabel 2750 3850 0    50   Input ~ 0
V0
Text HLabel 8450 3850 0    50   Input ~ 0
V0
Text HLabel 7500 3850 0    50   Input ~ 0
V1
Text HLabel 3700 3850 0    50   Input ~ 0
V1
Text HLabel 4650 3850 0    50   Input ~ 0
V2
Text HLabel 6550 3850 0    50   Input ~ 0
V2
Text HLabel 5600 3850 0    50   Input ~ 0
V3
Wire Wire Line
	2750 3850 2850 3850
Wire Wire Line
	3700 3850 3800 3850
Wire Wire Line
	4650 3850 4750 3850
Wire Wire Line
	5600 3850 5700 3850
Wire Wire Line
	6550 3850 6650 3850
Wire Wire Line
	7500 3850 7600 3850
Wire Wire Line
	8450 3850 8550 3850
Wire Wire Line
	3400 4050 3800 4050
Wire Wire Line
	4350 4050 4750 4050
Wire Wire Line
	5300 4050 5700 4050
Wire Wire Line
	6250 4050 6650 4050
Wire Wire Line
	7200 4050 7600 4050
Wire Wire Line
	8150 4050 8550 4050
$EndSCHEMATC
