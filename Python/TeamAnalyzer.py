import sqlite3  # This is the package for all sqlite3 access in Python
import sys      # This helps with command-line parameters

# All the "against" column suffixes:
types = ["bug","dark","dragon","electric","fairy","fight",
    "fire","flying","ghost","grass","ground","ice","normal",
    "poison","psychic","rock","steel","water"]

# Take six parameters on the command-line
if len(sys.argv) < 6:
    print("You must give me six Pokemon to analyze!")
    sys.exit()

conn = sqlite3.connect('pokemon.sqlite')

team = []
for i, arg in enumerate(sys.argv):
    if i == 0:
        continue
    # Extra Credit portion: If string get pokedex number
    if isinstance(i, str):
        cursor = conn.execute("SELECT pokedex_number FROM pokemon WHERE name = '"+str(i)+"';")
        for row in cursor:
            i = row[0]

    # Get name of pokemon
    cursor = conn.execute('SELECT name FROM pokemon WHERE pokedex_number = '+str(i)+';')
    for row in cursor:
        name = row[0]

    # Get pokemon type
    cursor = conn.execute('SELECT type_id, which FROM pokemon_type WHERE pokemon_id = '+str(i)+' ORDER BY pokemon_id;')
    type_ids = cursor.fetchall()
    t_1 = type_ids[0][0]
    t_2 = type_ids[1][0]

    cursor = conn.execute('SELECT name FROM type WHERE id == '+str(t_1)+' OR id == '+str(t_2)+';')

    types = cursor.fetchall()
    type1 = types[0][0]
    type2 = types[1][0]

    # Get weak and strong types for the given pokemon's type
    cursor = conn.execute("SELECT against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost, against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water FROM against WHERE type_source_id1 == '" + str(t_1) + "' AND type_source_id2 == '" + str(t_2) + "';")
    w_id = []
    s_id = []
    for row in cursor:
        for num in range(0, len(row)):
            if row[num] > 1:
                w_id.append(num)
            elif row[num] < 1:
                s_id.append(num)

    cursor = conn.execute('SELECT name FROM type ORDER BY name;')
    t_list = cursor.fetchall()[1:]

    weak = []
    for id in w_id:
        weak.append(t_list[id][0])
    strong = []
    for id in s_id:
        strong.append(t_list[id][0])
    # Print Information
    print('Analyzing ' + str(i))
    print(name + ' (' + type1 + ' ' + type2.replace("''", "") + ') is strong against ' + str(strong) + ' but weak against ' + str(weak))


answer = input("Would you like to save this team? (Y)es or (N)o: ")
if answer.upper() == "Y" or answer.upper() == "YES":
    teamName = input("Enter the team name: ")

    # Write the pokemon team to the "teams" table
    print("Saving " + teamName + " ...")

else:
    print("Bye for now!")

