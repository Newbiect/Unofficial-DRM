import base64

def decode_base64(s):
    n = len(s)
    if n % 4 != 0:
        return None
    padding = 0
    if n >= 1 and s[n - 1] == '=':
        padding = 1
        if n >= 2 and s[n - 2] == '=':
            padding = 2
            if n >= 3 and s[n - 3] == '=':
                padding = 3
    out_len = (n // 4) * 3 - padding
    buffer = bytearray(out_len)
    out = buffer
    if out is None or len(buffer) < out_len:
        return None
    j = 0
    accum = 0
    for i in range(n):
        c = s[i]
        if 'A' <= c <= 'Z':
            value = ord(c) - ord('A')
        elif 'a' <= c <= 'z':
            value = 26 + ord(c) - ord('a')
        elif '0' <= c <= '9':
            value = 52 + ord(c) - ord('0')
        elif c == '+' or c == '-':
            value = 62
        elif c == '/' or c == '_':
            value = 63
        elif c != '=':
            return None
        else:
            if i < n - padding:
                return None
            value = 0
        accum = (accum << 6) | value
        if (i + 1) % 4 == 0:
            if j < out_len:
                out[j] = (accum >> 16)
            if j < out_len:
                out[j + 1] = (accum >> 8) & 0xff
            if j < out_len:
                out[j + 2] = accum & 0xff
            j += 3
            accum = 0
    return buffer

def encode_base64(data):
    out = bytearray()
    size = len(data)
    i = 0
    while i < (size // 3) * 3:
        x1 = data[i]
        x2 = data[i + 1]
        x3 = data[i + 2]
        out.append(encode_6bit(x1 >> 2))
        out.append(encode_6bit((x1 << 4 | x2 >> 4) & 0x3f))
        out.append(encode_6bit((x2 << 2 | x3 >> 6) & 0x3f))
        out.append(encode_6bit(x3 & 0x3f))
        i += 3
    remainder = size % 3
    if remainder == 2:
        x1 = data[i]
        x2 = data[i + 1]
        out.append(encode_6bit(x1 >> 2))
        out.append(encode_6bit((x1 << 4 | x2 >> 4) & 0x3f))
        out.append(encode_6bit((x2 << 2) & 0x3f))
        out.append(ord('='))
    elif remainder == 1:
        x1 = data[i]
        out.append(encode_6bit(x1 >> 2))
        out.append(encode_6bit((x1 << 4) & 0x3f))
        out.append(ord('='))
        out.append(ord('='))
    return out

def encode_6bit(x):
    if x <= 25:
        return ord('A') + x
    elif x <= 51:
        return ord('a') + x - 26
    elif x <= 61:
        return ord('0') + x - 52
    elif x == 62:
        return ord('+')
    else:
        return ord('/')

def encode_base64_url(data):
    encoded = encode_base64(data)
    encoded_str = encoded.decode('utf-8')
    if '+' in encoded_str or '/' in encoded_str:
        encoded_str = encoded_str.replace('+', '-')
        encoded_str = encoded_str.replace('/', '_')
    return encoded_str