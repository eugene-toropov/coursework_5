from flask import render_template, Flask, url_for, request
from werkzeug.utils import redirect

from classes import unit_classes
from unit import EnemyUnit, PlayerUnit
from base import Arena
from equipment import Equipment

app = Flask(__name__)

heroes = {
    "player": None,
    "enemy": None,
}

arena = Arena()


@app.route("/")
def menu_page():
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        return arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    arena.stop_game()
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():

    if request.method == 'GET':
        equipment = Equipment()

        header = 'Выберите героя'
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html',result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        player.equip_weapon(Equipment().get_weapon(weapon_name))
        player.equip_armor(Equipment().get_armor(armor_name))

        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == 'GET':
        equipment = Equipment()

        header = 'Выберите противника'
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        result = {
            'header': header,
            'weapons': weapons,
            'armors': armors,
            'classes': unit_classes,
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form['name']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        unit_class_name = request.form['unit_class']

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class_name))

        enemy.equip_weapon(Equipment().get_weapon(weapon_name))
        enemy.equip_armor(Equipment().get_armor(armor_name))

        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run(port=15000)
