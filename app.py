from flask import Flask, render_template, request, session, redirect, flash
import random

app = Flask(__name__)
app.secret_key = "key243462"

choices = ["rock", "paper", "scissors"]

def game(player, computer):
    if player == computer:
        return "draw"
    elif (player == 'rock' and computer == 'scissors') or \
         (player == 'scissors' and computer == 'paper') or \
         (player == 'paper' and computer == 'rock'):
        return "win"
    else:
        return "lose"
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game_page():
    if 'score' not in session:
        session['score'] = {'win': 0, 'lose': 0, 'draw': 0}

    result = None
    computer = None
    score = session['score']

    if request.method == 'POST':
        player = request.form['choice']
        computer = random.choice(choices)
        result = game(player, computer)
        score[result] += 1
        session['score'] = score

        if result == "win":
            flash("You won!", "win")
        elif result == "lose":
            flash("You lost", "lose")
        else:
            flash("Draw", "draw")
        
        session['last_result'] = result
        session['last_computer'] = computer

        return redirect('/game')
    
    result = session.pop('last_result', None)
    computer = session.pop('last_computer', None)
        
    player_score = score['win']
    computer_score = score['lose']

    return render_template('game.html', result=result, computer=computer, score=session['score'], player_score=player_score,
    computer_score=computer_score)

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/game')

if __name__ == '__main__':
    app.run(debug=True)