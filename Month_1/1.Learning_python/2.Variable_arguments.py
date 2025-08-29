# Sometimes you don’t know how many arguments a function will get.
# *args → collects extra positional arguments into a tuple.
# **kwargs → collects extra keyword arguments into a dictionary.


def f(a, *args, **kwargs):
    print("a:", a)
    print("args:", args)
    print("kwargs:", kwargs)


f(1, 2, 3, 4, x=10, y=20)
