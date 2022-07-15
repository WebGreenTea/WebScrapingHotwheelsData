import pyperclip
s = ''
for i in range(1,9122+1):
    s+= str(i)
    s+=','

pyperclip.copy(s)