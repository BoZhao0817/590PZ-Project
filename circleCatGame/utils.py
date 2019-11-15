from random import randint

def generate_random_locations(n, loc_dict):
    # within a board n*n
    # generate a random valid location
    while True:
        i = randint(0,n-1)
        j = randint(0,n-1)
        if (i, j) not in loc_dict:
            return (i, j)
