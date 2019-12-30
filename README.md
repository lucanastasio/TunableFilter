README.tex

README

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
- ***Ports Impedances:*** <img src="/tex/cdc816ffd7b6d1b76a62ead02ba143e2.svg?invert_in_darkmode&sanitize=true" align=middle width=68.82416969999998pt height=22.465723500000017pt/>
- ***Ripple Level:*** <img src="/tex/57783d949426fabdcca898550ec66cdd.svg?invert_in_darkmode&sanitize=true" align=middle width=87.71305949999999pt height=22.831056599999986pt/>

    
## Design of the ideal Filter
We started with the design of the ideal pass-band filter in order to verify that all the specifications can be satisfied. For the design we use the ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunts components in order to have a pass-band response. The schematic of the ideal pass-band filter is the following:

![Ideal pass-band filter. First design](C:\Users\edamo\Documents\GitHub\TunableFilter\images "Ideal pass-band filter. First design.")

These are the formulas used in our first design:
- <img src="/tex/2397e8d4a73d25ea3da0986b488404c4.svg?invert_in_darkmode&sanitize=true" align=middle width=71.49763169999999pt height=30.392597399999985pt/>
- <img src="/tex/69b770b5f6ad24cd57d91c43adbd7b94.svg?invert_in_darkmode&sanitize=true" align=middle width=87.93189899999999pt height=28.670654099999997pt/>
- <img src="/tex/e28ff0fdf6f693f49c835c86054e8838.svg?invert_in_darkmode&sanitize=true" align=middle width=70.82224874999999pt height=29.205422400000014pt/>
- <img src="/tex/362ab4e30d1c9947b826e899d06fb60e.svg?invert_in_darkmode&sanitize=true" align=middle width=85.90233794999999pt height=24.575218800000012pt/>
- <img src="/tex/b89ed431637b6366fbef019ccb447228.svg?invert_in_darkmode&sanitize=true" align=middle width=71.49763169999999pt height=30.392597399999985pt/>
- <img src="/tex/62175fef705de4f5d580858f6a013925.svg?invert_in_darkmode&sanitize=true" align=middle width=87.93189899999999pt height=28.670654099999997pt/>

where:
- <img src="/tex/7d1b450a578433027da03cad276d2e39.svg?invert_in_darkmode&sanitize=true" align=middle width=19.50543209999999pt height=14.15524440000002pt/> are the coefficients of the low-pass prototype filter for a third order Chebyshev filter 
- <img src="/tex/7e9fe18dc67705c858c077c5ee292ab4.svg?invert_in_darkmode&sanitize=true" align=middle width=13.69867124999999pt height=22.465723500000017pt/> is the fractional bandwidth at the chose resonant frequency
- <img src="/tex/747fe3195e03356f846880df2514b93e.svg?invert_in_darkmode&sanitize=true" align=middle width=16.78467779999999pt height=14.15524440000002pt/> is the angular frequency at the chosen resonant frequency

The written formulas take account of the impedence scaling and the frequency scaling since the low-pass prototype uses an angular frequency at the resonant frequency of <img src="/tex/9d2144b1e85e5e062a75470af0bee047.svg?invert_in_darkmode&sanitize=true" align=middle width=64.02991319999998pt height=24.65753399999998pt/> and an impedence at the source of <img src="/tex/690c47c73832631f1ecfb4e5d2d66052.svg?invert_in_darkmode&sanitize=true" align=middle width=60.60496034999999pt height=22.465723500000017pt/>.
The choice of the resonant frequency (hence the fractional bandwidth) is not specified at this point of the design because we use the tool tune of the simulator (AWR) to sweep resonant frequency in a chosen range of frequencies.

