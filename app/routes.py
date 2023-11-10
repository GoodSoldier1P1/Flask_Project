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
        user = User(first_name, last_name, email, password)

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
    flash("Successfully logged out!" 'warning')
    logout_user()
    return redirect(url_for('poke_home'))



@app.route('/portal', methods=['GET', 'POST'])
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
            return render_template('user_portal.html', all_poke=all_poke, form=form)
        except IndexError:
            return redirect('/bug')
    else:
        return render_template('user_portal.html', form=form)
    


@app.route('/bug')
def found_bug():
    return render_template('foundbug.html')