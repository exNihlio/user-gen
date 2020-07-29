
import random
import json
import sys

#Open the names
male_names = list(open("names/male_names_fixed.txt").readlines())
female_names = list(open("names/female_names_fixed.txt").readlines())
last_names = list(open("names/last_names_fixed.txt").readlines())

#Open the details
user_details = json.load(open("details/details.json"))

# Hobbies
hobbies = json.load(open("hobbies/hobbies.json"))

# Occupations
occupations = json.load(open("occupation/occupations.json"))

#Open the address
streets = list(open("addresses/streets.txt").readlines())
terms = list(open("addresses/term.txt").readlines())
states = list(open("addresses/states.txt").readlines())

name_json = []

#print(str(sys.argv))

arg_num = sys.argv[1]

def _male_female():
  gend_int = _rand_int(1)
  gender =  {
    0: 'male',
    1: 'female'
    }
  return gender[gend_int]

def _first_name(gender):

    global male_names
    global female_names
    if gender == 'male':
        male_random = _rand_int(len(male_names) - 1 )
        return male_names[male_random].rstrip()

    elif gender == 'female':
        female_random = _rand_int(len(female_names) -1 )
        return female_names[female_random].rstrip()

def _last_name():
    global last_names
    last_random = _rand_int(len(last_names) -1 )
    return last_names[last_random].rstrip()

def _details():
    global user_details
    ages = user_details['ages']
    hair_colors = user_details['hair_color']
    eye_colors = user_details['eye_color']

    details = {}
    # Tweak ages to make distribution
    details['eye_color'] = eye_colors[_rand_int(len(eye_colors) -1 )]
    details['hair_color'] = hair_colors[_rand_int(len(hair_colors) -1)]
    chance = random.randint(1, 100)
    if chance >= 98:
        age = 90 + random.randint(0,15) + random.randint(-5,5)
    elif chance >= 85:
        age = 70 + random.randint(0,20) + random.randint(-10,5)
    elif chance >= 60:
        age = 50 + random.randint(0,19) 
    else:
        age = 20 + random.randint(0,30) + random.randint(-2,1)
       
    details['age'] = age 
    return details

def _address():
    global streets
    global terms
    global states

    address = {}
    street = streets[_rand_int(len(streets)-1)].rstrip()
    term = terms[_rand_int(len(terms)-1)].rstrip()
    state = states[_rand_int(len(states)-1)].rstrip()
    zip_code = "{}".format(random.randint(10000, 99999))
    street_num = "{}".format(random.randint(1, 999))

    address['full_address'] = f"{street_num} {street} {term}, {state}, {zip_code}"
    address['street'] = f"{street}"
    address['term'] = f"{term}"
    address['state'] = f"{state}"
    address['zip_code'] = f"{zip_code}"
    address['street_num'] = f"{street_num}"
    return address

def _hobbies(gender):
    global hobbies
    hobbies_no_pref = hobbies['hobbies_no_pref']
    hobbies_female_pref = hobbies['hobbies_female_pref']
    hobbies_male_pref = hobbies['hobbies_male_pref']
    hobbies_obscure = hobbies['hobbies_obscure']
    # Total number of hobbies a user will have
    # All users have one hobby, with a 30% change
    # to have two and an 18% chance to have three
    hobby_list = []
    # base number of hobbies we have
    hobby_num = 1
    # Figure out if we have more hobbies
    for i in range(1,3):
        if random.randint(1,3) == 1:
            hobby_num += 1
    
    # 80% chance to pick non-gendered hobby. 20% percent chance
    # to pick a "gendered" hobby, 20% chance to pick to hobby of the 
    # opposite gender if picking a gendered hobby
    # 10% chance to pick an "obscure" hobby
    for i in range(1,hobby_num + 1):
        if random.randint(1,10) not in [9,10]:
            hobby_list.append(hobbies_no_pref[random.randint(0, len(hobbies_no_pref)-1)])
        else:
            if gender == "male":
                if random.randint(1,10) not in [9,10]:
                    hobby_list.append(hobbies_male_pref[random.randint(0, len(hobbies_male_pref)-1)])
                else:
                    hobby_list.append(hobbies_female_pref[random.randint(0, len(hobbies_female_pref)-1)])
                    
            elif gender == "female":
                if random.randint(1,10) not in [9,10]:
                    hobby_list.append(hobbies_female_pref[random.randint(0, len(hobbies_female_pref)-1)])
                else:
                    hobby_list.append(hobbies_male_pref[random.randint(0, len(hobbies_male_pref)-1)])
    # Obscure hobby, replaces another hobby
    if random.randint(1, 10) == 10:
        random_hobby = hobbies_obscure[random.randint(0, len(hobbies_obscure)-1)]
        hobby_list[random.randint(0, len(hobby_list)-1)] = random_hobby
    
    return hobby_list

def _occupation():
    global occupations
    # 2% chance to be in high income, 20% chance to be in medium income,
    # and 78% chance to be in low income
    base_high_income = 80000
    base_medium_income = 50000
    base_low_income = 30000
    chance = random.randint(1, 100)
    if chance >= 98:
        occupation = occupations['high'][random.randint(0, len(occupations['high'])-1)]
        income = base_high_income + random.randint(1, 90000) + 2000
    elif chance >= 78:
        occupation = occupations['medium'][random.randint(0, len(occupations['medium'])-1)]
        income = base_medium_income + random.randint(1, 40000) + 2000
    else:
        occupation = occupations['low'][random.randint(0, len(occupations['low'])-1)]
        income = base_low_income + random.randint(1, 20000) - 2000
 
    return {
            "income": income,
            "occupation": occupation,
           }
def _rand_int(end_point):
  return random.randint(0, end_point)

for i in range(0, int(arg_num)):
  user_dict = {}
  user_dict['gender'] = _male_female()
  user_dict['first_name'] = _first_name(user_dict['gender'])
  user_dict['last_name'] = _last_name()
  user_dict['details'] = _details()
  user_dict['address'] = _address()
  user_dict['occupation'] = _occupation()
  user_dict['hobbies'] = _hobbies(user_dict['gender'])
  user_dict['index'] = i
  name_json.append(user_dict)

print(json.dumps(name_json,indent=4))
