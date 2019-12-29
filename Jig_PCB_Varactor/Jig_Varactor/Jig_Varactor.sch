EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
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
L Device:D_Capacitance D1
U 1 1 5E07283E
P 4000 3500
F 0 "D1" V 3954 3579 50  0000 L CNN
F 1 "D_Capacitance" V 4045 3579 50  0000 L CNN
F 2 "Diode_SMD:D_SC-80_HandSoldering" H 4000 3500 50  0001 C CNN
F 3 "~" H 4000 3500 50  0001 C CNN
	1    4000 3500
	0    1    1    0   
$EndComp
$Comp
L Connector_Generic:Conn_02x01 J2
U 1 1 5E073431
P 5250 3450
F 0 "J2" V 5254 3530 50  0000 L CNN
F 1 "Conn_02x01" V 5345 3530 50  0000 L CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_2x01_P2.54mm_Vertical" H 5250 3450 50  0001 C CNN
F 3 "~" H 5250 3450 50  0001 C CNN
	1    5250 3450
	0    1    1    0   
$EndComp
$Comp
L pspice:CAP C1
U 1 1 5E07494C
P 4000 2600
F 0 "C1" H 4178 2646 50  0000 L CNN
F 1 "CAP" H 4178 2555 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric" H 4000 2600 50  0001 C CNN
F 3 "~" H 4000 2600 50  0001 C CNN
	1    4000 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 2850 4000 3150
$Comp
L Device:R R1
U 1 1 5E07665C
P 4500 3150
F 0 "R1" V 4293 3150 50  0000 C CNN
F 1 "R" V 4384 3150 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4430 3150 50  0001 C CNN
F 3 "~" H 4500 3150 50  0001 C CNN
	1    4500 3150
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 3150 4350 3150
Connection ~ 4000 3150
Wire Wire Line
	4000 3150 4000 3350
Wire Wire Line
	4650 3150 5250 3150
Wire Wire Line
	5250 3150 5250 3250
Wire Wire Line
	5250 3850 5250 3750
Wire Wire Line
	4000 3650 4000 3850
$Comp
L Device:R R2
U 1 1 5E0773C0
P 4500 3850
F 0 "R2" V 4293 3850 50  0000 C CNN
F 1 "R" V 4384 3850 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric" V 4430 3850 50  0001 C CNN
F 3 "~" H 4500 3850 50  0001 C CNN
	1    4500 3850
	0    1    1    0   
$EndComp
Wire Wire Line
	4000 3850 4350 3850
Wire Wire Line
	5250 3850 4650 3850
$Comp
L Connector:Conn_Coaxial J1
U 1 1 5E07ADA9
P 4000 2150
F 0 "J1" V 4237 2079 50  0000 C CNN
F 1 "Conn_Coaxial" V 4146 2079 50  0000 C CNN
F 2 "mylibs:SMA_generic_EdgeMount" H 4000 2150 50  0001 C CNN
F 3 " ~" H 4000 2150 50  0001 C CNN
	1    4000 2150
	0    -1   -1   0   
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E07BD02
P 4200 2150
F 0 "#PWR0102" H 4200 1900 50  0001 C CNN
F 1 "GND" H 4205 1977 50  0000 C CNN
F 2 "" H 4200 2150 50  0001 C CNN
F 3 "" H 4200 2150 50  0001 C CNN
	1    4200 2150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0101
U 1 1 5E07E728
P 4000 3850
F 0 "#PWR0101" H 4000 3600 50  0001 C CNN
F 1 "GND" H 4005 3677 50  0000 C CNN
F 2 "" H 4000 3850 50  0001 C CNN
F 3 "" H 4000 3850 50  0001 C CNN
	1    4000 3850
	1    0    0    -1  
$EndComp
Connection ~ 4000 3850
$Comp
L power:PWR_FLAG #FLG0101
U 1 1 5E07ED61
P 5200 2150
F 0 "#FLG0101" H 5200 2225 50  0001 C CNN
F 1 "PWR_FLAG" H 5200 2323 50  0000 C CNN
F 2 "" H 5200 2150 50  0001 C CNN
F 3 "~" H 5200 2150 50  0001 C CNN
	1    5200 2150
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0103
U 1 1 5E07F3D5
P 5200 2150
F 0 "#PWR0103" H 5200 1900 50  0001 C CNN
F 1 "GND" H 5205 1977 50  0000 C CNN
F 2 "" H 5200 2150 50  0001 C CNN
F 3 "" H 5200 2150 50  0001 C CNN
	1    5200 2150
	1    0    0    -1  
$EndComp
$EndSCHEMATC