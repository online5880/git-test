def my_function(**kwargs):
    print(
        kwargs.get("first"),
        kwargs.get("mid"),
        kwargs.get("last"),
    )


my_function(first=123, mid="mid", last=999)
