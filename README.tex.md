# Tunable Filter with varactors
## Idea (our goal)
The idea of this project is the design of a tunable filter with variable resonance frequency. Achieving this would be possible using varactors. The varactors are used in place of the capacitors in resonators thanks to their abrupt juction that results in an high variation in capacitance with respect to the voltage applied across their terminals. So the varactor is the tuning component in this project. The use of this component will be explained in the following notes.

## Design specifications
The (approximate) design specifications used in the design of this filter are the following:
- ***Type of Filter:*** band-pass
- ***Type of Response:*** Chebyshev (equi-ripple)
- ***Order of the filter:*** Third Order
- ***Resonant frequency:*** $500MHz--1GHz$ (adjustable)
- ***Bandwitdh:*** $1\%-10\%$ (adjustable)
- ***Ports Impedances:*** $R_0=50\Omega$
- ***Ripple Level:*** $Ar=0.5\,dB$ (adjustable)

## Design of the ideal Filter
The project started with the design of the ideal pass-band filter in order to verify that all the specifications can be satisfied. For the design, the method used was ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunt components in order to have a pass-band response. Below is the schematic of the ideal pass-band filter:

![Ideal pass-band filter](images/Ideal_Reference_Filter.png  "Ideal pass-band filter")

Formulas used in the first design stage:
- $L1 = \frac{\Delta R_0}{g_1 \omega_0} H$
- $C1 = \frac{g_1}{\Delta R_0 \omega_0} F$
- $L2 = \frac{g_2 R_0}{\Delta \omega_0} H$
- $C2 = \frac{\Delta}{R_0 g_2 \omega_0} F$
- $L3 = \frac{\Delta R_0}{g_3 \omega_0} H$
- $C3 = \frac{g_3}{\Delta R_0 \omega_0} F$

where:
- $g_m$ : band-pass prototype filter coefficients, calculate as a third order Chebyshev filter [unitless]
- $\Delta$ : fractional bandwidth [%]
- $\omega_0$ : angular frequency [rad/s]

The above formulas take into account impedance scaling and frequency scaling since the low-pass prototype uses an angular frequency at the resonant frequency of $1 rad/sec$ and a source impedance of $R_0=1 \Omega$.
The resonant frequency (hence the fractional bandwidth) is not specified at this point of the design, instead it's left as a parameter. Then simulation environment's tuner tool (AWR) allows sweeping the parameter in its range.

In order to set an arbitrary inductor value for the resonators, impedance inverters were used with a proper value of ***K*** (inverter parameter). The resonator inductor value is called $L_0$ in the schematic and its value is not yet determined, it's again a tunable value in order to obtain the best value which can be found as an off-the-shelf component. Thus, in the schematic of the pass-band filter, 4 impedance inverters were added, as shown in the following image:

![Ideal pass-band filter with inverters](images/Ideal_filter_inverters.PNG  "Ideal pass-band filter with inverters")

The resonator capacitor value is set by the equation:

\begin{equation}
C_0 = \frac{1}{L_0 \omega_0^2}
\end{equation}

The above equation gives the proper value of $C_0$ for the desired resonat frequency.

Following are the formulas used to compute ***K*** parameters for each inverter:
- K for the impedence inverter at the source: $K_0=\sqrt{\frac{R_0 L_0BW}{g_0 g_1}}$
- K for the second impedence inverter: $K_1=\frac{BW L_0}{g_1 g_2}$
- K for the third impedence inverter: $K_2=\frac{BW L_0}{g_2 g_3}$
- K for the impedence inverter at the load: $K_3=\sqrt{\frac{R_0 L_0 BW}{g_3 g_4}}$

where $R_0$ is the source impedance, $BW$ is the bandwidth expressed in terms of angular frequency, $L_0$ is the desired resonator inductance, and $g_i$ are the band-pass filter prototype coefficients.

At this point impedance inverters are implemented as quarter-wave long transmission lines. The range of working frequencies spans from 0 to 1 GHz, so the physical length of the transmission lines results in an unfeasible dimension for a printed circuit board. To minimize board dimensions, the most reasonable choice is to implement the filter with lumped elements only, so an equivalent circuit for impedance inverters is required. For the 2 impedance inverters in the middle of the filter, the equivalent circuit is a T circuit composed of three capacitors where the shunt capacitor has a positive capacitance while the serires capacitors have a negative capacitance. Capacitors with negative capacitance are not physically possible but the use of this component is useful in the theoric design phase. Negative capacitors will be "absorbed" by the series with resonator capacitors, but only if the negative capacitors have a capacitance (in magnitude) greater than the resonator's one.
However, negative capacitances of impedance inverters at source and load ports are not "absorbed". To solve this problem another equivalent circuit is required for those two special cases, it consists of a shunt positive capacitor and only one series negative capacitor.
The schematic where all the impedance inverters are replaced with their respective equivalent circuits is shown in the figure:

![Ideal pass-band filter with equivalent circuits of inverter](images/Ideal_filter_lumped.PNG  "Ideal pass-band filter with equivalent circuits of inverters")

The formulas used to calculate capacitor values are:

- Impedance inverter at the source: 
	- shunt capacitor $C_{0i} = \frac{\sqrt{1-\left(\frac{K_0}{R_0}\right)^2}}{K_0 \omega_0}$
	- series capacitor $C_{s0i}=-C_{0i}-\frac{1}{\left(R_0 \omega_0\right)^2 C_{0i}}$
- Second impedance inverter:
	- all capacitors have the same value $C_{1i} =\frac{1}{\omega_0 K_1}$
- Third impedance inverter:
	- all capacitors have the same value $C_{2i} =\frac{1}{\omega_0 K_2}$
- Impedance inverter at the load: 
	- shunt capacitor $C_{3i} = \frac{\sqrt{1-\left(\frac{K_3}{R_0}\right)^2}}{K_3 \omega_0}$
	- series capacitor $C_{s3i}=-C_{3i}-\frac{1}{\left(R_0 \omega_0\right)^2 C_{3i}}$

Thanks to the symmetry of the circuit one has that $C_{s3i}=C_{s0i}$ and $C0i=C_{3i}$.

As a last step of the design of the ideal pass-band filter, negative capacitors are "absorbed" by positive capacitors of the resonators. The final circuit is the following:

![Final design of the ideal pass-band filter](images/Ideal_final_filter.PNG  "Final design of the ideal pass-band filter")

Capacitances are calculated using the well-known formula for series capacitance, thus:

- $C_1=\frac{1}{\frac{1}{C_0}+\frac{1}{C_{s0i}}-\frac{1}{C_{1i}}}$
- $C_2=\frac{1}{\frac{1}{C_0}-\frac{1}{C_{1i}}-\frac{1}{C_{2i}}}$
- $C_3=\frac{1}{\frac{1}{C_0}+\frac{1}{C_{s3i}}-\frac{1}{C_{2i}}}$

As per the circuit symmetry, $C_1=C_3$.
It may be noted that the plus sign in front of $C_{s0i}$ and $C_{s3i}$ is due to the fact that the minus sign is inclued in their formulas.

Frequency response at the test resonant frequency of 1GHz of the final design of the ideal filter (without varactor) is shown below for ripple levels of 0.5 dB and 3dB respectively:

![Frequency response 0.5dB](images/Freq_resp_ideal_05dB.png  "Frequency response of the ideal filter for 0.5dB ripple level")

![Frequency response 3dB](images/Freq_resp_ideal_3dB.png  "Frequency response of the ideal filter for 3dB ripple level")

## Adding tunable element: the varactor