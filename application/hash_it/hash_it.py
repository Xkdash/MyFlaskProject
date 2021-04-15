#import self
import hashlib
from flask import Blueprint,render_template,request,redirect,url_for

#self blueprinting

hashit_bp=Blueprint('hashit_bp', __name__,template_folder='templates',static_folder='static')

#self routing
@hashit_bp.route("/hashit",methods=['GET', 'POST'])
def compute_hash():
    if request.method=="POST":
        if request.form.get('home_key','')=="home_key":
            return redirect(url_for('home_bp.home_index'))
        p=request.form.get('plaintext','').strip()
        if p=="":
            return render_template("hashit.html",plaintext="",md5="",sha1="",sha256="",sha512="")
        plaintext=p
        md5=str(hashlib.md5(p.encode('utf-8')).hexdigest())
        sha1=str(hashlib.sha1(p.encode('utf-8')).hexdigest())
        sha256=str(hashlib.sha256(p.encode('utf-8')).hexdigest())
        sha512=str(hashlib.sha512(p.encode('utf-8')).hexdigest())
        return render_template("hashit.html",plaintext=plaintext,md5=md5,sha1=sha1,sha256=sha256,sha512=sha512)
    else:
        return render_template("hashit.html")
