######################################################################################################
#                                                                                                    #
#        Perform all the imports here                                                                #
#                                                                                                    #
######################################################################################################

from flask import Flask,Blueprint,redirect,url_for,render_template,request,session,current_app
import application.treasure_hunt.modules as modules
import json
import hashlib

regdict={}
statsdict={}
questdict={}
carddict={}
color_list=['cyan','orange','green','red']
quest_status=['Start','Resume','Completed','Locked']
######################################################################################################
#                                                                                                    #
#        Register BluePrint for the hunt app                                                         #
#                                                                                                    #
######################################################################################################


hunt_bp=Blueprint('hunt_bp',__name__,template_folder="templates",static_folder="static")

######################################################################################################
#                                                                                                    #
#        Redirect to the Island Page.                                                                #
#                                                                                                    #
######################################################################################################

@hunt_bp.route("/",methods=['GET','POST'])
def red():
    return redirect(url_for('hunt_bp.island'))

######################################################################################################
#                                                                                                    #
#        Function for Creating Email Verification Module after Registration.                         #
#                                                                                                    #
######################################################################################################

@hunt_bp.route("/<user_name>/verify",methods=['GET','POST'])
def verify(user_name):
    if request.method=="POST":
        if request.form.get("verify_btn","")=="verify_req":
            if modules.sanitize([user_name])==False:
                return render_template("verify.html",user_name=user_name)
            global statsdict,regdict,questdict,carddict
            regdict=modules.fetch(statsdict,regdict,questdict,carddict,1)
            reg_user=regdict[user_name]
            reg_user[3]=True; #verified
            firststats=[user_name,0,0,{"hands_on":[0,0],"the_order":[3,0],"the_raid":[3,0],"track_part":[3,0]}] #[username,score,bonus,{"mission":[open_status,number of attempts]}
            statsdict=modules.stats_add(user_name,firststats)
            regdict=modules.reg_update(user_name,regdict,reg_user)
            return redirect(url_for('hunt_bp.island'))
    return render_template("verify.html",user_name=user_name)


######################################################################################################
#                                                                                                    #
#        Function for Creating the User Registration Portal.                                         #
#                                                                                                    #
######################################################################################################

@hunt_bp.route("/registration",methods=['GET','POST'])
def register():
    if request.method=="GET":
        return render_template("registration.html")
    else:
        if request.form.get("reg_btn","").strip()=="reg_request":
            user_name=request.form.get("reg_user","").strip()
            user_email=request.form.get("reg_email","").strip()
            user_pass=request.form.get("reg_pass","").strip()
            user_conf=request.form.get("reg_pass_conf","").strip()
            is_safe=modules.sanitize([user_name,user_email,user_pass,user_conf])    #sanitization
            if is_safe==False:
                return render_template("registration.html")
            val = modules.validate(user_name,user_email,user_pass,user_conf)
            if val==5:
                global regdict
                hash_pass=hashlib.md5(user_pass.encode('utf-8')).hexdigest()
                reg_user=[user_name,user_email,hash_pass,False]
                regdict=modules.reg_add(user_name,reg_user)
                return redirect(url_for('hunt_bp.verify',user_name=user_name))
            else:
                return render_template("registration.html")
        return render_template("registration.html")



######################################################################################################
#                                                                                                    #
#        Function for Creating the Treasure Island Portal                                            #
#                                                                                                    #
######################################################################################################


@hunt_bp.route("/island",methods=['GET','POST'])
def island():
    global statsdict,regdict,questdict
    statsdict,regdict=modules.fetch(statsdict,regdict,questdict,carddict,2)
    if request.method=="GET":
        return render_template('island.html')
    else:
        if request.form.get("signup_btn","")=="signup_req":
            return redirect(url_for('hunt_bp.register'))
        if request.form.get("login_btn","")=="login_req":
            user_name=request.form.get("in_user","").strip()
            user_pass=request.form.get("in_pass","").strip()

            if user_name=="" or user_pass=="" or modules.sanitize([user_name,user_pass])==False:    #sanitization
                return render_template('island.html',err_msg="Wrong User Id or password.")
            hash_pass=hashlib.md5(user_pass.encode('utf-8')).hexdigest() 
            auth=modules.authenticate(user_name,hash_pass,statsdict,regdict)
            if auth==True:
                session[user_name]=user_name
                return redirect(url_for('hunt_bp.home',user_name=user_name))
            else:
                return render_template('island.html',err_msg="Wrong User Id or password.")
        return render_template('island.html')


######################################################################################################
#                                                                                                    #
#        Function for Creating the Quest Content.                                                    #
#                                                                                                    #
######################################################################################################


@hunt_bp.route("<user_name>/quest/<quest_name>",methods=['GET','POST'])
def quest(user_name,quest_name):
    if not session.get(user_name):
        return redirect(url_for('hunt_bp.island'))

    if session[user_name]=="":
        return redirect(url_for('hunt_bp.island'))

    global statsdict,regdict,questdict
    statsdict,regdict,questdict=modules.fetch(statsdict,regdict,questdict,carddict,3)
    userqdict=statsdict[user_name][3]   #user's stats of each quest
    qdict=questdict[quest_name]
    if userqdict[quest_name][0]<2 : #quest not completed yet
        open_flag=True
    else:
        open_flag=False
        return redirect('/treasure_hunt/'+user_name+'/pirate_cove')
    carddict[questdict[quest_name][4]][1]
    leaderboard=modules.gen_leaderboard(user_name)
    if request.method=="GET":
        if userqdict[quest_name][0]==0:    #not started yet
            userqdict[quest_name][0]=1     #start
            statsdict=modules.stats_update(user_name,statsdict,statsdict[user_name])
        return render_template('quest.html',user_name=user_name,quest_name=quest_name,quest_title=carddict[questdict[quest_name][4]][1],quest_text=qdict[0],quest_image=qdict[1],open_flag=open_flag,leaderboard=leaderboard)
    else:   #post request
        if open_flag==False:
            return redirect('/treasure_hunt/'+user_name+'/pirate_cove')
        if request.form.get("logout_btn","")=="logout":
            session[user_name]=""
            return redirect(url_for('hunt_bp.island'))
        
        if request.form.get("home_btn","")=="home":
            return redirect('/treasure_hunt/'+user_name+'/pirate_cove')
        
        if request.form.get("submit_btn","")=="submit_req":
            answer=request.form.get("answer_text").strip()
            if answer=="" or modules.sanitize([answer])==False: #sanitization
                return render_template('quest.html',user_name=user_name,quest_name=quest_name,quest_title=carddict[questdict[quest_name][4]][1],quest_text=qdict[0],quest_image=qdict[1],open_flag=open_flag,leaderboard=leaderboard)

            result=(qdict[2]==answer)

            userqdict[quest_name][1]+=1
 
            if result==True:
                open_flag=False
                userqdict[quest_name][0]=2  #completed
                keys = list(userqdict.keys())   #list of quest_names
                ind=keys.index(quest_name)  #index of the current quest
                if ind<=len(userqdict)-2:
                    userqdict[keys[ind+1]][0]=0
                
                newstat=statsdict[user_name]
 
                newstat[1]+=questdict[quest_name][3]	#score increment

                statsdict=modules.stats_update(user_name,statsdict,newstat)
                
                return redirect('/treasure_hunt/'+user_name+'/pirate_cove')
            else:
                newstat=statsdict[user_name]
                statsdict=modules.stats_update(user_name,statsdict,newstat)
        return render_template('quest.html',user_name=user_name,quest_name=quest_name,quest_title=carddict[questdict[quest_name][4]][1],quest_text=qdict[0],quest_image=qdict[1],open_flag=open_flag)



######################################################################################################
#                                                                                                    #
#        Function for Creating the User's Home.                                                		 #
#                                                                                                    #
######################################################################################################


@hunt_bp.route("/<user_name>/pirate_cove",methods=['GET','POST'])
def home(user_name=""):
    user_name=user_name.strip()

    if not session.get(user_name):
        return redirect(url_for('hunt_bp.island'))

    if session[user_name]=="":
        return redirect(url_for('hunt_bp.island'))
    clist=[]
    q_stat=[]
    q_value=[]
    
    c_over=[]
    c_title=[]
    q_sum=[]
    summary=[]
    leaderboard=modules.gen_leaderboard(user_name)
    
    global statsdict,regdict,questdict,carddict
    statsdict,regdict,questdict,carddict=modules.fetch(statsdict,regdict,questdict,carddict,4)
    userqdict=statsdict[user_name][3]
    for i in range(len(userqdict)):
        clist.append(color_list[list(userqdict.values())[i][0]])
        q_stat.append(quest_status[list(userqdict.values())[i][0]])
        q_value.append("quest_id_"+str(i+1))
        c_title.append(carddict[q_value[i]][1])
        c_over.append(carddict[q_value[i]][2])
        q_sum.append(carddict[q_value[i]][3])
        summary.append(carddict[q_value[i]][4])
    if request.method=="GET":
        return render_template('home.html',uname=user_name,clist=clist,quest_status=q_stat,quest_value=q_value,quest_title=c_title,quest_overview=c_over,quest_sum=q_sum,summary=summary,leaderboard=leaderboard)
    else:
        if request.form.get("logout_btn","")=="logout":
            session[user_name]=""
            return redirect(url_for('hunt_bp.island'))
        for i in range(len(q_value)):
            if request.form.get(q_value[i],"")==q_value[i]:
                quest_name=carddict[q_value[i]][0]
        if statsdict[user_name][3][quest_name][0]>=2:
            return render_template('home.html',uname=user_name,clist=clist,quest_status=q_stat,quest_value=q_value,quest_title=c_title,quest_overview=c_over,quest_sum=q_sum,summary=summary,leaderboard=leaderboard)
        else:
            return redirect(url_for('hunt_bp.quest',quest_name=quest_name,user_name=user_name))
    return render_template('home.html',uname=user_name,clist=clist,quest_status=q_stat,quest_value=q_value,quest_title=c_title,quest_overview=c_over,quest_sum=q_sum,summary=summary,leaderboard=leaderboard)
