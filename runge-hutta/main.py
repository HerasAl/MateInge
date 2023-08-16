from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

def runge_kutta(f, x0, y0, h, n):
    x_values = [x0]
    y_values = [y0]

    for i in range(n):
        k1 = h * f(x_values[-1], y_values[-1])
        k2 = h * f(x_values[-1] + h/2, y_values[-1] + k1/2)
        k3 = h * f(x_values[-1] + h/2, y_values[-1] + k2/2)
        k4 = h * f(x_values[-1] + h, y_values[-1] + k3)

        x_values.append(x_values[-1] + h)
        y_values.append(y_values[-1] + (k1 + 2*k2 + 2*k3 + k4) / 6)

    return x_values, y_values

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        expression = request.form['expression']
        x0 = float(request.form['x0'])
        y0 = float(request.form['y0'])
        h = float(request.form['h'])
        n = int(request.form['n'])

        def f(x, y):
            return eval(expression)

        x_values, y_values = runge_kutta(f, x0, y0, h, n)

        plt.plot(x_values, y_values)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Runge-Kutta Solution')
        plt.grid(True)
        plt.savefig('static/plot.png')

        return render_template('index.html', plot_path='static/plot.png')
    
    return render_template('index.html', plot_path=None)

if __name__ == '__main__':
    app.run(debug=True)
