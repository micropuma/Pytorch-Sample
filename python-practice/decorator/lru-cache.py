import functools

@functools.lru_cache(maxsize=3)
def print_float(x: float) -> float:
    print(f"Printing float: {x}")
    return x

@functools.lru_cache(maxsize=1)
def env_setup():
    print("Each time start a environment, do following env initialization!!!")

if __name__ == "__main__":
    # test lru_cache for maxsize = 3
    print_float(1.1)   # print
    print_float(2.2)   # print
    print_float(3.3)   # print
    print_float(1.1)   # cached
    print_float(2.2)   # cached
    print_float(3.3)   # cached
    print_float(4.4)   # print
    print_float(1.1)   # evicted

    # more like singleton method, used for envrionment configuration
    env_setup()        # print
    env_setup()        # function cached

    # use function benethe lru_cache
    print_float(1.1)   # cached
    print_float.__wrapped__(1.1)   # call the function benethe, bypassing cache


