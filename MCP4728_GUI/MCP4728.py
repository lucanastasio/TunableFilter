from smbus2 import SMBus, i2c_msg


class Channel:
	PWR_ON = 0x0
	PWR_DN_1K = 0x1
	PWR_DN_100K = 0x2
	PWR_DN_500K = 0x3
	VREF_VDD = 0x0
	VREF_INT = 0x1
	GAIN_X1 = 0x0
	GAIN_X2 = 0x1
	UPD_OUT = 0x0
	NO_UPD_OUT = 0x1

	def __init__(self, channel, dac):
		self.voltage = 0.0
		self.code = 0
		self.codeChanged = False
		self.step = 0.0005
		self.channel = channel
		self.vrefValue = 2.048
		self.vrefSel = self.VREF_INT
		self.gainSel = self.GAIN_X1
		self.powerDownSel = self.PWR_ON
		self.update = self.UPD_OUT
		self.vrefChanged = False
		self.DAC = dac

	def Vref(self, value, update):
		pass

	def Vref2048(self, update):
		self.vrefValue = 2.048
		self.step = 0.0005
		self.voltage = self.code * self.step
		if update:
			self.DAC.Vref2048(self.channel)

	def Vref4096(self, update):
		self.vrefValue = 4.096
		self.step = 0.001
		self.voltage = self.code * self.step
		if update:
			self.DAC.Vref4096(self.channel)

	def VrefVdd(self, vdd, update):

		self.vrefValue = vdd
		self.step = vdd / 4096
		self.voltage = self.code * self.step
		if update:
			self.DAC.VrefVdd(self.channel)


class MCP4728:
	CMD_FAST_WR = 0x00
	CMD_MULT_WR = 0x40
	CMD_SING_WR = 0x58
	CMD_SEQ_WR = 0x50
	CMD_SEL_VREF = 0x80
	CMD_SEL_GAIN = 0xC0
	CMD_SEL_PWR = 0xA0

	def __init__(self, bus, address):
		self.address = address
		self.i2c = SMBus(bus)
		self.channel = {'A': Channel(0x0, self),
						'B': Channel(0x1, self),
						'C': Channel(0x2, self),
						'D': Channel(0x3, self)}

	def fastwrite(self):
		"""
		Writes all 4 channels' input data and power down registers
		NOTE: Doesn't update Vout (output data registers)
		"""
		data = []
		for ch in self.channel.values():
			code = ch.code.to_bytes(2, 'big')
			data.append(self.CMD_FAST_WR | (ch.powerDownSel << 4) | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)

	def multiwrite(self, channel):
		"""
		Writes the selected channel(s) register(s)
		(including: data input register, gain, power down, Vref)
		Also determines if Vout gets updated or not

		:param channel: the channel(s) to write
		:type channel: str
		"""
		data = []
		for c in channel:
			ch = self.channel[c]
			code = ch.code.to_bytes(2, 'big')
			data.append(self.CMD_MULT_WR | (ch.channel << 1) | ch.update)
			data.append((ch.vrefSel << 7) | (ch.powerDownSel << 5) | (ch.gainSel << 4) | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)