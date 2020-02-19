"""
Tunable Filter GUI
Copyright (C) 2019 Luca Anastasio
<anastasio.lu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from scipy.special import chebyt
from numpy import linspace, log10, array, sqrt

class TunableFilter:

    def __init__(self, kind=None, response=None, order=None, ripple=None, center=None, fbw=None, lower=None, upper=None):
        """

        :param kind: {‘lowpass’, ‘highpass’, ‘bandpass’, ‘bandstop’}
        :param response: {'chebyshev', 'butterworth'}
        :param order: int
        :param ripple: float, dB
        """
        self.kind = kind
        self.response = response
        self.order = order
        self.ripple = ripple
        self.center = center
        self.fbw = fbw
        self.lower=lower
        self.upper=upper

    def setFractBW(self, fbw):
        #assert fbw < 0.0 or fbw > 100.0
        self.upper = self.center * (1 + fbw / 200.0)
        self.upper = self.center * (1 - fbw / 200.0)
        self.fbw = fbw

    def setCenterFreq(self, freq):
        self.upper = freq * (1 + self.fbw / 200.0)
        self.upper = freq * (1 - self.fbw / 200.0)
        self.center = freq

    def plot(self):
        freq = linspace(0.1e9, 1e9, 300)
        omega = (100.0/self.fbw) * ((freq/self.center) - (self.center/freq))
        #if self.response == 'chebyshev':
        Tn = chebyt(self.order)
        K = 10**(self.ripple/10.0) - 1
        Plr = 1 + K * Tn(omega)**2
        S21 = -10.0*log10(Plr)
        return array(freq), array(S21)
