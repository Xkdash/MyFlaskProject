from flask import redirect, url_for, render_template,Blueprint,request
import random
import base64
otp_bp=Blueprint('otp_bp',__name__,template_folder='templates',static_folder='static')

@otp_bp.route('/otp', methods=['GET','POST'])
def otpGen():
	if request.method=="GET":
		return render_template('otp.html',otp_length=50,otp_val="Press Generate !!")
	else:
		if request.form.get('home_key',"")=="home_value":
			return redirect(url_for('home_bp.home_index'))
		req=request.form.get('length_input',"").strip()

		if req=="":
			return render_template('otp.html')
		else:
			if req.isnumeric():
				out=""
				encoding_type=""
				l=int(req)
				ran=random.getrandbits(4*l)
				if request.form.get('encoding',"")=="deci":
					out=str(int(hex(ran),16))[:l]
					encoding_type="Decimal"
				elif request.form.get('encoding',"")=="hexa":
					out=hex(ran)[2:]
					encoding_type="Hex"
				elif request.form.get('encoding',"")=="b64":
					encoding_type="Base64"
					out=base64.b64encode(str(ran).encode()).decode()[:l]
				return render_template('otp.html',otp_length=req,otp_val=out,encoding_type=encoding_type)
			else:
				return render_template('otp.html')
