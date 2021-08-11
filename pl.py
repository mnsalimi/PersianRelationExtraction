import matplotlib.pyplot as plt
x = [1, 2, 3]
y = [10, 50, 54]
y2 = [2, 4, 5]
plt.plot(x, y)
plt.plot(x, y2)
plt.xlabel('x - training per batch')
plt.ylabel('y - loss/accracy')
plt.title('LOSS')
plt.legend(['y = loss', 'y = accuracy'], loc='upper left')
plt.savefig('foo.png')