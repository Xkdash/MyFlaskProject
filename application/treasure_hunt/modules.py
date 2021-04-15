######################################################################################################
#                                                                                                    #
#        Do all the imports here                                                                     #
#                                                                                                    #
######################################################################################################

import pymongo
import json






def sanitize(text):
    for i in range(len(text)):
        if "'" in text[i] or '"' in text[i] or ":" in text[i] or "/" in text [i] or "\\" in text[i] or "<" in text[i] or ">" in text[i] or "#" in text[i] or "{" in text[i] or "}" in text[i] or "[" in text[i] or "]" in text[i]:
            return False
    return True






######################################################################################################
#                                                                                                    #
#        Function for Fetching Data from the MongoDb.                                                #
#                                                                                                    #
######################################################################################################


def col_merge(gcol):
    combo={}
    doc = gcol.find({})
    for row in doc:
        gdict=row
        del gdict['_id']
        combo.update(gdict)
    return combo

def col_iter(user_name,gcol):
    doc=gcol.find({})
    for row in doc:
        if user_name in list(row.keys()):
            z=row
            return z[user_name]
    return 0

def fetch(statsdict,regdict,questdict,carddict,flag):
    
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]

    reg_col=treasure_db["reg"]
    regdict=col_merge(reg_col)
    if flag==1:
        return regdict

    stats_col=treasure_db["stats"]
    statsdict=col_merge(stats_col)
    
    if flag==2:
        return statsdict,regdict
    quest_col=treasure_db["quest"]
    questdict=quest_col.find_one()
    del questdict['_id']
    if flag==3:
        return statsdict,regdict,questdict
    card_col=treasure_db["cards"]
    carddict=card_col.find_one()
    del carddict['_id']
    if flag==4:
        return statsdict,regdict,questdict,carddict

######################################################################################################
#                                                                                                    #
#        Function for Authenticating User's Login Credentials.                                       #
#                                                                                                    #
######################################################################################################

def authenticate(user_name,hash_pass,statsdict,regdict):

    if not user_name in statsdict.keys():
        return False

    if not user_name in regdict.keys():
        return False
    if regdict[user_name][3]==False:
        return False
    if regdict[user_name][2]==hash_pass:
        return True
    return False

######################################################################################################
#                                                                                                    #
#        Function for Validating user's registration information.                                    #
#                                                                                                    #
######################################################################################################

def validate(user_name,user_email,user_pass,user_conf):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]

    reg_col=treasure_db["reg"]
    regdict=col_merge(reg_col)
    if user_name in list(regdict.keys()):
        return 0
    if not (len(user_name)<=15 and len(user_name)>=5):
        return 1
    if not (len(user_pass)>=6 and len(user_pass)<=15):
        return 2
    if not user_pass==user_conf:
        return 3
    if not (len(user_email)>=10 and len(user_email)<=40):
        return 4
    return 5


######################################################################################################
#                                                                                                    #
#        Function for updating collections.                                                          #
#                                                                                                    #
######################################################################################################


def stats_update(user_name,statsdict,values):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]
    stats_col=treasure_db["stats"]
    curr_user_stats=col_iter(user_name,stats_col)
    #print(curr_user_stats)
    newvalues={"$set":{user_name:values}}
    update_query={user_name:curr_user_stats}
    stats_col.update_one(update_query,newvalues)
    newstatsdict=col_merge(stats_col)
    return newstatsdict

def reg_update(user_name,regdict,values):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]
    reg_col=treasure_db["reg"]
    curr_user_reg=col_iter(user_name,reg_col)
    #print(curr_user_reg)
    #print(values)
    newvalues={"$set":{user_name:values}}
    update_query={user_name:curr_user_reg}
    reg_col.update_one(update_query,newvalues)
    newregdict=col_merge(reg_col)
    return newregdict


######################################################################################################
#                                                                                                    #
#        Function for adding collections.                                                            #
#                                                                                                    #
######################################################################################################



def reg_add(user_name,values):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]
    reg_col=treasure_db["reg"]
    reg_col.insert_one({user_name:values})
    newregdict=col_merge(reg_col)
    return newregdict

def stats_add(user_name,values):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]
    stats_col=treasure_db["stats"]
    stats_col.insert_one({user_name:values})
    newstatsdict=col_merge(stats_col)
    return newstatsdict



######################################################################################################
#                                                                                                    #
#        Function for generating the leaderboard.                                                    #
#                                                                                                    #
######################################################################################################

def gen_leaderboard(user_name):
    huntclient = pymongo.MongoClient("mongodb://localhost:27017/")
    treasure_db=huntclient["hunt"]
    stats_col=treasure_db["stats"]
    statsdict=col_merge(stats_col)
    user_list=list(statsdict.keys())
    score_dict={}
    maxlen=0
    for i in range(len(user_list)):
        score_dict[user_list[i]]=statsdict[user_list[i]][1]
        if maxlen<len(user_list[i]):
            maxlen=len(user_list[i])

    lboard={user_name: score for user_name, score in sorted(score_dict.items(), reverse=True, key=lambda item:item[1])}
    sorted_list=list(lboard.keys())
    lstring="Your Score: "+str(score_dict[user_name])+"\n Your Rank: "+str(sorted_list.index(user_name)+1)+"\n\nRank \t\t\t Username \t\t\t\t Score"
    
    for i in range(min(len(sorted_list),10)):
        currlen=len(sorted_list[i])
        lstring+="\n"+str(i+1)+"\t\t\t\t "+sorted_list[i].strip()+" "*(maxlen-currlen+6)+"\t\t\t"+str(lboard[sorted_list[i]])
    return lstring

