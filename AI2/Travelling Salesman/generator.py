from random import randint
import sys

size = int(sys.argv[1])
print(size, size * (size - 1) // 2)
for i in range(1, size + 1):
  for j in range(i + 1, size + 1):
    print(i, j, randint(0, 100))
