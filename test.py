from parametric_crc import *

xorout = 0x0
crc8_rohc = specialized_crc(4, 0x07, 0,True , True, 0, tableless=True)
print(bin(crc8_rohc([6,5,4,3,2,1])))
