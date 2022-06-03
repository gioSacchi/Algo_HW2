import math
import statistics
import sys
import random
import time
"""
We have understood the requirement 300(b+1) integer memory limit refer to the bucket counters and constants of 
hash/sign functions, i.e. what is printed and recuperated. Thus not including integers like s, n, t, b
"""

def main():
    random.seed(5)
    s, n, t, b = 0, None, 0, 0
    #lines = sys.stdin
    for line in sys.stdin:
        l = line.rstrip().split(" ")
        if s == 0:
            s = int(l[0])
        elif n is None:
            n = int(l[0])
            t = int(l[1])
            b = int(l[2])
            break
    # decide what this should be, num of buckets
    bucks = 5*(b+1)
    if n/bucks > 100:
        missing = n//100 - bucks
        bucks += int(1.02*missing)
    # number of hash fucs. delta and c to be decided
    d = math.floor(200*(b+1)/(6+bucks))
    # now choosing the first abitrarly
    #p = find_prim(10**8)
    p = 100000007

    counter = 0
    if s == 1:
        bucket_counters = [[0 for _ in range(bucks)] for _ in range(d)]  # d x bucks
        hash_list, sign_list = generate_ind_hash(p, d)

        for line in sys.stdin:
            l = line.rstrip().split(" ")
            id = int(l[0])
            score = int(l[1])
            for i in range(d):
                hash_f = func_hash(hash_list[i], id, p, bucks)
                sign_f = sign_hash(sign_list[i], id, p)
                # minus because I want to take yi - xi and this is xi
                bucket_counters[i][hash_f] -= sign_f*score
            counter += 1
            if counter == n:
                break

        # output
        print(d*(6+bucks))
        flat_string_buckets = " ".join([str(int(bucket_counters[i][j])) for i in range(d) for j in range(bucks)])
        print(flat_string_buckets, end=" ")
        hashes_string = " ".join([hash_list[i].for_print() + " " + sign_list[i].for_print() for i in range(d)])
        print(hashes_string)

    else:
        m = 0
        bucket_counters = []
        hash_list = []
        sign_list = []
        for line in sys.stdin:
            # input
            if m == 0:
                l = line.rstrip().split(" ")
                m = int(l[0])
            elif len(bucket_counters) == 0:
                l = line.rstrip().split(" ")
                bucket_vals = l[:bucks*d]
                hashing_vals = l[bucks*d:]
                bucket_counters = [[int(bucket_vals[i*bucks + j]) for j in range(bucks)] for i in range(d)]
                hash_list, sign_list = hash_s2(hashing_vals, d)
                break

        for line in sys.stdin:
            l = line.rstrip().split(" ")
            id = int(l[0])
            score = int(l[1])
            for i in range(d):
                hash_f = func_hash(hash_list[i], id, p, bucks)
                sign_f = sign_hash(sign_list[i], id, p)
                # plus because I want to take yi - xi and this is yi
                bucket_counters[i][hash_f] += sign_f * score
            counter += 1
            if counter == n:
                break

        # sequential queries now
        k = None
        counter = 0
        for line in sys.stdin:
            l = line.rstrip().split(" ")
            if k is None:
                k = int(l[0])
                continue
            id = int(l[0])
            approx = []
            for i in range(d):
                hash_f = func_hash(hash_list[i], id, p, bucks)
                sign_f = sign_hash(sign_list[i], id, p)
                approx.append(sign_f * bucket_counters[i][hash_f])

            #approx = [sign_hash(sign_list[i], id, p) * bucket_counters[i][func_hash(hash_list[i], id, p, bucks)] for i in range(d)]

            med = statistics.median(approx)
            if med >= t/2:
                print("Yes")
            else:
                print("No")
            sys.stdout.flush()
            counter += 1
            if counter >= k:
                break

def find_prim(n):
    """first prim between n and 2n"""
    b = 2*n
    if n == 1:
        return n
    if n == 2:
        return n
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
            return i
    return None

def generate_ind_hash(p, d):
    h_a = [random.randint(1, p-1) for _ in range(d)]
    h_b = [random.randint(0, p - 1) for _ in range(d)]
    s_a = [random.randint(1, p - 1) for _ in range(d)]
    s_b = [random.randint(0, p - 1) for _ in range(d)]
    s_c = [random.randint(0, p - 1) for _ in range(d)]
    s_d = [random.randint(0, p - 1) for _ in range(d)]
    return hash(h_a, h_b, s_a, s_b, s_c, s_d, d)

def func_hash(hash_vals, value, p, bucks):
    a, b = hash_vals.vars
    return ((a*value + b) % p) % bucks

def sign_hash(hash_vals, value, p):
    a, b, c, d = hash_vals.vars
    return ((((a*value**3 + b*value**2 + c*value + d) % p) % 2) - 0.5) * 2

def hash(h_a, h_b, s_a, s_b, s_c, s_d, nr_hash):
    hash_list = []
    sign_list = []
    for i in range(nr_hash):
        a = h_a[i]
        b = h_b[i]
        hash_list.append(Hashes([a, b]))
        a = s_a[i]
        b = s_b[i]
        c = s_c[i]
        d = s_d[i]
        sign_list.append(Hashes([a, b, c, d]))
    #hash_list = [Hashes([h_a[i], h_b[i]]) for i in range(nr_hash)]
    #sign_list = [Hashes([s_a[i], s_b[i], s_c[i], s_d[i]]) for i in range(nr_hash)]
    return hash_list, sign_list

def hash_s2(hash_vals, nr_hash):
    hash_list = []
    sign_list = []
    for i in range(nr_hash):
        vals = hash_vals[i*6:(i+1)*6]
        hash_list.append(Hashes([int(val) for val in vals[:2]]))
        sign_list.append(Hashes([int(val) for val in vals[2:]]))
    #hash_list_2 = [Hashes([int(val) for val in hash_vals[i*6:i*6 + 2]]) for i in range(nr_hash)]
    #sign_list = [Hashes([int(val) for val in hash_vals[i * 6 + 2:(i + 1) * 6]]) for i in range(nr_hash)]
    return hash_list, sign_list

class Hashes:
    """Class to store hashing constants, will contain 2 integers if hash function and 4 integers if sign function"""
    def __init__(self, array):
        self.vars = array

    def for_print(self):
        stringed = " ".join([str(elem) for elem in self.vars])
        return stringed

if __name__ == "__main__":
    main()