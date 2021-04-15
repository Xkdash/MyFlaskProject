from flask import redirect, url_for, render_template,Blueprint,request
from virus_total_apis import PublicApi as VirusTotalPublicApi
import validators
import string

hash_size=[32,48,64,128]

vt_bp=Blueprint('vt_bp',__name__,template_folder='templates',static_folder='static')

def vt_init():
	fin=open("application/vt_lookup/API_key.txt","r")
	code = fin.readline().strip();
	vtoken = VirusTotalPublicApi(code)
	fin.close()
	return vtoken
def parse_results(scan_results):
	combined_result=""
	if scan_results['response_code']<300:	#received
		results=scan_results['results']
		if results['response_code']==0:
			return "No Result","blue",0
		positives=results['positives']
		if int(positives)==0:
			return "Clean","green",0
		scanners=results['scans']
		scanner_list=list(scanners.keys())
		for i in range(len(scanner_list)):
			scanner_verdict=scanners[scanner_list[i]]
			if scanner_verdict['detected']==True:
				print(scanner_verdict['result'])
				combined_result+=scanner_verdict['result']+" as per "+scanner_list[i]+".\n"
		return combined_result,"red",positives
	else:
		return "Not Found","blue",0
def url_lookup(url):
	vtoken = vt_init()
	scan=vtoken.scan_url(url)	#send the url for scanning
	scan_results=vtoken.get_url_report(url)	#fetch the results
	return parse_results(scan_results)

def hash_lookup(fhash):	#Check if the hash exists on the VT server
	vtoken=vt_init()
	combined_result=""
	scan_results = vtoken.get_file_report(fhash)
	return parse_results(scan_results)

@vt_bp.route('/lookup', methods=['GET','POST'])
def index():
	val_type=""
	if request.method=="GET":
		return render_template('vt_lookup.html',val_type="Output")
	else:
		if request.form.get('home_key',"")=="home_value":
			return redirect(url_for('home_bp.home_index'))
		input_val=request.form.get('input_type',"").strip()
		if input_val=="":
			return render_template('vt_lookup.html',val_type="Output",input_val="",val_col="navy")
		if validators.url(input_val) or validators.url("http://"+input_val) or validators.url("https://"+input_val)==True:		#URL
			results,val_col,positives=url_lookup(input_val)
			val_type="URL"
		elif len(input_val) in hash_size and set(input_val).issubset(string.hexdigits): #FILE
			results,val_col,positives=hash_lookup(input_val)
			val_type="FILE"
		else:
			return render_template('vt_lookup.html',val_type="Output",out="Not a Valid URL or Hash.",input_val=input_val,val_col="navy")
		return render_template('vt_lookup.html',out=results,val_type="@"+val_type+"("+str(positives)+")",input_val=input_val,val_col=val_col)
	return render_template('vt_lookup.html',out=results,val_type="Output",input_val="",val_col="navy")
