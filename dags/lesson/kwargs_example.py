def f(x, **kwargs):
    print(f"x={x}, type={type(x)}")
    for key, value in kwargs.items():
        print(f"key={key}, value={value}")


f(x2=10, x=444, y=10)
