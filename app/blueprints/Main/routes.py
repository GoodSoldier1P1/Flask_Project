from . import main
from flask_login import login_required, current_user
import requests
from flask import render_template, request, redirect, url_for, flash
from app.forms import PokeSelect
from app.models import Pokemon, db, User, added_to_team
import random
from sqlalchemy.sql.expression import func



@main.route('/portal', methods=['GET', 'POST'])
@login_required
def poke_data():
    form = PokeSelect()

    if request.method == 'POST':

        name = form.poke_name.data.lower()
        print("Name: ", name)
        poke = Pokemon.query.filter(Pokemon.poke_id.ilike(name)).first()
        print("Poke: ", poke)
        print("This is how we do it")
    
        if poke:
            print("running IF")

            all_poke = {
                'name': poke.poke_id,
                'base_experience': poke.base_xp,
                'sprite': poke.sprite,
                'ATK_base': poke.attack,
                'HP_base': poke.hp,
                'DEF_base': poke.defense,
                'type': poke.poke_type.title(),
                'ability_1': {
                    'name': poke.ability,
                    'description': poke.ability_description
                }
            }

            return render_template('/user_portal.html', all_poke=all_poke, form=form, username=current_user.first_name)
        else:
            print("Running ELSE")
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
                    
                    print('This is i')
                    print(i)
                    print('This is ability')
                    print(ability)

                all_poke = poke_dict

                # ability_key = poke_dict['ability_1']['name'][2]

                print(poke_dict)

                new_poke = Pokemon(poke_id=poke_dict['name'], 
                                sprite=poke_dict['sprite'],
                                poke_type=poke_dict['type'],
                                ability=ability_data['name'], 
                                ability_description=ability_data['effect_entries'][1]['effect'],
                                hp=poke_dict['HP_base'],
                                defense=poke_dict['DEF_base'], 
                                attack=poke_dict['ATK_base'],
                                base_xp=poke_dict['base_experience'])
                
                db.session.add(new_poke)
                db.session.commit()

                return render_template('user_portal.html', all_poke=all_poke, form=form, username=current_user.first_name)
            except IndexError:
                return redirect('/bug')

    else:
        return render_template('/user_portal.html', form=form, username=current_user.first_name)
    

@main.route('/add_to_team/<pokemon_name>', methods=['GET', 'POST'])
@login_required
def add_to_team(pokemon_name):
    if request.method == 'POST':
        debug_pokemon_name = request.form.get('debug_pokemon_name')
        print(f"Received Pokemon Name: {pokemon_name}")
        print(f"Debug Pokemon Name: {debug_pokemon_name}")

    print(f"Pokemon Name: {pokemon_name}")

    user_id = current_user.id

    trainer = User.query.get(user_id)
    print(trainer)
    poke = Pokemon.query.filter(Pokemon.poke_id.ilike(pokemon_name)).first()
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
        print(poke)
        flash("User or Pokemon not found", 'danger')

    return redirect(url_for('main.poke_data'))


@main.route('/bug')
def found_bug():
    return render_template('foundbug.html')

@main.route('/team', methods=['GET', 'POST'])
@login_required
def user_team():

    poke_stats = Pokemon.query.filter_by()
    print("Poke Stats: ", poke_stats)
   
    pokemons = current_user.team.all()
    print(pokemons)
    print('user')

    poke_names = [pokemon.poke_id for pokemon in pokemons]
    print(poke_names)
    print('user')
    
    return render_template('user_team.html', poke_names=poke_names, poke_stats=poke_stats)


@main.route('/delete/<string:poke_name>', methods=['GET', 'POST'])
@login_required
def remove_pokemon(poke_name):
    print(poke_name)
    pokemon = Pokemon.query.filter_by(poke_id=poke_name).first()
    print('before delete if')
    print(pokemon)

    if pokemon:
        print('delete if')
        print(current_user.id)
        current_user.team.remove(pokemon)
        db.session.commit()
        return redirect(url_for('main.user_team'))
    else:
        print('delete else')
        print("How About No")
        flash(f"{pokemon} has been released!")
        return redirect(url_for('main.user_team'))
    





current_index = 0

@main.route('/battle')
@login_required
def battle():

    user_id = current_user.id

    pokemon_data = db.session.query(Pokemon).\
        join(User.team).\
        filter(User.id == user_id).all()
    
    # opponent_data = db.session.query(Pokemon).\
    #     join(User.team).\
    #     filter()

    global current_index
    print("Current Index: ", current_index)
    current_pokemon = pokemon_data[current_index]

    random_opponent = db.session.query(Pokemon).\
        join(added_to_team).filter(added_to_team.c.user_id != user_id).\
            order_by(func.random()).first()
    print("Random Opponent: ", random_opponent)

    return render_template('battle.html', all_poke=current_pokemon, opponent=random_opponent)



@main.route('/next_battle')
@login_required
def next_battle():
    user_id = current_user.id 

    pokemon_data = db.session.query(Pokemon).\
        join(User.team).\
        filter(User.id == user_id).all()
    
    global current_index
    current_index = (current_index + 1) % len(pokemon_data)

    return redirect(url_for('main.battle'))