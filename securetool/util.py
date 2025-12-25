
def retime(est_time):

    if est_time == "infinity" or est_time > 315360000000:
        sen = ("ETERNITY !!")
        score = 10
        return [sen, score]
    elif est_time < 0.24:
        sen = ("Instant!")
        score = 0
        return [sen, score]
    elif est_time < 0:
        sen = ("Less then a second")
        score = 1
        return [sen, score]
    elif est_time < 72000:
        sen = ("about a Day")
        score = 2
        return [sen, score]
    elif est_time < 504000:
        sen = ("about a Week")
        score = 3
        return [sen, score]
    elif est_time < 2628000:
        sen = ("about a Month")
        score = 4
        return [sen, score]
    elif est_time < 31536000:
        sen = ("about a Year")
        score = 5
        return [sen, score]
    elif est_time < 315360000:
        sen = ("Decade ")
        score = 6
        return [sen, score]
    elif est_time < 3153600000:
        sen = ("DECADES ")
        score = 7
        return [sen, score]
    elif est_time < 31536000000:
        sen = ("HUNDREDS of YEARS ")
        score = 8
        return [sen, score]
    elif est_time < 315360000000:
        sen = ("THOUSANDS of YEARS ")
        score = 9
        return [sen, score]
    else:
        sen = ("Effectively uncrackable")
        score = 10
        return [sen, score]
    
        
def strength_check(password):
    from password_strength import strength

    stren = strength(password)
    entropy = stren[0]
    est_time = stren[1]
    time_score = retime(est_time)

    print(f"\n  Crack Time:                 {time_score[0]}" )
    print(f"  Password Entropy:           {entropy}")
    print(f"  Password Strength SCORE:    {time_score[1]}\n")

    return 0

def hasher(password, algo):
    import hashlib
    
    password = password.encode("utf-8")
    hashed = 0
    if algo.lower() == "sha256":
        hashed = hashlib.sha256(password).hexdigest()
    elif algo.lower() == "sha224":
        hashed = hashlib.sha224(password).hexdigest()
    elif algo.lower() == "sha384":
        hashed = hashlib.sha384(password).hexdigest()
    elif algo.lower() == "sha512":
        hashed = hashlib.sha512(password).hexdigest()
    else:
        print("Algorithm unrecognizable")
        return

    print(f"\n  Hash:   {hashed}\n")
    return hashed


def verify(phash, password, algo):
    import hashlib
    password = password.encode("utf-8")
    hashed = 0
    if algo.lower() == "sha256":
        hashed = hashlib.sha256(password).hexdigest()
    elif algo.lower() == "sha224":
        hashed = hashlib.sha224(password).hexdigest()
    elif algo.lower() == "sha384":
        hashed = hashlib.sha384(password).hexdigest()
    elif algo.lower() == "sha512":
        hashed = hashlib.sha512(password).hexdigest()
    else:
        print("Algorithm unrecognizable")
        return

    return phash == hashed


def audit(pfile, minscore):
    from password_strength import strength

    di = {}

    with open(pfile, 'r') as f:
        for line in f.readlines():
            line = line.replace("\n", "")
            score = retime(strength(line)[1])[1]
            
            di[line] = ("weak" if score <= int(minscore) else "strong", score)
    
    
    return di

def struct_print(di):

    print("Auditing file: passwords.txt", 
          end='\n|---------------------------|\n')
    print(f"Total passwords checked:  {len(di)}")
    print(f"Weak passwords:           {len([i[0] for i in list(di.values()) if i[0] == "weak"])}")
    print(f"Strong pass words:         {len([i[0] for i in list(di.values()) if i[0] == "strong"])}", end="\n\n")
    
    print("Weak passwords:", end="")
    print("       {Scoring scale: 0-10}",end="\n\n")
    for k, v in di.items():
        if v[0] == "weak":
            print(f"-{k} ",end="")
            for n in range(20 - (len(k) if len(k) < 20 else 0)):
                print(end=" ")
            print(f"(Strength Score:  {v[1]})")
            