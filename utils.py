import hashlib, random

def encode(data):
    return str(data).encode('utf-8')

def generate_md5(data):
    md5 = hashlib.md5()
    md5.update(data)

    return md5.digest()

def check_md5(data, md5):
    generated_md5 = generate_md5(data)
    return md5 == generated_md5

def corrupt_md5(packet):
    packet = bytearray(packet)
    packet[-1] = (packet[-1] + 1) % 256
    packet = bytes(packet)

    return packet

def compare_error(p_error):
    random_number = random.random()
    return random_number < p_error