from crc import Calculator, Crc8
from crc import Configuration

config = Configuration(
    width = 8,
    polynomial=0x7,
    init_value= 0x00,
    final_xor_value=0x00,
    reverse_input=False,
    reverse_output=False
    )
calculator = Calculator(config, optimized=True)
# expected = 0xBC
data =bytes([6,5,4,3,2,1])
checksum = calculator.checksum(data)
print(bin(checksum))
# assert expected == calculator.checksum(data)
print(calculator.verify(data,checksum ))
