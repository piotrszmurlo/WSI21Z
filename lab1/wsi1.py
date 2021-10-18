import numpy as np
import matplotlib.pyplot as plt

def steepest_descent(x0, alfa, precision, f, gf):
    xs = []
    vals = []
    derivative = gf(x0)
    val = f(x0)
    steps = 0
    while True:
        xs.append(x0)
        vals.append(val)
        x1 = x0 - alfa*derivative
        derivative = gf(x1)
        val1 = f(x1)
        steps += 1
        if abs(val - val1) < precision:
            break
        if val1 < val:
            val=val1
            x0=x1
        else:
            alfa *= 0.5
    return (x0, xs, vals, steps)

def main():
    f = lambda x: x**4 - 5 * x**2 - 3*x
    gf = lambda x: 4*x**3 - 10*x + 3

    # f = lambda x: x**2 +3*x +8
    # gf = lambda x: 2*x+3

    alfa = 0.015
    x0 = 0.1
    result = steepest_descent(x0,alfa, 0.001, f, gf)

    # for i in np.arange(0.01, 0.05, 0.005):
    #     print('wynik: ' + str(steepest_descent(-3,i, 0.001, f, gf)[0]) + f'; alfa: {i}; kroki: {str(steepest_descent(-3,i, 0.001, f, gf)[3])}')
    print("result: " + str(result[0]))
    print("steps: "+ str(result[3]))
    x = np.arange(-3, 3, 0.1)
    y = f(x)
    plt.plot(x,y)
    # plt.title(f"y=x^4 - 5x^2 - 3x, alfa={alfa}, x0={x0}, kroki: {result[3]}")
    plt.title(f"y = x^2 + 3x + 8, alfa={alfa}, x0={x0}, kroki: {result[3]}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.scatter(result[1], result[2])
    plt.plot(result[1], result[2])
    plt.show()

if __name__ == '__main__':
    main()
