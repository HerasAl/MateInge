from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

def f(x, y):
    return y - x

def euler_mejorado(f, x0, y0, h, n):
    x_values = [x0]
    y_values = [y0]

    for _ in range(n):
        x = x_values[-1]
        y = y_values[-1]
        
        k1 = h * f(x, y)
        k2 = h * f(x + h, y + k1)
        
        x_new = x + h
        y_new = y + 0.5 * (k1 + k2)
        
        x_values.append(x_new)
        y_values.append(y_new)

    return x_values, y_values

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x0 = float(request.form['x0'])
        y0 = float(request.form['y0'])
        h = float(request.form['h'])
        n = int(request.form['n'])
        
        x_values, y_values = euler_mejorado(f, x0, y0, h, n)

        plt.plot(x_values, y_values, label='Euler Mejorado')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.legend()
        plt.grid()
        plt.title('Solución de Ecuación Diferencial')

        img_path = 'static/plot.png'
        plt.savefig(img_path)
        plt.clf()

        return render_template('index.html', img_path=img_path)

    return render_template('index.html', img_path=None)

if __name__ == '__main__':
    app.run(debug=True)
