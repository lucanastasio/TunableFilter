# Tunable Filter with varactors
## Idea (our goal)
The idea of this project is to design a tunable filter in order to move the resonance frequency with the usage of varactors. The varactors are used in place of the capacitors in resonators thanks of the property to vary their capacitance as a function of the voltage applied across their terminals. So the varactor is the tuning component in this project. The use of this component will be explained in the following notes.

## Design specifications
The design specifications used in the design of this filter are the following:
- ***Type of Filter:*** band-pass
- ***Type of Response:*** Chebyshev (equi-ripple)
- ***Order of the filter:*** Third Order
- ***Resonant frequencies:***
    - $f_0$
    - $f_1$
    - $f_2$

- ***Bandwitdh:*** (constant for all resonant frequencies)
- ***Ports Impedances:*** $Z_0=50\Omega$
- ***Ripple Level:*** $Ar=0.5\,dB$

    
## Design of the ideal Filter
We started with the design of the ideal pass-band filter in order to verify that all the specifications can be satisfied. For the design we use the ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunts components in order to have a pass-band response. The schematic of the ideal pass-band filter is the following:

![Ideal pass-band filter](images/Ideal_Reference_Filter.PNG  "Ideal pass-band filter")

These are the formulas used in our first design:
- $L1 = \frac{g_1 Z_0}{\Delta \omega_0}$
- $C1 = \frac{\Delta}{Z_0 g_1 \omega_0}$
- $L2 = \frac{\Delta Z_0}{\omega_0 g_2}$
- $C2 = \frac{g_2}{\Delta Z_0 \omega_0}$
- $L3 = \frac{g_3 Z_0}{\Delta \omega_0}$
- $C3 = \frac{\Delta}{Z_0 g_3 \omega_0}$

where:
- $g_m$ are the coefficients of the low-pass prototype filter for a third order Chebyshev filter 
- $\Delta$ is the fractional bandwidth at the chose resonant frequency
- $\omega_0$ is the angular frequency at the chosen resonant frequency

The written formulas take account of the impedence scaling and the frequency scaling since the low-pass prototype uses an angular frequency at the resonant frequency of $1 rad/sec$ and an impedence at the source of $Z_0=1 \Omega$.
The choice of the resonant frequency (hence the fractional bandwidth) is not specified at this point of the design because we use the tool tune of the simulator (AWR) to sweep resonant frequency in a chosen range of frequencies.

