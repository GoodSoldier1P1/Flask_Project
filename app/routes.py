from flask import request, render_template, redirect
import requests
from app import app
from app.forms import LoginForm, SignupForm, PokeSelect

@app.route('/', methods=['GET', 'POST'])
def poke_home():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USERS and REGISTERED_USERS[email]['password'] == password:
            return redirect('/portal')
        else:
            return "Invalid email or password"
    else:
        return render_template('index.html', form=form)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        full_name = f"{form.first_name.data} {form.last_name.data}"
        email = form.email.data
        password = form.password.data

        REGISTERED_USERS[email] = {
            'name': full_name,
            'password': password
        }

        return redirect('/')
    else:
        return render_template('signup.html', form=form)


REGISTERED_USERS = {
    'danielamyx859@gmail.com': {
        'name': 'Daniel Amyx',
        'password': 'Isaac2023'
    },
    'dkatina@gmail.com': {
        'name': 'Dylan Katina',
        'password': 'test'
    }
}

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
            return redirect('/bug')
    else:
        return render_template('user_portal.html')
    


@app.route('/bug')
def found_bug():
    return render_template('foundbug.html')