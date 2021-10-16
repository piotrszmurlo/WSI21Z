import numpy as np
import matplotlib.pyplot as plt

def steepest_descent(x0, alfa, precision, f, gf):
    xs = []
    vals = []
    derivative = gf(x0)
    val = f(x0)
    while True:
        xs.append(x0)
        vals.append(val)
        x1 = x0 - alfa*derivative
        derivative = gf(x1)
        val1 = f(x1)
        if abs(val - val1) < precision:
            break
        if val1 < val:
            val=val1
            x0=x1
        else:
            alfa *= 0.8
    return (x0, xs, vals)

def main():
    f = lambda x: x**4 - 5 * x**2 - 3*x
    gf = lambda x: 4*x**3 - 10*x + 3
    result = steepest_descent(-5,0.01, 0.001, f, gf)
    print(result[0])
    x = np.arange(-3, 3, 0.1)
    y = f(x)
    plt.plot(x,y)
    plt.scatter(result[1], result[2])
    plt.show()

if __name__ == '__main__':
    main()