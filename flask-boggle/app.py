from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

boggle_game = Boggle()


@app.route('/')
def index():
    '''display board'''
    board = boggle_game.make_board()
    # save board to session so it doesn't change on routes
    session['board'] = board
    highscore = session.get('highscore', 0)
    numplays = session.get('numplays', 0)

    return render_template('index.html', board=board, highscore=highscore, numplays=numplays)


@app.route('/check-word')
def check_word():
    '''check if word is in word.txt'''
    word = request.args['word']
    board = session['board']
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})


@app.route('/display-score', methods=['POST'])
def display_score():
    '''update stats'''
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    session['numplays'] = numplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
