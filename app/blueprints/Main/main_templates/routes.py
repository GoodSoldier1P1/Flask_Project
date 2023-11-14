from . import main
from flask_login import login_required, current_user
import requests
from flask import render_template, request, redirect, url_for, flash
from app.forms import PokeSelect



@main.route('/portal', methods=['GET', 'POST'])
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
    

@main.route('/add_to_team/<pokemon_name>', methods=['GET', 'POST'])
def add_to_team(pokemon_name):
    flash(f"{pokemon_name} added to your team!", 'success')
    return redirect(url_for('main.poke_data'))


@main.route('/bug')
def found_bug():
    return render_template('foundbug.html')

@main.route('/team')
@login_required
def user_team():
    return render_template('user_team.html', username=current_user.first_name)