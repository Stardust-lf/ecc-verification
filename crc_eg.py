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
expected = 0xBC
data = bytes([0,1,2,3,4,5])
assert expected == calculator.checksum(data)
print(calculator.verify(data, expected))
