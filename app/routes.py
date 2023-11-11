from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, SignupForm, PokeSelect
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/', methods=['GET', 'POST'])
def poke_home():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit:
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f"Hello, {queried_user.first_name}!", 'success')
            return redirect(url_for('poke_data'))
        else:
            return "Invalid email or password"
    else:
        return render_template('index.html', form=form)
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()

    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        #create an instance of our user class
        user = User(first_name, last_name, email, password, team=[] if user.team is None else user.team)

        # add user to database
        db.session.add(user)
        db.session.commit()

        flash(f"Thank you for signing up {first_name}!", 'success')
        return redirect(url_for('poke_home'))
    else:
        return render_template('signup.html', form=form)


@app.route('/logout')
@login_required
def logout():
    flash("Successfully logged out!", 'warning')
    logout_user()
    return redirect(url_for('poke_home'))



@app.route('/portal', methods=['GET', 'POST'])
@login_required
def poke_data():
    form = PokeSelect()
    if request.method == 'POST':

        name = form.poke_name.data

        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        response = requests.get(url)
        data = response.json()
        try:


            poke_dict = {
                'name': data['forms'][0]['name'].title(),
                'base_experience': data['base_experience'],
                'sprite': data['sprites']['front_shiny'],
                'ATK_base': data['stats'][1]['base_stat'],
                'HP_base': data['stats'][0]['base_stat'],
                'DEF_base': data['stats'][2]['base_stat'],
                'type': data['types'][0]['type']['name'].title()
        }
            

            abilities = data['abilities']
            for i, ability in enumerate(abilities):
                ability_url = ability['ability']['url']
                ability_resonse = requests.get(ability_url)
                ability_data = ability_resonse.json()
                key = f"ability_{i+1}"
                poke_dict[key] = {
                    'name': ability_data['name'].title(),
                    'description': ability_data['effect_entries'][1]['effect']
                }


            all_poke = poke_dict
            return render_template('user_portal.html', all_poke=all_poke, form=form, username=current_user.first_name)
        except IndexError:
            return redirect('/bug')
    else:
        return render_template('user_portal.html', form=form, username=current_user.first_name)
    

@app.route('/add_to_team/<pokemon_name>', methods=['GET', 'POST'])
def add_to_team(pokemon_name):
    if current_user.team is None:
        current_user.team=[]


    current_user.team.append(pokemon_name)
    db.session.commit()

    flash(f"{pokemon_name} added to your team!, 'success")
    return redirect(url_for('poke_data'))


@app.route('/bug')
def found_bug():
    return render_template('foundbug.html')

@app.route('/team')
@login_required
def user_team():
    return render_template('user_team.html', username=current_user.first_name)