def test(**kwargs):
    for key in kwargs:
        print(f"{key} ==> {kwargs[key]}")

test(category="Мясные изделия", search="Фарш")

data = {"category":"Мясные изделия", "search":"Фарш"}
test(**data)
