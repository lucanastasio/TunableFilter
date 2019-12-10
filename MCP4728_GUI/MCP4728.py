from smbus2 import SMBus, i2c_msg

'''
class Vref:
	def __init__(self, Vdd):
		self.Int2V = 2.048
		self.Int4V = 4.096
		self.Vdd = Vdd

	def Vdd(self, Vdd):
		self.Vdd = Vdd
'''


class Channel:
	def __init__(self, channel, dac):
		self.voltage = 0.0
		self.code = 0
		self.step = 0.0005
		self.channel = channel
		self.vref = 2.048
		self.changed = False
		self.DAC = dac

	def Vref2048(self):
		self.vref = 2.048
		self.step = 0.0005
		self.voltage = self.code * self.step
		self.DAC.Vref2048(self.channel)

	def Vref4096(self):
		self.vref = 4.096
		self.step = 0.001
		self.voltage = self.code * self.step
		self.DAC.Vref4096(self.channel)

	def VrefVdd(self, vdd):
		self.vref = vdd
		self.step = vdd/4096
		self.voltage = self.code * self.step
		self.DAC.VrefVdd(self.channel)

class MCP4728:
	CMD_FAST_WRITE = 0x00
	CMD_MULTI_WRITE = 0x40
	CMD_SINGLE_WRITE = 0x58
	CMD_SEQ_WRITE = 0x50
	CMD_SELECT_VREF = 0x80
	CMD_SELECT_GAIN = 0xC0
	CMD_SELECT_PWRDOWN = 0xA0

	def __init__(self, bus, address):
		self.address = address
		self.i2c = SMBus(bus)
		self.channel = {'A' : Channel(0, self),
		                'B' : Channel(0, self),
		                'C' : Channel(0, self),
		                'D' : Channel(0, self)}

	def fastwrite(self):
		data = []
		for ch in self.channel.values():
			code = ch.code.to_bytes(2, 'big')
			data.append(self.CMD_FAST_WRITE | code[0])
			data.append(code[1])
		msg = i2c_msg.write(self.address, data)
		self.i2c.i2c_rdwr(msg)