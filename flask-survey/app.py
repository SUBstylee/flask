# import
from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
# app
app = Flask(__name__)

app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)
# variables
# store responses, references length to check if correct question
CURRENT_SURVEY_KEY = 'current_survey'  # which survey is being taken
RESPONSES_KEY = 'responses'
# routes


@app.route('/')
def show_root():
    '''show survey selection page'''
    return render_template('survey-choice.html', surveys=surveys)


@app.route('/', methods=['POST'])
def survey_choice():
    '''pick a survery'''
    survey_id = request.form['survey_code']
    survey = surveys[survey_id]
    # check if survey has already been completed
    if request.cookies.get(f"completed_{survey_id}"):
        return render_template("completed.html", survey=survey)

    session[CURRENT_SURVEY_KEY] = survey_id

    return render_template('survey.html', survey=survey)


@app.route('/start', methods=['POST'])
def start_survey():
    '''start the survey'''
    session[RESPONSES_KEY] = []
    return redirect('/question/0')


@app.route('/answer', methods=['POST'])
def save_answer():
    '''save answer, then go to next question'''
    choice = request.form['answer']
    text = request.form.get('text', '')

    responses = session[RESPONSES_KEY]
    responses.append({'choice': choice, 'text': text})

    session[RESPONSES_KEY] = responses
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if(len(responses) == len(survey.questions)):
        return redirect('/finished')
    else:
        return redirect(f'/question/{len(responses)}')


@app.route('/question/<int:q_id>')
def show_question(q_id):
    '''display question and options'''
    responses = session.get(RESPONSES_KEY)
    survey_code = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_code]

    if(responses is None):
        # too soon
        flash('You are accessing the survey too soon.')
        return redirect('/')
    if(len(responses) == len(survey.questions)):
        # finished
        return redirect('/finished')
    if(len(responses) != q_id):
        # out of order
        flash('You are accessing the questions out of order.')
        return redirect(f'/question/{len(responses)}')
    # pass question
    question = survey.questions[q_id]
    return render_template('question.html', q_num=q_id, question=question)


@app.route('/finished')
def finished():
    '''let user know survey is complete'''
    survey_id = session[CURRENT_SURVEY_KEY]
    survey = surveys[survey_id]
    responses = session[RESPONSES_KEY]

    html = render_template('finished.html', survey=survey, responses=responses)

    # Set cookie noting this survey is done so they can't re-do it
    response = make_response(html)
    response.set_cookie(f"completed_{survey_id}", "yes", max_age=60)
    return response
