README

# Tunable Filter with varactors
## Idea (our goals)
The idea of this project is to design a tunable filter in order to move the resonance frequency with the usage of varactors. The varactors are used in place of the capacitors in resonators thanks of the property to vary their capacitance as a function of the voltage applied across thei terminals. So the varactor is the tuning component in this project. The use of this component will be explained in the following notes.

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
- ***Ports Impedances:*** <img src="/tex/cdc816ffd7b6d1b76a62ead02ba143e2.svg?invert_in_darkmode&sanitize=true" align=middle width=68.82416969999998pt height=22.465723500000017pt/>
- ***Ripple Level:*** <img src="/tex/57783d949426fabdcca898550ec66cdd.svg?invert_in_darkmode&sanitize=true" align=middle width=87.71305949999999pt height=22.831056599999986pt/>

    
## Design of the ideal Filter
We started with the design of the ideal pass-band filter in ordert to verify that all the specifications can be satisfied. For the design we use the ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunts components in ordert to have a pass-band response.
