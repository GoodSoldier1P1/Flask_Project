from . import main
from flask_login import login_required, current_user
import requests
from flask import render_template, request, redirect, url_for, flash
from app.forms import PokeSelect
from app.models import Pokemon, db, User, added_to_team



@main.route('/portal', methods=['GET', 'POST'])
@login_required
def poke_data():
    form = PokeSelect()

    if request.method == 'POST':

        name = form.poke_name.data
        poke = Pokemon.query.filter_by(poke_id=name).first()

        if poke:

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

                new_poke = Pokemon(poke_id=name)
                
                db.session.add(new_poke)
                db.session.commit()


    else:
        return render_template('/user_portal.html', form=form, username=current_user.first_name)
    

@main.route('/add_to_team/<pokemon_name>', methods=['GET', 'POST'])
@login_required
def add_to_team(pokemon_name):

    print(f"Pokemon Name: {pokemon_name}")

    user_id = current_user.id

    trainer = User.query.get(user_id)
    print(trainer)
    poke = Pokemon.query.filter_by(poke_id=pokemon_name.lower()).first()
    print(poke)

    if trainer and poke:
        if len(trainer.team.all()) < 6 and poke not in trainer.team:
            print('Do It')
            trainer.team.append(poke)

            db.session.commit()
    
            flash(f"{pokemon_name} added to your team!", 'success')
        
        else:
            print("Don't Do It")
            flash("Your team is already full (6 Pokemon Max) OR Pokemon is already on your team", 'danger')
    else:
        print("Can't Do It")
        flash("User or Pokemon not found", 'danger')

    return redirect(url_for('main.poke_data'))


@main.route('/bug')
def found_bug():
    return render_template('foundbug.html')

@main.route('/team', methods=['GET', 'POST'])
@login_required
def user_team():
    
    pokemons = current_user.team.all()
    print(pokemons)
    print('user')

    poke_names = [pokemon.poke_id for pokemon in pokemons]
    print(poke_names)
    print('user')
    
    return render_template('user_team.html', poke_names=poke_names)


@main.route('/delete/<string:poke_name>', methods=['GET', 'POST'])
@login_required
def remove_pokemon(poke_name):
    pokemon = Pokemon.query.filter_by(poke_id=poke_name).first()
    print('before delete if')
    print(pokemon)

    if pokemon and current_user.id == current_user.team.first():
        print('delete if')
        print(current_user.id)
        current_user.team.delete(pokemon)
        db.session.commit()
        return redirect(url_for('main.user_team'))
    else:
        print('delete else')
        print("How About No")
        flash(f"{pokemon} has been released!")
        return redirect(url_for('main.user_team'))