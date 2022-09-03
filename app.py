
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config["SECRET_KEY"] = "mittens575"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)



@app.route("/")
def home_page():
    """Brings user to home page with questions"""
    return render_template("homepage.html", survey=survey)



@app.route("/begin", methods=["POST"])
def begin_survey():
    """Clear the session of responses."""
    session[RESPONSES_KEY] = []

    return redirect("/questions/0")



@app.route("/answer", methods=["POST"])
def save_responses():
    """Save responses as user goes through the survey"""
    choice = request.form["answer"]

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")



@app.route("/questions/<int:qust>")
def display_question(qust):
    """Display current question."""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != qust):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {qust}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qust]
    return render_template(
        "questions.html", question_num=qust, question=question)



@app.route("/complete")
def complete_survey():
    """Survey completed by user"""
    return render_template("completed.html")