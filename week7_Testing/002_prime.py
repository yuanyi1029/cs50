import math

def is_prime(n):
    if n < 2:
        return False
    else:
        for i in range(2, math.sqrt(n)):
            if n % i == 0:
                return False
        return True


