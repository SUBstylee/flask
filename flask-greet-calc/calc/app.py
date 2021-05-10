from flask import Flask, request
from operations import *

app = Flask(__name__)


@app.route('/add')
def op_add():
    '''Adds params a and b'''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = add(a, b)
    return str(result)


@app.route('/sub')
def op_sub():
    '''Subtracts param a from param b'''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = sub(a, b)
    return str(result)


@app.route('/mult')
def op_mult():
    '''Multiplies params a and b'''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = mult(a, b)
    return str(result)


@app.route('/div')
def op_div():
    '''Divides param a by param b'''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = div(a, b)
    return str(result)

# further study


operations = {
    'add': add,
    'sub': sub,
    'mult': mult,
    'div': div
}


@app.route('/math/<operation>')
def mult_op(operation):
    '''Performs operation based on route, operation matched to dictionary and a,b request'''
    a = int(request.args.get('a'))
    b = int(request.args.get('b'))
    result = operations[operation](a, b)
    return str(result)
