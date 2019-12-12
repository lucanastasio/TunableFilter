from smbus2 import SMBus, i2c_msg


class Channel:
	VREF_VDD = 0x0
	VREF_INT = 0x1
	GAIN_X1 = 0x0
	GAIN_X2 = 0x1
	pwr = {
		'POWER_ON': 0x0,
		'DOWN_1K': 0x1,
		'DOWN_100K': 0x2,
		'DOWN_500K': 0x3
	}

	def __init__(self, chsel, dac):
		self.voltage = 0.0
		self.code = 0
		self.codeChanged = False
		self.step = 0.0005
		self.chSel = chsel
		self.vrefValue = 2.048
		self.vrefSel = self.VREF_INT
		self.gainSel = self.GAIN_X1
		self.powerDownSel = self.pwr['POWER_ON']
		self.vrefChanged = False
		self.DAC = dac

	def Vref(self, value, update):
		pass

	def Vref2048(self, update):
		self.vrefValue = 2.048
		self.step = 0.0005
		self.voltage = self.code * self.step
		if update:
			self.DAC.Vref2048(self.chSel)

	def Vref4096(self, update):
		self.vrefValue = 4.096
		self.step = 0.001
		self.voltage = self.code * self.step
		if update:
			self.DAC.Vref4096(self.chSel)

	def VrefVdd(self, vdd, update):

		self.vrefValue = vdd
		self.step = vdd / 4096
		self.voltage = self.code * self.step
		if update:
			self.DAC.VrefVdd(self.chSel)


class MCP4728:
	cmd = {
		'FAST_WR': 0x00,
		'MULT_WR': 0x40,
		'SING_WR': 0x58,
		'SEQ_WR': 0x50,
		'SEL_VREF': 0x80,
		'SEL_GAIN': 0xC0,
		'SEL_PWR': 0xA0,
		'GEN_RST': 0x06,
		'GEN_WUP': 0x09,
		'GEN_UPD': 0x08,
		'GEN_ADD': 0x0C
	}

	def __init__(self, bus, address):
		self.address = address
		self.i2c = SMBus(bus)
		self.channel = {'A': Channel(0x0, self),
						'B': Channel(0x1, self),
						'C': Channel(0x2, self),
						'D': Channel(0x3, self)}

	def FastWrite(self):
		"""
		Writes all 4 channels' input data and power down registers (EEPROM not affected)
		NOTE: Doesn't update Vout (output data registers)
		"""
		data = []
		for c in 'ABCD':
			ch = self.channel[c]
			code = ch.code.to_bytes(2, 'big')
			data.append(self.cmd['FAST_WR'] | (ch.powerDownSel << 4) | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def MultiWrite(self, channels, update=True):
		"""
		Writes the selected channel(s) register(s) (EEPROM not affected)
		(including: data input register, gain, power down, Vref)
		Also determines if Vout gets updated or not

		:param channels: the channel(s) to write (e.g. 'ABCD' or 'ABC' or 'CD' or 'B' and so on)
		:type channels: str
		:param update: trigger an update of Vout if True, else just write register
		:type update: bool
		"""
		data = []
		for c in channels:
			ch = self.channel[c]
			code = ch.code.to_bytes(2, 'big')
			data.append(self.cmd['MULT_WR'] | (ch.chSel << 1) | int(not update))
			data.append((ch.vrefSel << 7) | (ch.powerDownSel << 5) | (ch.gainSel << 4) | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SequentialWrite(self, start, update=True):
		"""
		Writes registers and EEPROM starting from the given channel to channel D

		:param start: the starting channel (e.g. 'A' or 'B' or 'C' or 'D')
		:type start: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		data = [(self.cmd['SEQ_WR'] | self.channel[start].chSel << 1 | int(not update))]
		for c in range(ord(start), ord('D')+1):
			ch = self.channel[chr(c)]
			code = ch.code.to_bytes(2, 'big')
			data.append((ch.vrefSel << 7) | (ch.powerDownSel << 5) | (ch.gainSel << 4) | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def SingleWrite(self, channel, update=True):
		"""
		Writes registers and EEPROM only for the given channel

		:param channel: channel to write (e.g. 'A' or 'B' or 'C' or 'D')
		:type channel: str
		:param update: trigger an update of Vout if True, else just write registers and EEPROM
		:type update: bool
		"""
		ch = self.channel[channel]
		data = [(self.cmd['SING_WR'] | ch.chSel << 1 | int(not update))]
		code = ch.code.to_bytes(2, 'big')
		data.append((ch.vrefSel << 7) | (ch.powerDownSel << 5) | (ch.gainSel << 4) | code[0])
		data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def WriteAddress(self, newaddr):
		"""
		Unimplemented, requires dedicated pin
		"""
		pass

	def WriteVref(self):
		"""
		Writes Vref selection bits, does not affect EEPROM
		"""
		pass

	def WriteGain(self):
		"""
		Writes Gain selection bits, does not affect EEPROM
		"""
		pass

	def WritePower(self):
		"""
		Writes Power selection bits, does not affect EEPROM
		"""
		pass

	def ReadAll(self):
		"""
		Reads registers and EEPROM contents and saves values in current state
		"""
		msg = i2c_msg.read(self.address, 24)
		# in case it doesn't work, try to split in messages of 3 bytes each
		self.i2c.i2c_rdwr(msg)
		#msg.
		pass

	@staticmethod
	def GeneralCallReset():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallWakeUp():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallSoftwareUpdate():
		"""

		"""
		pass

	@staticmethod
	def GeneralCallReadAddress():
		"""

		"""
		pass
