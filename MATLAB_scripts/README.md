Extraction of the function that gives the biasing voltage to be applied to the diode in order to obtain the desired capacitance:

* Import the datasheet in Engauge Digitizer
* Extract the curve points and export the data
* Import the data in MATLAB and andjust the units if necessary
* Open the curve fitting tool and use C data for X axis and V data for Y axis
* Select the appropriate fitting type and adjust the fit
* To verify that the fit corresponds to the graph in the datasheet, first export the fit to the MATLAB workspace as "fit", then:
~~~matlab
plot(fit)
% comment/don't use the following if the voltage isn't in log scale
set(gca, 'YScale', 'log')
% swap X and Y axes
view([90 -90])
~~~

For example, the resultinf function for BB202 was:
~~~matlab
V(C) = (p1*C^3 + p2*C^2 + p3*C + p4) / (C^4 + q1*C^3 + q2*C^2 + q3*C + q4)
p1 = -1312
p2 = -4819
p3 = 2384
p4 = 1.172e+04
q1 = 974.2
q2 = 5311
q3 = 1.313e+04
q4 = 1.153e+04
~~~
