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

![Ideal pass-band filter](images/Ideal_Reference_Filter.PNG  "Ideal pass-band filter")

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

In order to set an inductor value for the resonators, we used impedance inverters with the proper value of ***K*** (inverter parameter). The inductor of the resonators is called <img src="/tex/cc96eb8a40f81e8514147d06c9e8ad92.svg?invert_in_darkmode&sanitize=true" align=middle width=17.73978854999999pt height=22.465723500000017pt/> in the schematic and its value is not yet specified because we use it as a tunable value in order to find the best value to satify our needs. Thus in the schematic of the pass-band filter we added 4 impedance inverters like shown in the following image:

![Ideal pass-band filter with inverters](images/Ideal_filter_inverters.PNG  "Ideal pass-band filter with inverters")

The value of the capacitor of the resonators is set by the equation:

<p align="center"><img src="/tex/4243a7f1749971a1af6341d602d48112.svg?invert_in_darkmode&sanitize=true" align=middle width=391.0090734pt height=37.37361045pt/></p>

This equation allow us to have the proper value of <img src="/tex/93205c116b0f5c643ea55261e300e1f1.svg?invert_in_darkmode&sanitize=true" align=middle width=18.30139574999999pt height=22.465723500000017pt/> for the wanted resonat frequency.

The formulas used to compute the values of the ***K*** parameter of each inverter are the following:
- K for the impedence inverter at the source: <img src="/tex/be11f8c265dc6082e3cd07fe1aee9d24.svg?invert_in_darkmode&sanitize=true" align=middle width=120.01437524999999pt height=37.765414500000006pt/>
- K for the second impedence inverter: <img src="/tex/c3127375dad6e978852de8c9c4a8cb2d.svg?invert_in_darkmode&sanitize=true" align=middle width=85.28488649999998pt height=29.205422400000014pt/>
- K for the third impedence inverter: <img src="/tex/ed10587cf4afda6dd7de51a4040bf4f8.svg?invert_in_darkmode&sanitize=true" align=middle width=85.28488649999998pt height=29.205422400000014pt/>
- K for the impedence inverter at the load: <img src="/tex/72e869314f9771fa9b606fa3a25d0573.svg?invert_in_darkmode&sanitize=true" align=middle width=120.01437524999999pt height=37.765414500000006pt/>

where <img src="/tex/12d208b4b5de7762e00b1b8fb5c66641.svg?invert_in_darkmode&sanitize=true" align=middle width=19.034022149999988pt height=22.465723500000017pt/> is the source impedance (called <img src="/tex/db85bd6dfbbcc6817fc7960910b43296.svg?invert_in_darkmode&sanitize=true" align=middle width=17.77402769999999pt height=22.465723500000017pt/> at the beginning), <img src="/tex/55a8863546098e2e5191b038a8a61dbf.svg?invert_in_darkmode&sanitize=true" align=middle width=31.101665099999988pt height=22.465723500000017pt/> is the bandwidth expressed in terms of angular frequency, <img src="/tex/cc96eb8a40f81e8514147d06c9e8ad92.svg?invert_in_darkmode&sanitize=true" align=middle width=17.73978854999999pt height=22.465723500000017pt/> is the chosen inductance for the resonators of the filter, and <img src="/tex/681a37b53b66acbc455e39ca3e6f1c41.svg?invert_in_darkmode&sanitize=true" align=middle width=12.49148174999999pt height=14.15524440000002pt/> are the coefficients of the low-pass filter prototype.

At this point the impedance inverters are implemented by pieces of quarter-wavelength transmission lines. The range of working frequencies span from 0 to 1 GHz, so the physical length of the transmission lines results in a bigger board. To minimize the board dimensions we choose to implement the filter with only lumped elements, so an equivalent circuit for impedance inverters is required. For the 2 impedance inverters in the middle of the filter, the equivalent circuit is a T circuit formed by three capacitor where the shunt capacitor has a positive value of capacitance while the serires capacitors have a negative value of capacitance. Capacitors with negative capacitance are not physically possible but the use of this components are useful in the designing. Negative capacitors will be absorbed in the series with the capacitors of the resonators if the negative capacitors have absolute value capacitance greater than that of the resonator's capacitors.
For the impedance inverters at the source and at the load we have the problem that a negative capacitor is not absorbed. To solve this problem an other equivalent circuit is required for this two inverters impedance. This new equivalent circuit is used only for the inverter impedance at the source and at the load and it consists of a shunt positive capacitor and of a series negative capacitor.
The schematic where all the impedence inverters are replaced with their respective equivalent circuits is shown in the next figure:

![Ideal pass-band filter with equivalent circuits of inverter](images/Ideal_filter_lumped.PNG  "Ideal pass-band filter with equivalent circuits of inverters")

The formulas used to calculate the values of the capacitors are:

- For the impedence inverter at the source: 
    - shunt capacitor $C_{0i} = \frac{\sqrt{1-\left(\frac{K_0}{R_0}\right)^2}}{K_0 \omega_0}$
    - series capacitor $C_{s0i}=-C_{0i}-\frac{1}{\left(R_0 \omega_0\right)^2 C_{0i}}$
- For the second impedence inverter:
    - all the capacitors have the same value $C_{1i} =\frac{1}{\omega_0 K_1}$
- For the second impedence inverter:
    - all the capacitors have the same value $C_{2i} =\frac{1}{\omega_0 K_2}$
- For the impedence inverter at the load: 
    - shunt capacitor $C_{3i} = \frac{\sqrt{1-\left(\frac{K_3}{R_0}\right)^2}}{K_3 \omega_0}$
    - series capacitor $C_{s3i}=-C_{3i}-\frac{1}{\left(R_0 \omega_0\right)^2 C_{3i}}$

For the symmetry of the circuit we have that <img src="/tex/0f3182696059f04bb88a094b02cee4eb.svg?invert_in_darkmode&sanitize=true" align=middle width=81.05285099999999pt height=22.465723500000017pt/> and <img src="/tex/10525d96a26f5068692a7df2dcd060db.svg?invert_in_darkmode&sanitize=true" align=middle width=71.67699989999998pt height=22.465723500000017pt/>.

In the last step of the design of the idea pass-band filter the negative capacitors are absorbed by the positive capacitors of the resonators. The final circuit is the following:

![Final design of the ideal pass-band filter](images/Ideal_final_filter.PNG  "Final design of the ideal pass-band filter")

The capacitance of the capacitors are calculated using the classical formulas of the equivalent capacitance of capacitors in series, thus:

- <img src="/tex/991c8ed7d65b6e607cda3fe6a69e3994.svg?invert_in_darkmode&sanitize=true" align=middle width=133.29895589999998pt height=27.77565449999998pt/>
- <img src="/tex/644f92405f036ce592c443030ea1925c.svg?invert_in_darkmode&sanitize=true" align=middle width=127.97354789999999pt height=27.77565449999998pt/>
- <img src="/tex/10785af3428be1dc276bd4a75739d3dc.svg?invert_in_darkmode&sanitize=true" align=middle width=133.29895589999998pt height=27.77565449999998pt/>

For the symmetry of the circuit, <img src="/tex/d13451bc523f105bd0e1646ea245c0e3.svg?invert_in_darkmode&sanitize=true" align=middle width=59.34233579999999pt height=22.465723500000017pt/>.
We have to notice that the plus sign in front of <img src="/tex/418a9ab89262b4343c84da32780776d4.svg?invert_in_darkmode&sanitize=true" align=middle width=29.156666549999986pt height=22.465723500000017pt/> and <img src="/tex/53505c3bf70884fd3832e15e76936ea3.svg?invert_in_darkmode&sanitize=true" align=middle width=29.156666549999986pt height=22.465723500000017pt/> is due to the fact that the minus sign is inclued in their formulas.

The frequency response at the frequency test of 1GHz of the final design of the ideal filter (without varactor) is shown below for the ripple level of 0.5 dB and 3dB respectively:

![Frequency response 0.5dB](images/Freq_resp_ideal_05dB.png  "Frequency response of the ideal filter for 0.5dB ripple level")

![Frequency response 3dB](images/Freq_resp_ideal_3dB.png  "Frequency response of the ideal filter for 3dB ripple level")

## The tunable element: the varactor





