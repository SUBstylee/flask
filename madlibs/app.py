from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from stories import stories

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
debug = DebugToolbarExtension(app)


@app.route('/')
def get_story():
    '''User picks a story'''
    return render_template('choice.html', stories=stories.values())


@app.route('/questions')
def gather_words():
    '''Generate form for words'''

    story_id = request.args['story_id']
    story = stories[story_id]
    prompts = story.prompts

    return render_template('questions.html', story_id=story_id, title=story.title, prompts=prompts)


@app.route('/story')
def print_story():
    '''Print story on page'''
    story_id = request.args['story_id']
    story = stories[story_id]
    text = story.generate(request.args)

    return render_template('story.html', title=story.title, text=text)
