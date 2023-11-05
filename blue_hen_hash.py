BLOCK_SIZE = 8
HALF_BLOCK_SIZE = BLOCK_SIZE // 2
HALF_BLOCK_BIT_SIZE = HALF_BLOCK_SIZE * 8
CIPHER_ROUNDS = 4


def pad_message(message: bytes) -> bytes:
    if len(message) % BLOCK_SIZE == 0:
        return message

    message += 0x80.to_bytes(1, "little", signed=False)
    if len(message) % BLOCK_SIZE == 0:
        return message

    total_zero_bytes = (BLOCK_SIZE - (len(message) % BLOCK_SIZE))
    message += b'\0' * total_zero_bytes
    assert len(message) % BLOCK_SIZE == 0
    return message


def blue_hen_prf(block: bytes, right: bytes) -> bytes:
    assert len(block) == BLOCK_SIZE
    assert len(right) == HALF_BLOCK_SIZE
    block_low = int.from_bytes(block[HALF_BLOCK_SIZE:], byteorder='little', signed=False)
    block_high = int.from_bytes(block[:HALF_BLOCK_SIZE], byteorder='little', signed=False)
    right = int.from_bytes(right, byteorder='little', signed=False)

    mask = 0xFFFFFFFF
    out = (right + block_low) & mask
    out = (((out << 8) & mask) | ((out >> (HALF_BLOCK_BIT_SIZE - 8)) & mask)) & mask
    out = (out + block_high) & mask
    out = (((out >> 3) & mask) | ((out << (HALF_BLOCK_BIT_SIZE - 3)) & mask)) & mask
    return out.to_bytes(HALF_BLOCK_SIZE, byteorder='little', signed=False)


def blue_hen_compression_function(h: bytes, block: bytes) -> bytes:
    assert len(h) == BLOCK_SIZE
    assert len(block) == BLOCK_SIZE
    left = h[:HALF_BLOCK_SIZE]
    right = h[HALF_BLOCK_SIZE:]
    for i in range(CIPHER_ROUNDS):
        next_left = right
        next_right = blue_hen_prf(block, right)
        next_right = bytes(x ^ y for x, y in zip(left, next_right))
        left, right = next_left, next_right

    output = left + right
    assert len(output) == BLOCK_SIZE
    return output


def blue_hen_hash(message: bytes) -> bytes:
    iv = b'BLUE_HEN'
    h = iv
    padded_message = pad_message(message)
    for i in range(0, len(padded_message), BLOCK_SIZE):
        block = padded_message[i:i+BLOCK_SIZE]
        compressed_block = blue_hen_compression_function(h, block)
        h = bytes(x ^ y for x, y in zip(h, compressed_block))
    assert len(h) == BLOCK_SIZE
    return h

lol = input("enter thang: ")
for i in range(2**16):
    hexthang = blue_hen_hash(lol.encode('ascii') + i.to_bytes(2,'little', signed=False)).hex()
    if(hexthang[0] == '0' and hexthang[1] == '0'):
        print(i, hexthang)
#print(blue_hen_hash(b'hello\x8b6').hex())
