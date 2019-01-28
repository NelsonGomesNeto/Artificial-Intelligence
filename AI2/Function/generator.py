from random import randint
import sys

size = int(sys.argv[1])
print(size)
c = []
for i in range(size):
  c += [randint(-50, 50)]
print(*c, randint(-5000, 5000))