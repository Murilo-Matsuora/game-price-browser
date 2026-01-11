from flask import Flask, url_for, render_template, request, redirect
import requests
import datetime

nexarda_url = "https://www.nexarda.com/api/v3"

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html", year = datetime.datetime.today().year)

@app.route("/search", methods=["GET", "POST"])
def search_game():

    if request.method == "POST":
        query = request.form.get("game_query")
        return redirect(url_for("search_game", game_query=query))
    
    query = request.args.get("game_query")
    if not query:
        return redirect(url_for("home"))
    
    params = {
        "q": query,
        "type": "games",
        "currency": "USD"
    }
    response = requests.get(f"{nexarda_url}/search", params=params)
    response.raise_for_status()

    games = response.json()["results"]["items"]

    return render_template("search.html", games=games, query=query)

@app.route("/game/<id>", methods=["GET"])
def game_details(id):
    params = {
        "id": id,
        "type": "game",
        "currency": "USD"
    }

    response = requests.get(f"{nexarda_url}/prices", params=params)
    response.raise_for_status()

    game = response.json()["info"]
    prices = response.json()["prices"]
    
    return render_template("game.html", game=game, prices=prices)

if __name__ == "__main__":
    app.run(debug=True)