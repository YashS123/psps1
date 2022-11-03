from flask import Flask, render_template, request, flash, url_for
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
app = Flask(__name__)


@app.route('/')
def intro():
    return render_template('intro.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/ack')
def ack():
    return render_template('aboutus.html')


@app.route('/res')
def res():
    return render_template('research.html')


@app.route('/data')
def data():
    return render_template('data.html')


@app.route('/result', methods=['POST'])
def result():
    lis = []
    input_data = [x for x in request.form.values()]
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    print(input_data)
    print(input_data_as_numpy_array)
    print(input_data_reshaped)
    z = len(input_data)
    str = input_data[0]
    k = str.split(":")
    m = []
    for i in range(1, z):
        k.append(input_data[i])
    for z in k:
        m.append(float(z))
    po = m[1]
    op = m[0]
    turnsrat = po/op
    faultrelay = m[3] * turnsrat
    pickup = m[1]*m[2]/100
    psm = round(faultrelay/pickup, 2)
    t = (0.14/((psm**0.02)-1))
    k = round(t, 2)
    actualrelay = round(k*m[4], 2)
    return render_template('predict.html', pick=(pickup), result=(faultrelay), psm=(psm), time=(k), actual=(actualrelay))


@app.route('/relaytrip', methods=['POST'])
def relaytrip():
    input_data = [x for x in request.form.values()]
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    print(input_data)
    print(input_data_as_numpy_array)
    print(input_data_reshaped)
    z = len(input_data)
    str = input_data[2]
    str1 = input_data[0]
    str2 = input_data[1]
    k = str.split(":")
    k1 = str1.split("+j")
    k2 = str2.split("+j")
    m = k1+k2+k
    lis = []
    for i in range(3, z):
        m.append(input_data[i])
    for z in m:
        lis.append(float(z))
    print(lis)
    is1 = (complex(lis[0], lis[1])*lis[5])/lis[4]
    is2 = (complex(lis[2], lis[3])*lis[5])/lis[4]
    print(is2)
    print(is1)
    id = is1-is2
    id = id.real
    id = round(id, 2)
    ir = (is1+is2)/2
    ir = ir.real
    ir = round(ir, 2)
    b = ir*lis[7]/100
    b = round(b, 2)
    if(id > b):
        k = "Operating torque is greater than Restraining Torque hence the relay operates"
    elif(id < b):
        k = "Operating torque is smaller than Restraining Torque hence the relay dosent operates"
    elif(id == b):
        k = "Operating torque is equal to Restraining Torque hence the relay is on the verge of operation"
    x = np.linspace(0, 20, 100)
    data1 = (lis[7]/100)*x
    x2 = abs(ir)
    data2 = abs(id)
    plt.ylabel("Operating Current (I1-I2)")
    plt.xlabel("Restraining Current ((I1+I2)/2)")
    plt.plot(x, data1)
    plt.plot(x2, data2, '--bo')

    plt.text(14.0, 1.9, "Positive Torque")
    plt.text(17.5, 0, "Negative Torque")
    plt.show()
    dir_name = "C:/Users/yashs/Desktop/PSPS/static/css"
    plt.rcParams["savefig.directory"] = os.chdir(os.path.dirname(dir_name))
    plt.savefig("img.png")
    plt.close()
    return render_template('relaytrip.html', ic1=(is1), ic2=(is2), id=(id), ir=(ir), b=(b), k=(k), slope=(input_data[4]))


if __name__ == "__main__":
    app.run(debug=True)
