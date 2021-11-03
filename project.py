import csv
import time
import sys
import math
import random
import json
from tqdm import tqdm


FILENAME = "TFT_set4_euw_challanger_games.csv"
important_fields = [1, 2, 3, 4, 10, 11, 12, 13]
field_names = ['match_id', 'puuid', 'placement', 'level', 'chosen_unit', 'chosen_trait', 'units', 'traits']
field_types = ['str', 'str', 'int', 'int', 'str', 'str', 'json', 'json']
ints = [3, 4]
jsons = [12, 13]
#string, string, int, int, string, string, json, json

#{'match_id':'' , 'puuid':'' ,  'placement':# ,  'level':# , 'chosen_unit':'' , 'chosen_trait':'' , 'units': {'unit':{'items':[] , 'stars':#}} 'traits': {'trait':#}}

MOST_RECENT_TIME = 0
TIMER_START = 0
PRINT_TIMERS = True
champions = {   'Aatrox': {'cost':4, 'traits':["Cultist", "Vanguard"]}, 'Ahri': {'cost':4, 'traits':["Spirit", "Mage"]}, 'Akali': {'cost':3, 'traits':["Ninja", "Assassin"]},
                'Annie': {'cost':2, 'traits':["Fortune", "Mage"]}, 'Aphelios': {'cost':2, 'traits':["Moonlight", "Hunter"]}, 'Ashe': {'cost':4, 'traits':["Elderwood", "Hunter"]},
                'Azir': {'cost':5, 'traits':["Warlord", "Keeper", "Emperor"]}, 'Cassiopeia': {'cost':4, 'traits':["Dusk", "Mystic"]}, 'Diana': {'cost':1, 'traits':["Moonlight", "Assassin"]},
                'Elise': {'cost':1, 'traits':["Cultist", "Keeper"]}, 'Evelynn': {'cost':3, 'traits':["Cultist", "Shade"]}, 'Ezreal': {'cost':5, 'traits':["Elderwood", "Dazzler"]},
                'Fiora': {'cost':1, 'traits':["Enlightened", "Duelist"]}, 'Garen': {'cost':1, 'traits':["Warlord", "Vanguard"]}, 'Hecarim': {'cost':2, 'traits':["Elderwood", "Vanguard"]},
                'Irelia': {'cost':3, 'traits':["Enlightened", "Divine", "Adept"]}, 'Janna': {'cost':2, 'traits':["Enlightened", "Mystic"]}, 'JarvanIV': {'cost':2, 'traits':["Warlord", "Keeper"]},
                'Jax': {'cost':2, 'traits':["Divine", "Duelist"]}, 'Jhin': {'cost':4, 'traits':["Cultist", "Sharpshooter"]}, 'Jinx': {'cost':3, 'traits':["Fortune", "Sharpshooter"]},
                'Kalista': {'cost':3, 'traits':["Cultist", "Duelist"]}, 'Katarina': {'cost':3, 'traits':["Warlord", "Fortune", "Assassin"]}, 'Kayn': {'cost':5, 'traits':["Tormented", "Shade"]},
                'Kennen': {'cost':3, 'traits':["Ninja", "Keeper"]}, 'Kindred': {'cost':3, 'traits':["Spirit", "Hunter"]}, 'LeeSin': {'cost':5, 'traits':["Divine", "Duelist"]},
                'Lillia': {'cost':5, 'traits':["Dusk", "Mage"]}, 'Lissandra': {'cost':1, 'traits':["Moonlight", "Dazzler"]}, 'Lulu': {'cost':2, 'traits':["Elderwood", "Mage"]},
                'Lux': {'cost':3, 'traits':["Divine", "Dazzler"]}, 'Maokai': {'cost':1, 'traits':["Elderwood", "Brawler"]}, 'Morgana': {'cost':4, 'traits':["Enlightened", "Dazzler"]},
                'Nami': {'cost':1, 'traits':["Enlightened", "Mage"]}, 'Nidalee': {'cost':1, 'traits':["Warlord", "Sharpshooter"]}, 'Nunu': {'cost':3, 'traits':["Elderwood", "Brawler"]},
                'Pyke': {'cost':2, 'traits':["Cultist", "Assassin"]}, 'Riven': {'cost':4, 'traits':["Dusk", "Keeper"]}, 'Sejuani': {'cost':4, 'traits':["Fortune", "Vanguard"]},
                'Sett': {'cost':5, 'traits':["Boss", "Brawler"]}, 'Shen': {'cost':4, 'traits':["Ninja", "Adept", "Mystic"]}, 'Sylas': {'cost':2, 'traits':["Moonlight", "Brawler"]},
                'TahmKench': {'cost':1, 'traits':["Fortune", "Brawler"]}, 'Talon': {'cost':4, 'traits':["Enlightened", "Assassin"]}, 'Teemo': {'cost':2, 'traits':["Spirit", "Sharpshooter"]},
                'Thresh': {'cost':2, 'traits':["Dusk", "Vanguard"]}, 'TwistedFate': {'cost':1, 'traits':["Cultist", "Mage"]}, 'Vayne': {'cost':1, 'traits':["Dusk", "Sharpshooter"]},
                'Veigar': {'cost':3, 'traits':["Elderwood", "Mage"]}, 'Vi': {'cost':2, 'traits':["Warlord", "Brawler"]}, 'Warwick': {'cost':4, 'traits':["Divine", "Hunter", "Brawler"]},
                'Wukong': {'cost':1, 'traits':["Divine", "Vanguard"]}, 'XinZhao': {'cost':3, 'traits':["Warlord", "Duelist"]}, 'Yasuo': {'cost':1, 'traits':["Exile", "Duelist"]},
                'Yone': {'cost':5, 'traits':["Exile", "Adept"]}, 'Yuumi': {'cost':3, 'traits':["Spirit", "Mystic"]}, 'Zed': {'cost':1, 'traits':["Ninja", "Shade"]},
                'Zilean': {'cost':5, 'traits':["Cultist", "Mystic"]} }
trait_breakpoints = {   "Cultist": [3, 6, 9], "Divine": [2, 4, 6, 8], "Dusk": [2, 4, 6], "Elderwood":[3, 6, 9], "Enlightened": [2, 4, 6], "Moonlight": [3, 5],
                        "Ninja": [1, 4], "Spirit": [2, 4], "Boss": [1], "Tormented": [1], "Warlord": [3, 6, 9], "Adept": [2, 3, 4], "Assassin":[2, 4, 6], "Mystic": [2, 4, 6],
                        "Brawler": [2, 4, 6, 8], "Dazzler": [2, 4], "Duelist": [2, 4, 6, 8], "Emperor":[1], "Hunter": [2, 3, 4, 5], "Keeper":[2, 4, 6], "Mage":[3, 6, 9],
                        "Shade": [2, 3, 4], "Sharpshooter":[2, 4, 6], "Vanguard":[2, 4, 6, 8]   }
def parse_raw_data():
    file = open(FILENAME)
    num_lines = len(file.readlines())
    file.close()
    file = open(FILENAME)
    reader = csv.reader(file)
    fields = next(reader)
    parsed_data = []
    print("Loading raw match data...")
    for x in tqdm(range(1, num_lines)):
        data = next(reader)
        new_data = {}
        for i in range(len(important_fields)):
            field_val = important_fields[i]
            key = field_names[i]
            value = data[field_val]
            if field_val in ints:
                value = int(value)
            elif field_val in jsons:
                value = value.replace("\'", '\"')
                value = json.loads(value)
            new_data[key] = value
        parsed_data.append(new_data)
    display_timer_data("parsing raw data")
    return parsed_data

def parse_true_test_set(filename):
    file = open(filename)
    num_lines = len(file.readlines())
    file.close()
    file = open(filename)
    reader = csv.reader(file)
    fields = next(reader)
    parsed_data = []
    print("Loading test data...")
    for x in tqdm(range(1, num_lines)):
        data = next(reader)
        new_data = {}
        jsons = [0, 1, 5, 8]
        y = 0
        for y in range(len(data)):
            value = data[y]
            if y in jsons:
                value = value.replace("\'", '\"')
                value = json.loads(value)
            new_data[fields[y]] = value
        parsed_data.append(new_data)
    display_timer_data("parsing test data")
    return parsed_data

def write_simple_data(filename, data):
    file = open(filename, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(field_names)
    print(f"Writing data to {filename}...")
    for data_index in tqdm(range(len(data))):
        row = data[data_index]
        rowValues = []
        x = 0
        for key in row:
            if field_types[x] == 'json':
                row[key] = json.dumps(row[key])
            x+=1
            rowValues.append(row[key])
        writer.writerow(rowValues)
    display_timer_data(f"writing data to {filename}")

def create_test_set(test_filename, train_filename, raw_data, percent):
    numTests = int((percent/100.0) * len(raw_data))
    sample = random.sample(range(len(raw_data)), numTests)
    test_data = []
    train_data = []
    print(f"Splitting into train and test sets...")
    for x in tqdm(range(len(raw_data))):
        if x in sample:
            #x is part of the test_data set
            test_data.append(raw_data[x])
        else:
            #x is part of the train_data set
            train_data.append(raw_data[x])
    display_timer_data("splitting into train and test sets")
    write_simple_data(test_filename, test_data)
    write_simple_data(train_filename, train_data)

def put_in_buckets(data):
    buckets = []

    for x in tqdm(range(len(data))):
        point = data[x]
        good_fit = False
        for bucket in buckets:
            if team_fits_in_bucket(point, bucket):
                good_fit = True
                bucket.append(point)
                break
        if not good_fit:
            buckets.append([point])
    return buckets

def team_fits_in_bucket(team, bucket):
    if len(bucket) == 0:
        return True
    for trait in team['traits']:
        #print(trait)
        if trait not in bucket[0]['traits']:
            #print("returning")
            return False
        else:
            dictn = bucket[0]['traits']
            #print(type(dictn))
            #print(dictn)
            if team['traits'][trait] != bucket[0]['traits'][trait]:
                return False
    return True

def team_is_similar(team, team2):
    numSame = 0
    total = 0
    for unit in team['units']:
        if unit in team2['units']:
            numSame+=1
        total+=1
    return (numSame >= total*0.9)

def team_is_subset(team, super_team):
    for unit in team['units']:
        if unit not in super_team['units']:
            return False
    return True

def team_is_superset(team, set):
    for subteam in set:
        if not team_is_subset(subteam, team):
            return False
    return True

def read_simple_data(filename):
    file = open(filename)
    num_lines = len(file.readlines())
    file.close()
    file = open(filename)
    reader = csv.reader(file)
    fields = next(reader)
    parsed_data = []
    print("Loading simplified data...")
    for x in tqdm(range(1, num_lines)):
        data = next(reader)
        new_data = {}
        for i in range(len(data)):
            key = field_names[i]
            value = data[i]
            if field_types[i] == 'int':
                value = int(value)
            elif field_types[i] == 'json' or key == 'units' or key == 'traits':
                value = value.replace("\'", '\"')
                value = json.loads(value)
            new_data[key] = value
        parsed_data.append(new_data)
    display_timer_data("parsing simplified data")
    return parsed_data

def get_winners(simplified_data):
    winners = []
    for x in tqdm(range(len(simplified_data))):
        data = simplified_data[x]
        if data['placement'] == 1:
            winners.append(data)
    return winners

def get_top_four(simplified_data):
    winners = []
    for x in tqdm(range(len(simplified_data))):
        data = simplified_data[x]
        if data['placement'] <= 4:
            winners.append(data)
    return winners

def calculate_traits(champion_names, chosen_trait=None, chosen_unit=None):
    counted = []
    traits = {}
    for champ_name in champion_names:
        if champ_name not in counted:
            counted.append(champ_name)
            champ_traits = champions[champ_name]['traits']
            for trait in champ_traits:
                if trait not in traits:
                    traits[trait] = 1
                else:
                    traits[trait] = traits[trait]+1

    if chosen_trait is not None:
        if chosen_trait in traits:
            traits[chosen_trait] = traits[chosen_trait]+1
        else:
            traits[chosen_trait] = 1

    return traits

def team_similarity(early_team, final_team):
    early_traits = calculate_traits(early_team['units'], early_team['chosen_trait'], early_team['chosen_unit'])
    early_units = early_team['units']
    final_traits = final_team['traits']
    final_units = final_team['units']
    unit_similarity = 0
    num_units = 0
    for unit in early_units:
        num_units+=1
        if unit in final_units:
            early_stars = early_units[unit]['stars']
            final_stars = final_units[unit]['stars']
            if final_stars>=early_stars:
                unit_similarity+=1
            else:
                unit_similarity+=(0.5)**(early_stars-final_stars) #0.5 if difference = 1; 0.25 if difference is 2
    trait_similarity = 0
    num_traits = 0
    for trait in early_traits:
        num_traits+=1
        if trait in final_traits:
            early_rank = early_traits[trait]
            final_rank = final_traits[trait]
            if final_rank >= early_rank:
                trait_similarity+=1
            else:
                trait_similarity += float(final_rank) / early_rank

    return (0.4*trait_similarity)+(0.6*unit_similarity)

def find_nearest_neighbors(data, team, num_neighbors=5):
    neighbor_similarity = [-1]*num_neighbors
    neighbors = [None]*num_neighbors
    for point in data:
        least_similar_index = find_minimum(neighbor_similarity)
        similarity = team_similarity(team, point)
        if similarity > neighbor_similarity[least_similar_index]:
            neighbors[least_similar_index] = point
            neighbor_similarity[least_similar_index] = similarity
    return neighbors

def pure_nearest_neighbors(test_data, train_data):
    results = []
    for x in tqdm(range(len(test_data))):
        test_point = test_data[x]
        neighbor = find_nearest_neighbors(train_data, test_point, 1)[0]
        results.append(neighbor['units'])
    return results

def do_test(test_set, train_set):
    results = pure_nearest_neighbors(test_set, train_set)
    num_results = len(results)
    sum_results = 0
    exactly_correct=0.0
    print("Testing results...")
    for x in tqdm(range(num_results)):
        result_units = results[x].keys()
        true_units = test_set[x]['final_units'].keys()
        same = 0.0
        total = 0.0
        for key in true_units:
            if key in result_units:
                same+=1
            total+=1
        if total != 0:
            sum_results+=(same/total)
            if same == total:
                exactly_correct+=1
    display_timer_data("Testing results")
    print(f"Number exactly correct: {exactly_correct} [{exactly_correct*100/num_results}% of results]")
    print(f"Average accuracy: {sum_results/num_results}")

def bucketing_test(test_set, buckets):
    results = []
    for x in tqdm(range(len(test_set))):
        point = test_set[x]
        best_bucket = 0
        best_similarity = -1
        index = 0
        for bucket in buckets:
            similarity = team_similarity(point, bucket[0])
            if similarity > best_similarity:
                best_similarity = similarity
                best_bucket = index
            index+=1
        best_team_sim = -1
        best_team = 0
        index = 0
        for team in buckets[best_bucket]:
            similarity = team_similarity(point, bucket[0])
            if similarity > best_team_sim:
                best_team_sim = similarity
                best_team = index
            index+=1
        results.append(buckets[best_bucket][best_team]['units'])
    print("Testing results...")
    num_results = len(results)
    sum_results = 0
    exactly_correct=0.0
    close = 0.0
    for x in tqdm(range(num_results)):
        result_units = results[x].keys()
        true_units = test_set[x]['final_units'].keys()

        same = 0.0
        total = 0.0
        for key in true_units:
            if key in result_units:
                same+=1
            total+=1
        if total != 0:
            sum_results+=(same/total)
            if same == total:
                exactly_correct+=1
            elif same >= total*0.9:
                close +=1
    display_timer_data("Testing results")
    print(f"Number exactly correct: {exactly_correct} [{exactly_correct*100/num_results}% of results]")
    print(f"Number close but not exact: {close} [{close*100/num_results}% of results]")
    print(f"Average accuracy: {sum_results/num_results}")

def create_true_test_set(output_filename, data):
    data = back_in_time(data)
    file = open(output_filename, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow(['final_units', 'final_traits', 'final_chosen_unit', 'final_chosen_trait', 'final_placement', 'units', 'chosen_unit', 'chosen_trait', 'traits'])
    print(f"Writing data to {output_filename}...")
    for data_index in tqdm(range(len(data))):
        row = data[data_index]
        rowValues = []
        x = 0
        for key in row:
            if x in [0, 1, 5, 8]:
                row[key] = json.dumps(row[key])
            x+=1
            rowValues.append(row[key])
        writer.writerow(rowValues)
    display_timer_data(f"Writing data to {output_filename}")

def find_minimum(arr):
    min = arr[0]
    i = 0
    for x in range(1, len(arr)):
        if arr[x]<min:
            min=arr[x]
            i=x
    return i

def display_timer_data(str):
    global MOST_RECENT_TIME
    if PRINT_TIMERS:
        cur_time = time.perf_counter()
        print(f"Finished {str} after {round(cur_time-TIMER_START)} seconds. (Took {round(cur_time-MOST_RECENT_TIME, 2)} seconds)")
        MOST_RECENT_TIME = cur_time

def back_in_time(data):
    output_data = []
    for x in tqdm(range(len(data))):
        player = data[x]
        new_entry = {}
        new_entry['final_units'] = player['units']
        new_entry['final_traits'] = player['traits']
        new_entry['final_chosen_unit'] = player['chosen_unit']
        new_entry['final_chosen_trait'] = player['chosen_trait']
        new_entry['final_placement'] = player['placement']
        new_entry['units'] = {}
        for unit in player['units']:
            #unit is a key;player['units'] is a dictionary
            unitInfo = player['units'][unit]
            if unitInfo['stars'] == 3:
                if unit not in new_entry['units']:
                    new_entry['units'][unit] = {'items': [], 'stars': 2}
                else:
                    new_entry['units'][unit]['stars'] = 2
            elif unitInfo['stars'] == 2:
                #TODO: improve this later
                if random.random() < 0.2:
                    if unit not in new_entry['units']:
                        new_entry['units'][unit] = {'items': [], 'stars': 2}
                    else:
                        new_entry['units'][unit]['stars'] = 2
                else:
                    if unit not in new_entry['units']:
                        new_entry['units'][unit] = {'items': [], 'stars': 1}
        if random.random() < 0.2:
            new_entry['chosen_unit'] = new_entry['final_chosen_unit']
            new_entry['chosen_trait'] = new_entry['final_chosen_trait']
        else:
            new_entry['chosen_unit'] = ''
            new_entry['chosen_trait'] = None
        new_entry['traits'] = calculate_traits(new_entry['units'].keys(), new_entry['chosen_trait'], new_entry['chosen_unit'])
        output_data.append(new_entry)
    return output_data

def simplify_traits(data):
    for point in data:
        for key in trait_breakpoints:
            if key in point['traits']:
                if point['traits'][key] < trait_breakpoints[key][0]:
                    point['traits'].pop(key, None)
                else:
                    for x in range(len(trait_breakpoints[key])):
                        i = len(trait_breakpoints[key])-1-x
                        if point['traits'][key] > trait_breakpoints[key][i]:
                            point['traits'][key] = trait_breakpoints[key][i]
                            break

def setup():
    global TIMER_START
    TIMER_START = time.perf_counter()

def main():
    test = parse_true_test_set('pure_test_data.csv')
    train = read_simple_data('train_set_winners.csv')
    simplify_traits(train)
    buckets = put_in_buckets(train)
    maxlength = 0
    nums =   [1, 5, 10, 25, 50, 100]
    counts = [0, 0, 0,  0,  0,  0]
    for bucket in buckets:
        for i in range(len(counts)):
            if len(bucket) > nums[i]:
                counts[i]+=1
        if len(bucket) > maxlength:
            maxlength=len(bucket)
    new_dataset = []
    for bucket in buckets:
        if len(bucket) >= 1:
            new_dataset.append(bucket)
    bucketing_test(test, new_dataset)

if __name__ == '__main__':
    setup()
    main()
