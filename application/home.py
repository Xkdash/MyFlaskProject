#import self
from flask import Flask,render_template,url_for,request,Blueprint,redirect

#import other apps
from application.hash_it import hash_it
from application.otp import otp_gen
from application.hash_invert import hash_invert
from application.vt_lookup import vt_lookup
from application.treasure_hunt import hunt

#self blueprinting
home_bp=Blueprint('home_bp', __name__,template_folder='templates',static_folder='static')    

#blueprint others
hashit_bp=hash_it.hashit_bp
otp_bp=otp_gen.otp_bp
invert_bp=hash_invert.invert_bp
vt_bp=vt_lookup.vt_bp
hunt_bp=hunt.hunt_bp
#other routing
@hashit_bp.route("/hashit",methods=['GET', 'POST'])
def hashit():
    return redirect(url_for('hashit_bp.hashit'))

@otp_bp.route("/otp",methods=['GET', 'POST'])
def genOTP():
    return redirect(url_for('otp_bp.otpGen'))

@invert_bp.route("/invert",methods=['GET', 'POST'])
def invert(): 
    return redirect(url_for('invert_bp.index'))

@vt_bp.route("/vtlookup",methods=['GET', 'POST'])
def vtlookup(): 
    return redirect(url_for('vt_bp.index'))

@hunt_bp.route("/treasure/island",methods=['GET', 'POST'])
def treasure(): 
    return redirect(url_for('hunt_bp.island'))

#self routing
@home_bp.route("/",methods=['GET', 'POST'])
@home_bp.route("/index",methods=['GET', 'POST'])

def home_index():
    if request.method=="GET":
        return render_template("index.html")
    else:
        if request.form.get('hash_btn','')=="hash_value":
            return hashit()
        elif request.form.get('otp_btn','')=="otp_value":
            return genOTP()
        elif request.form.get('invert_btn','')=="invert_value":
            return invert()
        elif request.form.get('vt_btn','')=="vt_value":
            return vtlookup()
        elif request.form.get('treasure_btn','')=="treasure_value":
            return treasure()
    return render_template("index.html")

