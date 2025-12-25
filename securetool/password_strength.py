
def strength(password):
    entropy = 0

    import json
    data = 0
    with open("securetool/top30.json", 'r') as f:
        data = json.load(f)

    if password in data:
        entropy = data.index(password)
    else:
        char_set = sum(find_charset_size(password))

        from math import log2
        entropy = round(log2(char_set ** len(password)), 2)

    est_time = 0
    try:
        est_time = ((((2 ** entropy) / (10**11)))) 
    except OverflowError:
        est_time = "infinity"
    

    return (entropy, est_time)


def find_charset_size(password):
    char_set = [0, 0, 0, 0] #[ lowercase, uppercase, numbers, symbols ]

    for i in password:
        if 0 not in char_set:
            break
        if i.isalpha():
            if i.isupper() and char_set[0] == 0:
                char_set[0] = 26
            if i.islower() and char_set[1] == 0:
                char_set[1] = 26
        if i.isnumeric() and char_set[2] == 0:
            char_set[2] = 10
        if not i.isalnum() and char_set[3] == 0:
            char_set[3] = 32
    

    return tuple(char_set)