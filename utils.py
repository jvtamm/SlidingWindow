import hashlib, random

def encode(data):
    return str(data).encode('utf-8')

def generate_md5(data_list):
    md5 = hashlib.md5()
    for data in data_list:
        md5.update(encode(data))

    return md5.digest()

def check_md5(data, md5):
    generated_md5 = generate_md5([data])
    return md5 == generated_md5

def compare_error(p_error):
    random_number = random.random()
    return random_number > p_error