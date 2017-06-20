#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Ne pas se soucier de ces imports
import setpath
from flask import Flask, render_template, session, request, redirect, flash
from getpage import getPage

app = Flask(__name__)

app.secret_key = "TODO: mettre une valeur secrète ici"


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Si vous définissez de nouvelles routes, faites-le ici

@app.route('/new-game', methods=['POST'])
def getData():
	if request.method == 'POST':
		session["article"] = request.form['firstPage']
		session["score"] = 0
		
		if request.form['firstPage'] == "Philosophie" :
			flash("Choix de Philosophie impossible. Veuillez réessayer !", 'error')
			return redirect("/")
		
		if request.form['firstPage'] == "" :
			flash("Choix invalide. Veuillez réessayer !", 'error')
			return redirect("/")

		for i in getPage(request.form['firstPage'])[1] :
			if i == "Philosophie" :
				flash("La page redirige automatiquement vers Philosophie. Veuillez réessayer !", 'error')
				return redirect("/")
			else :
				pass

		
		return redirect("/game")
	else :
		error = 'Verification'
	# return render_template('/game')



@app.route('/game', methods=['GET'])
def game():

	title, l = getPage(session["article"])
	if l==[]:
		flash("Page non disponible. Veuillez réessayer !", 'error')
		session["score"] = 0
		return redirect("/")
	if title == "Philosophie" :
		flash("Victoire! Votre score est de", 'info')
		return redirect("/")


	return render_template('game.html', l=l)


@app.route('/move', methods=['POST'])
def move():

		session["article"] = request.form["destination"]
		
		if session["article"] == "Philosophie":
			flash("Victoire! Votre score est de ", 'info')
			return redirect("/")
		else :
			session["score"] = session["score"] + 1
			return redirect("/game")
 
if __name__ == '__main__':
    app.run(debug=True)

