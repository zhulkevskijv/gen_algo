import math


def flip_num(num):
    return 0 if num != 0 else 1


def float_bin(number, places=3):
    whole, dec = str(number).split(".")
    whole = int(whole)
    dec = int(dec)
    res = bin(whole).lstrip("0b") + "."

    for x in range(places):
        whole, dec = str((decimal_converter(dec)) * 2).split(".")
        dec = int(dec)
        res += whole

    return res


def decimal_converter(num):
    while num > 1:
        num /= 10
    return num


def gray_to_binary(gray):
    binary_code = [gray[0]]

    for i in range(1, len(gray)):
        if gray[i] == 0:
            binary_code += str(binary_code[i - 1])
        else:
            binary_code += str(flip_num(binary_code[i - 1]))

    return binary_code


def binary_to_gray(bin_arr):
    n = ''.join([str(x) for x in bin_arr])
    n = int(n, 2)
    n ^= (n >> 1)

    return bin(n)[2:]


def encode(x, a, b, m, is_binary):
    n = int((x - a) * (2 ** m - 1) / (b - a))
    if is_binary:
        code = bin(n)[2:]
        while len(code) < m:
            code = '0' + code
        return split_str_code(code)
    else:
        n ^= (n >> 1)
        code = bin(n)[2:]
        while len(code) < m:
            code = '0' + code
        return split_str_code(code)




def to_decimal(code_arr, is_binary):
    # print('Code arr - ', code_arr)
    arr = code_arr if is_binary else gray_to_binary(code_arr)
    # print(bin_arr)
    str_bin_code = ''.join([str(x) for x in arr])
    # print(str_bin_code)
    # print(int(str_bin_code, 2))
    return int(str_bin_code, 2)


def split_str_code(s):
    return [int(ch) for ch in s]


def decode(code, a, b, m, is_binary):
    # print(code,' ',a,' ',b,' ',m)
    return round(a + to_decimal(code, is_binary) * ((b - a) / (math.pow(2, m) - 1)), 2)

