import utils

def less_than(lhs, rhs):
    if len(lhs) < len(rhs):
        return True
    elif len(lhs) > len(rhs):
        return False
    return utils.memcmp(lhs, rhs) < 0

def byte_array_to_hex_string(in_buffer, length):
    hex_chars = "0123456789ABCDEF"
    out_buffer = ['\0'] * (length * 2)
    for i in range(length):
        byte = in_buffer[i]
        out_buffer[i * 2] = hex_chars[(byte >> 4) & 0xf]
        out_buffer[i * 2 + 1] = hex_chars[byte & 0xf]
    return ''.join(out_buffer)