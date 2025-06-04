def daonguoc(s):
    s = s.strip()
    s = s[::-1]
    result = ''.join(s)
    return result
s = str(input())
print(daonguoc(s))

