import math
import statistics
import sys
import random
"""
We have understood the requirement 300(b+1) integer memory limit refer to the bucket counters and constants of 
hash/sign functions, i.e. what is printed and recuperated. Thus not including integers like s, n, t, b
"""

def main():
    random.seed(132)
    s, n, t, b = 0, 0, 0, 0
    lines = sys.stdin
    for line in lines:
        l = line.rstrip().split(" ")
        if s == 0:
            s = int(l[0])
        elif n == 0:
            n = int(l[0])
            t = int(l[1])
            b = int(l[2])

    # sort for reinit??????
    lines = sys.stdin

    # decide what this should be, num of buckets
    bucks = 7*b
    # number of hash fucs. delta and c to be decided
    d = math.floor(300*(b+1)/(6+bucks))
    bucket_counters = [[0 for _ in range(bucks)] for _ in range(d)] # d x bucks
    # now choosing the first abitrarly
    p = find_prim(n)

    if p is None:
        return None

    hash_list, sign_list = generate_ind_hash(p, d)

    if hash_list is None:
        return None

    counter = 0
    if s == 1:
        for line in lines:
            if counter == n:
                break
            else:
                l = line.rstrip().split(" ")
                id = int(l[0])
                score = int(l[1])
                for i in range(d):
                    hash_f = func_hash(hash_list[i], id, p, bucks)
                    sign_f = sign_hash(hash_list[i], id, p)
                    # minus because I want to take yi - xi and this is xi
                    bucket_counters[i][hash_f] -= sign_f*score
            counter += 1
        print(d*(6+bucks))
        for i in range(d):
            for j in range(bucks):
                print(bucket_counters[i][j], end=" ")

        for i in range(d):
            print(hash_list[i].for_print(), end=" ")
            if i == d:
                print(sign_list[i].for_print())
            else:
                print(sign_list[i].for_print(), end=" ")
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
        return hash(h_a, h_b, s_a, s_b, s_c, s_d, d)

def func_hash(hash_vals, value, p, bucks):
    s = 0
    for i, const in enumerate(hash_vals):
        s += const*value**i
    return (s % p) % bucks

def sign_hash(hash_vals, value, p):
    s = 0
    for i, const in enumerate(hash_vals):
        s += const * value ** i
    return (((s % p) % 2) - 0.5) * 2

def hash(h_a, h_b, s_a, s_b, s_c, s_d, nr_hash):
    hash_list = []
    sign_list = []
    for i in range(nr_hash):
        a = h_a[i]
        b = h_b[i]
        hash_list.append(Hashes.all_var(Hashes, [a, b]))
        a = s_a[i]
        b = s_b[i]
        c = s_c[i]
        d = s_d[i]
        sign_list.append(Hashes.all_var(Hashes, [a, b, c, d]))
    return hash_list, sign_list

class Hashes:
    """Class to store hashing constants, will contain 2 integers if hash function and 4 integers if sign function"""
    def __init__(self):
        self.vars = []

    def add_var(self, val):
        self.vars.append(val)

    def all_var(self, array):
        self.vars = array

    def for_print(self):
        stringed = " ".join(self.vars)
        return stringed

if __name__ == "__main__":
    print(find_prim(20))