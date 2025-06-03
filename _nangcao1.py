import math
a = int(input("Nhập số nguyên dương a: "))
b = int(input("Nhập số nguyên dương b: "))

for i in range(a, b + 1):
    if i % 3 == 0 and math.isqrt(i)**2 != i:
        print(i)
    