import typing


def hex2int(source: str) -> int:
    if source == '0x':
        return 0
    sign_bit_mask = 1 << (len(source) * 4 - 1)
    other_bit_mask = sign_bit_mask - 1
    value = int(source, 16)
    return - (value & sign_bit_mask) | (value & other_bit_mask)
