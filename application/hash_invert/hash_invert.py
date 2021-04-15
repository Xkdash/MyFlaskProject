from flask import redirect, url_for, render_template,Blueprint,request
import random
import base64
import requests

size={"md5":32,"sha1":40,"sha256":64,"sha384":96,"sha512":128,"ntlm":32}

invert_bp=Blueprint('invert_bp',__name__,template_folder='templates',static_folder='static')

def invertHash(hash_val,hash_type):
	fin=open("application/hash_invert/creds.txt")
	creds=fin.readline().strip().split(",")
	email=creds[0]
	code=creds[1]
	fin.close()
	response=requests.get('https://md5decrypt.net/en/Api/api.php?hash='+hash_val+"&hash_type="+hash_type+"&email="+email+"&code="+code)
	if response.status_code==200:
	    return response.text

@invert_bp.route('/invert', methods=['GET','POST'])
def index():
	if request.method=="GET":
		return render_template('invert.html',hash_type="@md5")
	else:
		if request.form.get('home_key',"")=="home_value":
			return redirect(url_for('home_bp.home_index'))
		input_hash=request.form.get('invert',"").strip()
		hash_type=request.form.get('algo',"").strip()
		if hash_type=="" or input_hash=="" or size.get(hash_type)==None:
			return render_template('invert.html',hash_type="@md5")
		l=len(input_hash)
		if not l==size[hash_type]:
			if l in size.values():
				temp=list(size.keys())[list(size.values()).index(l)]
				return render_template('invert.html',out="The entered hash is of type "+temp,hash_type="@suggest",input_hash=input_hash,c_type="navy")
			return render_template('invert.html',out="The entered hash is incorrect.",hash_type="@error",input_hash=input_hash,c_type="red")
		inverted=invertHash(input_hash,hash_type).strip()
		if inverted=="":
			return render_template('invert.html',out="Not Found in the Database!",hash_type="@failure",input_hash=input_hash,c_type="orange")
		return render_template('invert.html',out=inverted,hash_type="@"+hash_type,input_hash=input_hash,c_type="green")
