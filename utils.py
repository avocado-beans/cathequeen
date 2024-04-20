import os
import random
import time
import requests
import pymysql
directory = 'static/girls100/'

heart = ['face1974.jpg']
def pick_random_girl(girllist=[], girl2url=None, time_since=0, exclude=[], timer=3600):
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_list.append(f)
    for girl in girllist:
        if girl in file_list:
            file_list.remove(girl)
    for girl in heart:
        if girl in file_list:
            file_list.remove(girl)
    
    clock = time.time()-time_since 
    if clock < 3600:
        print(time.time()-time_since, exclude)
        for girl in exclude:
            if girl in file_list:
                file_list.remove(girl)
    if clock >= 3600:
        clock = -1
    if girl2url in file_list:
        file_list.remove(girl2url)
        
    print(len(file_list),"girls left")
    if len(file_list) < 130:
        print('RAN OUT OF GIRLS')
        return 'FINISHED', clock
        
    else:
        return random.choice(file_list), clock
    
def sorted_list():
    leaderboard = open('ratings.txt', 'r')
    ratings = leaderboard.readlines()[0].split("|")
    
    rating_list = []
    for rating in ratings:
        try:
            if rating.split(":")[1] != '1400':
                if not rating.split(":")[0] in heart:
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
                if not rating.split(":")[0] in heart:
                    sorted_names.append(rating.split(":")[0])
                    pictures.append(f"static/girls100/{rating.split(':')[0]}")
                break
                
    return(sorted_names, rating_list, pictures)
    
    
def reset_ratings():
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        file_list.append(f)

    leaderboard = open('ratings.txt', 'w')
    for girl in file_list:
        girl = girl.split('girls100/')[1]
        leaderboard.write(f'{girl}:1400|')
    leaderboard.close()
    
def update_rating(girl_rating):
    leaderboard = open('ratings.txt', 'r')
    ratings = leaderboard.readlines()[0].split("|")
    mega_string = ""
    for rating in ratings:
        if rating.split(":")[0] == girl_rating.split(":")[0]:
            mega_string += girl_rating + "|"
        else:
            mega_string += rating + "|"
    
    mega_string = mega_string.split('||')[0]
    leaderboard.close()
    leaderboard = open('ratings.txt', 'w')
    leaderboard.write(mega_string)
    leaderboard.close()
    
def update_ratings_P(girl1_url, girl2_url, Winner, K):
    print("LINKS:", girl1_url, girl2_url)
    girl1_name = girl1_url.split('/')[2]
    girl1_score = rating(girl1_name)
    girl2_name = girl2_url.split('/')[2]
    girl2_score = rating(girl2_name)
    
    try:
        girl1_Pscore, girl2_Pscore = update_ratings(girl1_score, girl2_score, Winner, K)
        girl1_tag = girl1_name+":"+str(girl1_Pscore)
        girl2_tag = girl2_name+":"+str(girl2_Pscore)
    
        update_rating(girl1_tag)
        update_rating(girl2_tag)
    except:
        print("FAILED AT", girl1_url, girl2_url)
    
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
    
def parse(conn):
    try:
        conn.ping() 
        with conn.cursor() as cursor:
            sql = "SELECT * FROM `girls`"
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                return (row['data'])
    except:
        pass

def update(new_data, conn):
    try:
        conn.ping() 
        with conn.cursor() as cursor:
            sql = "DELETE FROM `girls`"
            cursor.execute(sql)            
            sql = "INSERT INTO `girls` (`data`) VALUES (%s)"
            cursor.execute(sql, (new_data))
        conn.commit()
        print("Record updated successfully")
    except:
        pass

def check_if_empty(conn):
    if len(sorted_list()[0]) == 0:
        previous_ratings = parse(conn)
        file = open('ratings.txt','w')
        file.writelines(previous_ratings)
        file.close()

def save_to_cloud(start_at, conn):
    if time.time()-start_at >= 60:
        print("STARTING RESET")
        file = open('ratings.txt','r')
        old_data = parse(conn)
        new_data = file.readlines()
        update(new_data, conn)
        file.close()
        print("ENDED RESET")
        if time.time()-start_at >= 840:
            conn.close()
            conn = pymysql.connect(
                host='sql11.freesqldatabase.com',
                user='sql11700114',
                password='cAe4eMACLu',
                db='sql11700114',
                cursorclass=pymysql.cursors.DictCursor
            )
        
        return 'RESET', conn
    return 'HOLD', conn
