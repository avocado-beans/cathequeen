import os
import random
directory = 'static/people/'
 
 
def pick_random_girl():
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_list.append(f)
    
    girl = random.choice(file_list)
    picture_list = []
    for filename in os.listdir(girl):
        f = os.path.join(girl, filename)
        picture_list.append(f)
    return random.choice(picture_list)
    
def sorted_list():
    leaderboard = open('ratings.txt', 'r')
    ratings = leaderboard.readlines()[0].split("|")
    
    rating_list = []
    for rating in ratings:
        try:
            rating_list.append(rating.split(":")[1])
        except:
            pass
    
    rating_list.sort(reverse=True)
    sorted_names = []
    pictures = []
    last_rating = ""
    for rate in rating_list:
        for rating in ratings:
            if rating.split(":")[1] == rate and not rating.split(":")[0] in sorted_names:
                sorted_names.append(rating.split(":")[0])
                pictures.append(pick_random_photo(f"static/people/{rating.split(':')[0]}"))
                break
        
    return(sorted_names, rating_list, pictures)
    
def pick_random_photo(url):
    picture_list = []
    for filename in os.listdir(url):
        f = os.path.join(url, filename)
        picture_list.append(f)
    return random.choice(picture_list)
    
def reset_ratings():
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_list.append(f)

    leaderboard = open('ratings.txt', 'w')
    for girl in file_list:
        girl = girl.split('people/')[1]
        leaderboard.write(f'{girl}:1400|')
    leaderboard.close()
    
reset_ratings()
def update_rating(girl_rating):
    leaderboard = open('ratings.txt', 'r')
    ratings = leaderboard.readlines()[0].split("|")
    mega_string = ""
    for rating in ratings:
        if rating.split(":")[0] == girl_rating.split(":")[0]:
            mega_string += girl_rating + "|"
        else:
            mega_string += rating + "|"
    leaderboard.close()
    leaderboard = open('ratings.txt', 'w')
    leaderboard.write(mega_string)
    leaderboard.close()
    
def update_ratings_P(girl1_url, girl2_url, Winner, K):
    girl1_name = girl1_url.split('/')[2]
    girl1_score = rating(girl1_name)
    girl2_name = girl2_url.split('/')[2]
    girl2_score = rating(girl2_name)
    
    girl1_Pscore, girl2_Pscore = update_ratings(girl1_score, girl2_score, Winner, K)
    girl1_tag = girl1_name+":"+str(girl1_Pscore)
    girl2_tag = girl2_name+":"+str(girl2_Pscore)
    
    update_rating(girl1_tag)
    update_rating(girl2_tag)
    
def rating(girl):
    leaderboard = open('ratings.txt', 'r')
    ratings = leaderboard.readlines()[0].split("|")
    for rating in ratings:
        if rating.split(":")[0] == girl.split(":")[0]:
            return float(rating.split(":")[1])
    return 
    
def update_ratings(Ra, Rb, Winner, K):
    Ea = 1/(1 + 10**((Rb-Ra) / 400))
    Eb = 1/(1 + 10**((Ra-Rb) / 400))
    
    if Winner == 1:
        Ra = Ra + K * (1 - Ea)
        Rb = Rb + K * (0 - Eb)
    if Winner == 2:
        Ra = Ra + K * (0 - Ea)
        Rb = Rb + K * (1 - Eb)
    return Ra, Rb
    
