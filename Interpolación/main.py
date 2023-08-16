from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.utils as plotly_utils
import plotly as plotly

import json

app = Flask(__name__)

# Función para calcular la tabla de diferencias divididas
def get_diff_table(X, Y):
    n = len(X)
    A = np.zeros([n, n])

    for i in range(0, n):
        A[i][0] = Y[i]

    for j in range(1, n):
        for i in range(j, n):
            A[i][j] = (A[i][j-1] - A[i-1][j-1]) / (X[i] - X[i - j])

    return A

# Función para realizar la interpolación de Newton
def newton_interpolation(X, Y, x):
    sum = Y[0]
    temp = np.zeros((len(X), len(X)))
    temp_sum = 1.0

    for i in range(0, len(X)):
        temp[i, 0] = Y[i]

    for i in range(1, len(X)):
        temp_sum = temp_sum * (x - X[i - 1])

        for j in range(i, len(X)):
            temp[j, i] = (temp[j, i - 1] - temp[j - 1, i - 1]) / (X[j] - X[j - i])

        sum += temp_sum * temp[i, i]

    return sum

@app.route('/')
def index():
    return render_template('index.html')  # Renderiza una plantilla HTML en la página de inicio

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()  # Obtiene los datos JSON enviados desde el cliente

    X = data['X']  # Valores de X
    Y = data['Y']  # Valores de Y
    x_values = data['x_values']  # Valores de x para los que se realizará la interpolación

    dense_x_values = np.linspace(min(X), max(X), 1000)  # Genera 1000 puntos entre los valores mínimos y máximos de X

    ys = []

    # Calcula los valores interpolados utilizando la función de interpolación de Newton
    for x in dense_x_values:
        ys.append(newton_interpolation(X, Y, x))

    # Crea trazas para los datos originales y los valores interpolados
    trace_original = go.Scatter(x=X, y=Y, mode='markers', name='Original Values')
    trace_interpolation = go.Scatter(x=dense_x_values, y=ys, mode='lines', name='Interpolation')

    # Configura el diseño del gráfico
    layout = go.Layout(title='Interpolación',
                       xaxis=dict(title='x'),
                       yaxis=dict(title='y'))

    graph_data = [trace_original, trace_interpolation]
    graph_json = json.dumps(graph_data, cls=plotly_utils.PlotlyJSONEncoder)  # Convierte los datos del gráfico a JSON

    return jsonify({'graph_json': graph_json, 'y_values': ys})  # Devuelve los datos JSON con el gráfico y los valores interpolados

if __name__ == '__main__':
    app.run(debug=True)  # Inicia la aplicación Flask en modo de depuración
