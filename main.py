import math
import statistics
import sys
import random

def main():
    random.seed(132)
    s, n, t, b = 0, 0, 0, 0
    lines = list(sys.stdin)
    for line in lines[:2]:
        lines.remove(line)
        l = line.rstrip().split(" ")
        if s == 0:
            s = int(l[0])
        elif n == 0:
            n = int(l[0])
            t = int(l[1])
            b = int(l[2])

    lines = lines[2:]
    if 2*n <= 300*(b+1):
        save_all(s, n, t, b, lines)
    else:
        count_sketch(s, n, t, b, lines)

    # number of hash fucs. delta and c to be decided
    d = c*math.log2(1/delta)
    # decid what this should be, num of buckets
    bucks = 3/epsilon**2
    bucket_counters = [[0 for _ in range(bucks)] for _ in range(d)] # t x bucks
    # now choosing the first abitrarly
    p = find_prims(n)[0]
    hash_list, sign_list = generate_ind_hash(p, d, bucks)

    if hash_list is None:
        return None

    counter = 0
    if s == 1:
        for line in lines:
            l = line.rstrip().split(" ")
            if counter == n:
                break
            else:
                id = int(l[0])
                score = int(l[1])
                for i in range(d):
                    hash_f = hash_list[i]
                    sign_f = sign_list[i]
                    #minus because I want to take yi - xi and this is xi
                    bucket_counters[i][hash_f(id)] -= sign_f[id]*score
            counter += 1
        #Not really return, need to print what needs printing
        return bucket_counters, hash_list, sign_list
    else:
        l = lines.pop(0).rstrip().split(" ")
        m = int(l[0])
        l = lines.pop(0).rstrip().split(" ")
        # extract the m elements from l and save

        for line in lines[:n]:
            l = line.rstrip().split(" ")
            id = int(l[0])
            score = int(l[1])
            for i in range(d):
                hash_f = hash_list[i]
                sign_f = sign_list[i]
                # plus because I want to take yi - xi and this is yi
                bucket_counters[i][hash_f(id)] += sign_f[id] * score

        rem_lines = lines[n:]
        # sequential queries now
        k = rem_lines.pop(0).rstrip().split(" ")
        for q_i in range(k):
            #do I already have the first one?
            approx = []
            if q_i == 0:
                id = rem_lines[0]
                for i in range(d):
                    hash_f = hash_list[i]
                    sign_f = sign_list[i]
                    # plus because I want to take yi - xi and this is yi
                    approx.append(sign_f[id] * bucket_counters[i][hash_f(id)])
                    #alt. sort and take middle elem
                    med = statistics.median(approx)
                    if med >= t:
                        print("Yes")
                    else:
                        print("No")
            sys.stdout.flush()

def save_all(s, n, t, b, lines):
    if s == 1:
        mem = [0 for _ in range(n)]
        for line in lines:
            l = line.rstrip().split(" ")

def bucks_and_R(n, b):
    if b >= 1:
        bucks = 10*b
        # want 15ln(n)<=R<=30 + 179/(10b+4)
        if 15*math.log(n) > 30 + 179/(bucks+4):
            #what should I do?
            pass
        else:
            R = 30 + math.floor(179/(bucks+4))
    else:
        bucks = 1
        # want 15ln(n)<=R<=30 + 179/5 = 65
        if 15*math.log(n) > 65:
            #what should I do?
            pass
        else:
            R = 65
def find_prims(n):
    b = 2*n
    res = []
    if n == 1:
        res.append(n)
        n += 1
        if (b >= 2):
            res.append(n)
            n += 1
    if n == 2:
        res.append(n)
    if n % 2 == 0:
        n += 1
    for i in range(n, b + 1, 2):
        flag = 1
        j = 2
        while j * j <= i:
            if i % j == 0:
                flag = 0
                break
            j += 1
        if flag == 1:
            res.append(i)
    return res

def generate_ind_hash(p, d, bucks):
    h_a = []
    h_b = []
    s_a = []
    s_b = []
    s_c = []
    s_d = []
    for i in range(d):
        #p-1??
        h_a.append(random.randint(1, p))
        h_b.append((random.randint(0, p)))
        s_a.append(random.randint(1, p))
        s_b.append((random.randint(0, p)))
        s_c.append((random.randint(0, p)))
        s_d.append((random.randint(0, p)))
    #check none are equal
    if (len(h_a) != len(set(h_a)) and len(h_b) != len(set(h_b))) or (len(s_a) != len(set(s_a)) and len(s_b) != len(set(s_b))
                                                        and len(s_c) != len(set(s_c)) and len(s_d) != len(set(s_d))):
        return None, None
    else:
        return hash(h_a, h_b, s_a, s_b, s_c, s_d, p, d, bucks)

def hash(h_a, h_b, s_a, s_b, s_c, s_d, p, d, bucks):
    hash_list = []
    sign_list = []
    for i in range(d):
        a = h_a[i]
        b = h_b[i]
        def curried_hash(value):
            return ((a*value + b) % p) % bucks
        hash_list.append(curried_hash)
        a = s_a[i]
        b = s_b[i]
        c = s_c[i]
        d = s_d[i]
        def curried_sign_hash(value):
            return ((((a*value**3 + b*value**2 + c*value + d) % p) % 2) - 0.5)*2
        sign_list.append(curried_sign_hash)
    return hash_list, sign_list

if __name__ == "__main__":
    print(find_prims(100000))