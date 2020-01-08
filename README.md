# Tunable Filter with varactors
## Idea (our goal)
The idea of this project is the design of a tunable filter with variable resonance frequency. Achieving this would be possible using varactors. The varactors are used in place of the capacitors in resonators thanks to their abrupt juction that results in an high variation in capacitance with respect to the voltage applied across their terminals. So the varactor is the tuning component in this project. The use of this component will be explained in the following notes.

## Design specifications
The (approximate) design specifications used in the design of this filter are the following:
- ***Type of Filter:*** band-pass
- ***Type of Response:*** Chebyshev (equi-ripple)
- ***Order of the filter:*** Third Order
- ***Resonant frequency:*** <img src="/tex/be3bf702a3f3ea055627d3967282e21f.svg?invert_in_darkmode&sanitize=true" align=middle width=143.15300009999999pt height=22.465723500000017pt/> (adjustable)
- ***Bandwitdh:*** <img src="/tex/d4ddd504b100b5ece54261c069ee5f40.svg?invert_in_darkmode&sanitize=true" align=middle width=72.14616419999999pt height=24.65753399999998pt/> (adjustable)
- ***Ports Impedances:*** <img src="/tex/f5540f2a9de3058224089b503918d667.svg?invert_in_darkmode&sanitize=true" align=middle width=70.08416414999998pt height=22.465723500000017pt/>
- ***Ripple Level:*** <img src="/tex/57783d949426fabdcca898550ec66cdd.svg?invert_in_darkmode&sanitize=true" align=middle width=87.71305949999999pt height=22.831056599999986pt/> (adjustable)

## Design of the ideal Filter
The project started with the design of the ideal pass-band filter in order to verify that all the specifications can be satisfied. For the design, the method used was ***Insertion Loss Method*** taking the low-pass Filter prototype and changing the series and shunt components in order to have a pass-band response. Below is the schematic of the ideal pass-band filter:

![Ideal pass-band filter](images/Ideal_Reference_Filter.png  "Ideal pass-band filter")

Formulas used in the first design stage:
- <img src="/tex/cf296703d6117d58e3dd6bb05959f831.svg?invert_in_darkmode&sanitize=true" align=middle width=87.79483679999998pt height=29.205422400000014pt/>
- <img src="/tex/2f6ca6a0cdc2f6c2f50ee7f81132b9b5.svg?invert_in_darkmode&sanitize=true" align=middle width=101.67511529999999pt height=24.575218800000012pt/>
- <img src="/tex/c0de4b070309aba50fd55529404f84b7.svg?invert_in_darkmode&sanitize=true" align=middle width=89.41647329999999pt height=30.392597399999985pt/>
- <img src="/tex/30194512e918ffcf7ffaccea575432fc.svg?invert_in_darkmode&sanitize=true" align=middle width=103.70467634999997pt height=28.670654099999997pt/>
- <img src="/tex/46bc15fff8b24299bfde56aa0a067825.svg?invert_in_darkmode&sanitize=true" align=middle width=87.79483679999998pt height=29.205422400000014pt/>
- <img src="/tex/e101e293b5511de41bf6225c730c6fa2.svg?invert_in_darkmode&sanitize=true" align=middle width=101.67511529999999pt height=24.575218800000012pt/>

where:
- <img src="/tex/7d1b450a578433027da03cad276d2e39.svg?invert_in_darkmode&sanitize=true" align=middle width=19.50543209999999pt height=14.15524440000002pt/> : band-pass prototype filter coefficients, calculate as a third order Chebyshev filter [unitless]
- <img src="/tex/7e9fe18dc67705c858c077c5ee292ab4.svg?invert_in_darkmode&sanitize=true" align=middle width=13.69867124999999pt height=22.465723500000017pt/> : fractional bandwidth [%]
- <img src="/tex/747fe3195e03356f846880df2514b93e.svg?invert_in_darkmode&sanitize=true" align=middle width=16.78467779999999pt height=14.15524440000002pt/> : angular frequency [rad/s]

The above formulas take into account impedance scaling and frequency scaling since the low-pass prototype uses an angular frequency at the resonant frequency of <img src="/tex/9d2144b1e85e5e062a75470af0bee047.svg?invert_in_darkmode&sanitize=true" align=middle width=64.02991319999998pt height=24.65753399999998pt/> and a source impedance of <img src="/tex/4b83a89bf4988ab705715511ad637aff.svg?invert_in_darkmode&sanitize=true" align=middle width=61.864954799999985pt height=22.465723500000017pt/>.
The resonant frequency (hence the fractional bandwidth) is not specified at this point of the design, instead it's left as a parameter. Then simulation environment's tuner tool (AWR) allows sweeping the parameter in its range.

In order to set an arbitrary inductor value for the resonators, impedance inverters were used with a proper value of ***K*** (inverter parameter). The resonator inductor value is called <img src="/tex/cc96eb8a40f81e8514147d06c9e8ad92.svg?invert_in_darkmode&sanitize=true" align=middle width=17.73978854999999pt height=22.465723500000017pt/> in the schematic and its value is not yet determined, it's again a tunable value in order to obtain the best value which can be found as an off-the-shelf component. Thus, in the schematic of the pass-band filter, 4 impedance inverters were added, as shown in the following image:

![Ideal pass-band filter with inverters](images/Ideal_filter_inverters.PNG  "Ideal pass-band filter with inverters")

The resonator capacitor value is set by the equation:

<p align="center"><img src="/tex/4243a7f1749971a1af6341d602d48112.svg?invert_in_darkmode&sanitize=true" align=middle width=391.0090734pt height=37.37361045pt/></p>

The above equation gives the proper value of <img src="/tex/93205c116b0f5c643ea55261e300e1f1.svg?invert_in_darkmode&sanitize=true" align=middle width=18.30139574999999pt height=22.465723500000017pt/> for the desired resonat frequency.

Following are the formulas used to compute ***K*** parameters for each inverter:
- K for the impedence inverter at the source: <img src="/tex/f7b89c463688749918b041126c69ba21.svg?invert_in_darkmode&sanitize=true" align=middle width=120.01437524999999pt height=37.765414500000006pt/>
- K for the second impedence inverter: <img src="/tex/f7613bac00793b106441c9f09a620e9e.svg?invert_in_darkmode&sanitize=true" align=middle width=85.28488649999998pt height=29.205422400000014pt/>
- K for the third impedence inverter: <img src="/tex/302b7515d55ad845fca5b5ae5d0b536d.svg?invert_in_darkmode&sanitize=true" align=middle width=85.28488649999998pt height=29.205422400000014pt/>
- K for the impedence inverter at the load: <img src="/tex/73185b3c3800d2c2cf77e3ee60e93201.svg?invert_in_darkmode&sanitize=true" align=middle width=120.01437524999999pt height=37.765414500000006pt/>

where <img src="/tex/12d208b4b5de7762e00b1b8fb5c66641.svg?invert_in_darkmode&sanitize=true" align=middle width=19.034022149999988pt height=22.465723500000017pt/> is the source impedance, <img src="/tex/55a8863546098e2e5191b038a8a61dbf.svg?invert_in_darkmode&sanitize=true" align=middle width=31.101665099999988pt height=22.465723500000017pt/> is the bandwidth expressed in terms of angular frequency, <img src="/tex/cc96eb8a40f81e8514147d06c9e8ad92.svg?invert_in_darkmode&sanitize=true" align=middle width=17.73978854999999pt height=22.465723500000017pt/> is the desired resonator inductance, and <img src="/tex/681a37b53b66acbc455e39ca3e6f1c41.svg?invert_in_darkmode&sanitize=true" align=middle width=12.49148174999999pt height=14.15524440000002pt/> are the band-pass filter prototype coefficients.

At this point impedance inverters are implemented as quarter-wave long transmission lines. The range of working frequencies spans from 0 to 1 GHz, so the physical length of the transmission lines results in an unfeasible dimension for a printed circuit board. To minimize board dimensions, the most reasonable choice is to implement the filter with lumped elements only, so an equivalent circuit for impedance inverters is required. For the 2 impedance inverters in the middle of the filter, the equivalent circuit is a T circuit composed of three capacitors where the shunt capacitor has a positive capacitance while the serires capacitors have a negative capacitance. Capacitors with negative capacitance are not physically possible but the use of this component is useful in the theoric design phase. Negative capacitors will be "absorbed" by the series with resonator capacitors, but only if the negative capacitors have a capacitance (in magnitude) greater than the resonator's one.
However, negative capacitances of impedance inverters at source and load ports are not "absorbed". To solve this problem another equivalent circuit is required for those two special cases, it consists of a shunt positive capacitor and only one series negative capacitor.
The schematic where all the impedance inverters are replaced with their respective equivalent circuits is shown in the figure:

![Ideal pass-band filter with equivalent circuits of inverter](images/Ideal_filter_lumped.PNG  "Ideal pass-band filter with equivalent circuits of inverters")

The formulas used to calculate capacitor values are:

- Impedance inverter at the source: 
	- shunt capacitor <img src="/tex/51d3943b76434ae01c373d60ae7021fb.svg?invert_in_darkmode&sanitize=true" align=middle width=119.49824699999998pt height=65.42513010000002pt/>
	- series capacitor <img src="/tex/334145d17cc535c19724aee9d200d1d9.svg?invert_in_darkmode&sanitize=true" align=middle width=178.45430789999998pt height=27.77565449999998pt/>
- Second impedance inverter:
	- all capacitors have the same value <img src="/tex/356e534cd9558f5268910152e8f83023.svg?invert_in_darkmode&sanitize=true" align=middle width=79.82265389999999pt height=27.77565449999998pt/>
- Third impedance inverter:
	- all capacitors have the same value <img src="/tex/099f2c1e9990918a3bbeece632e7806a.svg?invert_in_darkmode&sanitize=true" align=middle width=79.82265389999999pt height=27.77565449999998pt/>
- Impedance inverter at the load: 
	- shunt capacitor <img src="/tex/505eff73a0d81b205722124c0b3b7f1a.svg?invert_in_darkmode&sanitize=true" align=middle width=119.49824699999998pt height=65.42513010000002pt/>
	- series capacitor <img src="/tex/53be8c63ebbc14a2a752c28813dfbdef.svg?invert_in_darkmode&sanitize=true" align=middle width=178.45430789999998pt height=27.77565449999998pt/>

Thanks to the symmetry of the circuit one has that <img src="/tex/0f3182696059f04bb88a094b02cee4eb.svg?invert_in_darkmode&sanitize=true" align=middle width=81.05285099999999pt height=22.465723500000017pt/> and <img src="/tex/10525d96a26f5068692a7df2dcd060db.svg?invert_in_darkmode&sanitize=true" align=middle width=71.67699989999998pt height=22.465723500000017pt/>.

As a last step of the design of the ideal pass-band filter, negative capacitors are "absorbed" by positive capacitors of the resonators. The final circuit is the following:

![Final design of the ideal pass-band filter](images/Ideal_final_filter.PNG  "Final design of the ideal pass-band filter")

Capacitances are calculated using the well-known formula for series capacitance, thus:

- <img src="/tex/991c8ed7d65b6e607cda3fe6a69e3994.svg?invert_in_darkmode&sanitize=true" align=middle width=133.29895589999998pt height=27.77565449999998pt/>
- <img src="/tex/644f92405f036ce592c443030ea1925c.svg?invert_in_darkmode&sanitize=true" align=middle width=127.97354789999999pt height=27.77565449999998pt/>
- <img src="/tex/10785af3428be1dc276bd4a75739d3dc.svg?invert_in_darkmode&sanitize=true" align=middle width=133.29895589999998pt height=27.77565449999998pt/>

As per the circuit symmetry, <img src="/tex/d13451bc523f105bd0e1646ea245c0e3.svg?invert_in_darkmode&sanitize=true" align=middle width=59.34233579999999pt height=22.465723500000017pt/>.
It may be noted that the plus sign in front of <img src="/tex/418a9ab89262b4343c84da32780776d4.svg?invert_in_darkmode&sanitize=true" align=middle width=29.156666549999986pt height=22.465723500000017pt/> and <img src="/tex/53505c3bf70884fd3832e15e76936ea3.svg?invert_in_darkmode&sanitize=true" align=middle width=29.156666549999986pt height=22.465723500000017pt/> is due to the fact that the minus sign is inclued in their formulas.

Frequency response at the test resonant frequency of 1GHz of the final design of the ideal filter (without varactor) is shown below for ripple levels of 0.5 dB and 3dB respectively:

![Frequency response 0.5dB](images/Freq_resp_ideal_05dB.png  "Frequency response of the ideal filter for 0.5dB ripple level")

![Frequency response 3dB](images/Freq_resp_ideal_3dB.png  "Frequency response of the ideal filter for 3dB ripple level")

## Adding tunable element: the varactor