import hashlib

def encode(data):
    return str(data).encode('utf-8')

def generate_md5(data_list):
    md5 = hashlib.md5()
    for data in data_list:
        md5.update(encode(data))

    return md5.digest()