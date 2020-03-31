import sys

reso = sys.argv[1:][0]
w, h = reso.split()[0].split('x')
print(w, h)