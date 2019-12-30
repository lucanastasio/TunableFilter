README

# Tunable Filter with varactors
## Idea (our goals)
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
We started with the design of the ideal pass-band filter in ordert to verify that all the specifications can be satisfied. For the design we use the ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunts components in order to have a pass-band response.
