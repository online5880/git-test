# .*args 는 가변인자이다. 길이 제한이 없는 파라미터이다.


def myFunction(*args):
    print(args)
    result = 1
    for arg in args:
        result *= arg

    return result


print(myFunction(2, 4, 6, 8, 10))
print(myFunction(3, 5, 7))
