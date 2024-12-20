
def reverse_bits(value: int, width: int):
    assert 0 <= value < (1 << width)
    return int('{v:0{w}b}'.format(v=value, w=width)[::-1], 2)


reversed_int8_bits = tuple(reverse_bits(i, 8) for i in range(256))

def parametric_crc(data: bytes, ref_init: int, *, width: int, ref_poly: int,
                   refin: bool, refout: bool, xorout: int, bit_len: int = None,
                   interim: bool = False, residue: bool = False, table: [int] = None):
    bit_len = len(data) * 8 if bit_len is None else bit_len
    assert width > 0 and 0 <= xorout < (1 << width) and bit_len <= len(data) * 8
    crc = ref_init
    print(f"Initial CRC: {crc:0{width}b}")  # 打印初始值
    
    if table:  # 使用查表法
        num_bytes, bit_len = bit_len >> 3, bit_len & 7
        for i in range(num_bytes):
            b = data[i] if refin else reversed_int8_bits[data[i]]
            print(f"Processing byte: {b:08b} (refin={refin})")
            crc = table[(crc & 0xff) ^ b] ^ (crc >> 8)
            print(f"Updated CRC (after table lookup): {crc:0{width}b}")
        data = data[num_bytes:num_bytes + 1] if bit_len else b''
    
    for b in data:  # 手动计算，逐位处理
        b = b if refin else reversed_int8_bits[b]
        if bit_len < 8:
            if bit_len <= 0:
                break
            b &= (1 << bit_len) - 1  # 去掉无用的高位
        print(f"Processing byte/remaining bits: {b:08b} (bit_len={bit_len})")
        crc ^= b
        print(f"CRC after XOR with byte: {crc:0{width}b}")
        for _ in range(min(bit_len, 8)):

            print(f"Current CRC: {crc:0{width}b}, Poly: {ref_poly:0{width}b}")  # 添加打印语句，检查当前值
            if crc & 1:
                crc = (crc >> 1) ^ ref_poly
                print(f"Bit shifted, CRC XOR with poly: {crc:0{width}b}")
            else:
                crc = crc >> 1
                print(f"Bit shifted, no XOR: {crc:0{width}b}")
        bit_len -= 8

    if interim:
        return crc
    crc = crc if refout else reverse_bits(crc, width)
    return crc if residue else crc ^ xorout


def specialized_crc(width: int, poly: int, init: int, refin: bool,
                    refout: bool, xorout: int, tableless: bool = False):
    ref_init = reverse_bits(init, width)  # 兼容 CRC 手册的位翻转
    ref_poly = reverse_bits(poly, width)  # 兼容 CRC 手册的位翻转
    p = dict(width=width, ref_poly=ref_poly, xorout=xorout, refin=refin, refout=refout)
    t = None if tableless else [parametric_crc(b'\0', i, interim=True, **p)
                                for i in range(256)]
    
    def crc_fn(data: bytes, ref_init: int = ref_init, *, interim: bool = False,
               residue: bool = False, bit_len: int = None):
        print(f"CRC parameters: width={width}, poly={poly}, init={init}, refin={refin}, refout={refout}, xorout={xorout}")
        print(f"Tableless mode: {tableless}")
        return parametric_crc(data, ref_init, interim=interim, residue=residue,
                              bit_len=bit_len, table=t, **p)
    
    return crc_fn
