"""
Logging in basically means getting the custom_sessionid and VIN, which are used to make 
every subsequent request.
"""

from Crypto.Cipher import Blowfish
import requests
import base64

def login(username, password, region_code='NE', initial_app_strings='geORNtsZe5I4lRGjG9GZiA'):
	baseprm = 'uyI5Dj9g8VCOFDnBRUbr3g'
	c1  = Blowfish.new(baseprm, Blowfish.MODE_ECB)
	packingLength = 8 - len(password) % 8
	packedPassword = password + chr(packingLength) * packingLength
	encryptedPassword = c1.encrypt(packedPassword)
	encodedPassword = base64.standard_b64encode(encryptedPassword)

	url = "https://gdcportalgw.its-mo.com/api_v180117_NE/gdc/UserLoginRequest.php"
	data = {
		"RegionCode": region_code,
		"UserId": username,
		"initial_app_strings": initial_app_strings,
		"Password": encodedPassword,
	}
	headers = {'User-Agent': 'Mozilla/5.0'}

	r = requests.post(url,data=data, headers=headers)
	r.raise_for_status()
	if not r.json()['status'] == 200:
		raise Exception('Cannot login.  Probably username & password are wrong. ' + r.text)

	custom_sessionid = r.json()['VehicleInfoList']['vehicleInfo'][0]['custom_sessionid']
	VIN = r.json()['CustomerInfo']['VehicleInfo']['VIN']

	return custom_sessionid, VIN
