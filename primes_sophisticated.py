from math import sqrt
import multiprocessing as mp
import time

def prime_finder(i):
    i_is_prime = True
    for j in range(2, int(sqrt(i))+1):
        if i%j == 0:
            i_is_prime = False
            break
    if i_is_prime:
        print(i)


if __name__=='__main__':
    num = int(input("Enter a positive integer: "))
    print("Primes below {} are:".format(num))
    p = mp.Pool(4)
    interval = list(range(0,num))
    stime = time.perf_counter()
    p.map(prime_finder, interval)
    etime = time.perf_counter()
    print(etime-stime)
    input("press 'Return' key to exit")