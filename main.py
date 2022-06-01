import math
import statistics
import sys
import random
"""
We have understood the requirement 300(b+1) integer memory limit refer to the bucket counters and constants of 
hash/sign functions, i.e. what is printed and recuperated. Thus not including integers like s, n, t, b
"""

def main():
    random.seed(300)
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
    bucks = 7*b
    # number of hash fucs. delta and c to be decided
    d = math.floor(300*(b+1)/(6+bucks))
    # now choosing the first abitrarly
    p = find_prim(10**8)

    if p is None:
        #print("bajs")
        pass

    counter = 0
    if s == 1:
        bucket_counters = [[0 for _ in range(bucks)] for _ in range(d)]  # d x bucks
        hash_list, sign_list = generate_ind_hash(p, d)

        if hash_list is None:
            #print("bajs")
            pass

        for line in sys.stdin:
            l = line.rstrip().split(" ")
            id = int(l[0])
            score = int(l[1])
            for i in range(d):
                hash_f = func_hash(hash_list[i], id, p, bucks)
                sign_f = sign_hash(hash_list[i], id, p)
                # minus because I want to take yi - xi and this is xi
                bucket_counters[i][hash_f] -= sign_f*score
            counter += 1
            if counter == n:
                break

        # output
        print(d*(6+bucks))
        for i in range(d):
            for j in range(bucks):
                print(int(bucket_counters[i][j]), end=" ")

        for i in range(d):
            print(hash_list[i].for_print(), end=" ")
            if i == d:
                print(sign_list[i].for_print())
            else:
                print(sign_list[i].for_print(), end=" ")
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
                for i in range(d):
                    bucket_counters.append([])
                    for j in range(bucks):
                        bucket_counters[-1].append(int(bucket_vals[i*bucks + j]))
                hash_list, sign_list = hash_s2(hashing_vals, d)
            else:
                l = line.rstrip().split(" ")
                id = int(l[0])
                score = int(l[1])
                for i in range(d):
                    hash_f = func_hash(hash_list[i], id, p, bucks)
                    sign_f = sign_hash(hash_list[i], id, p)
                    # plus because I want to take yi - xi and this is yi
                    bucket_counters[i][hash_f] += sign_f * score
                counter += 1
                if counter == n:
                    break

        # sequential queries now
        k = None
        #counter = 0
        for line in sys.stdin:
            l = line.rstrip().split(" ")
            if k is None:
                k = int(l[0])
                continue
            approx = []
            id = int(l[0])
            for i in range(d):
                hash_f = func_hash(hash_list[i], id, p, bucks)
                sign_f = sign_hash(hash_list[i], id, p)
                # plus because I want to take yi - xi and this is yi
                approx.append(sign_f * bucket_counters[i][hash_f])
            #alt. sort and take middle elem
            med = statistics.median(approx)
            if med >= t/2:
                print("Yes")
            else:
                print("No")
            sys.stdout.flush()
            #counter += 1
            #if counter >= k:
                #break

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
        h_a.append(random.randint(1, p-1))
        h_b.append((random.randint(0, p-1)))
        s_a.append(random.randint(1, p-1))
        s_b.append((random.randint(0, p-1)))
        s_c.append((random.randint(0, p-1)))
        s_d.append((random.randint(0, p-1)))
    #check none are equal
    """if (len(h_a) != len(set(h_a)) and len(h_b) != len(set(h_b))) or (len(s_a) != len(set(s_a)) and len(s_b) != len(set(s_b))
                                                        and len(s_c) != len(set(s_c)) and len(s_d) != len(set(s_d))):
        return None, None"""
    return hash(h_a, h_b, s_a, s_b, s_c, s_d, d)

def func_hash(hash_vals, value, p, bucks):
    s = 0
    for i, const in enumerate(hash_vals.vars):
        s += const*value**i
    return (s % p) % bucks

def sign_hash(hash_vals, value, p):
    s = 0
    for i, const in enumerate(hash_vals.vars):
        s += const * value ** i
    return (((s % p) % 2) - 0.5) * 2

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
    return hash_list, sign_list

def hash_s2(hash_vals, nr_hash):
    hash_list = []
    sign_list = []
    for i in range(nr_hash):
        vals = hash_vals[i*6:(i+1)*6]
        hash_list.append(Hashes([int(val) for val in vals[:2]]))
        sign_list.append(Hashes([int(val) for val in vals[2:]]))
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