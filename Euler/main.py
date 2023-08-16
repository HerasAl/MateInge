from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

# Definir la ecuación diferencial: y' = -2x + yx
def equation(x, y):
    return -2*x + y*x

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        x_initial = float(request.form['x_initial'])
        y_initial = float(request.form['y_initial'])
        x_final = float(request.form['x_final'])
        step_size = float(request.form['step_size'])

        num_steps = int((x_final - x_initial) / step_size)
        x_values = np.linspace(x_initial, x_final, num_steps + 1)
        y_values = []
        y_values.append(y_initial)

        for i in range(num_steps):
            y_new = y_values[i] + equation(x_values[i], y_values[i]) * step_size
            y_values.append(y_new)

        plt.plot(x_values, y_values, 'r', label="Aproximación de Euler")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Aproximación de y\' = -2x + yx usando el Método de Euler')
        plt.legend()
        plt.grid(True)

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close()

        values = [{'x': x, 'y': y} for x, y in zip(x_values, y_values)]

        return render_template('index.html', plot_url=plot_url, values=values)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
