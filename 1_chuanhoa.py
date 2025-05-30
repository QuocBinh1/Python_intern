s = str((input()))
s = s.split()
for i in range(len(s)):
    s[i] = s[i].capitalize()
s = ' '.join(s)
print(s)