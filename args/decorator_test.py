def hello_decorator(func):
    def inner1(*args, **kw):
        print("before execution", args, kw)
        returned_value = func(*args, **kw)
        print("after Execution", returned_value)

        return returned_value

    return inner1


@hello_decorator
def sum_two_numbers(a, b):
    print("inside the function")
    # print(a + b, c, d, e, f, g, h, i)
    return a + b


print("sum = ", sum_two_numbers(1, 3))
