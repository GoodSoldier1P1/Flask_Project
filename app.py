from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def poke_home():
    if request.method == 'POST':
        return render_template('user_portal.html')
    else:
        return render_template('index.html')
    

@app.route('/portal', methods=['GET', 'POST'])
def poke_data():
    if request.method == 'POST':
        name = request.form.get('name')

        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        data = response.json()
        try:
            poke_dict = {
                'name': data['forms'][0]['name'].title(),
                'ability': data['abilities'][0]['ability']['name'].title(),
                'ability_2': data['abilities'][1]['ability']['name'].title(),
                'base_experience': data['base_experience'],
                'sprite': data['sprites']['front_shiny'],
                'ATK_base': data['stats'][1]['base_stat'],
                'HP_base': data['stats'][0]['base_stat'],
                'DEF_base': data['stats'][2]['base_stat'],
                'type': data['types'][0]['type']['name'].title()
        }
            all_poke = poke_dict
            return render_template('user_portal.html', all_poke=all_poke)
        except IndexError:
            return 'Please enter a valid poke name (or number)'
    else:
        return render_template('user_portal.html')