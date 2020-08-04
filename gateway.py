from requests import Session
from subprocess import Popen, PIPE
from lxml import html, etree
import json

class Gateway():

	def __init__(self):
		self.s = Session()
		self.login_page = "http://192.168.254.254/api/system/user_login"
		self.host_info = "http://192.168.254.254/api/system/HostInfo"
		self.dns_settings = "http://192.168.254.254/api/ntwk/lan_server"
		self.wizard = "http://192.168.254.254/html/wizard/wizard.html"
		self.reboot = "http://192.168.254.254/api/service/reboot.cgi"
		self.portmapping = "http://192.168.254.254/api/ntwk/portmapping"

		self.login()

	def getRequestCredentials(self,link):

		resp = self.s.get(link)

		param, token = self.getPageKeys(resp.text)

		self.param = param
		self.token = token

	def postRequestCredentials(self,link,data):

		resp = self.s.post(link, data=data)

		param, token = self.getPageKeys(resp.text)

		self.param = param
		self.token = token

	def getToken(self,param, token):
		resp = Popen(["node", "login", param, token], stdout=PIPE)
		token = resp.communicate()[0].decode().strip()

		return token

	def changeToken(self,msg):
		pass

	def getPageKeys(self, text):
		tree = html.fromstring(text)

		param = ""
		token = ""

		for i in tree.xpath("head/meta"):

			if i.get("name") == "csrf_param":
				param = i.get("content")
			elif i.get("name") == "csrf_token":
				token = i.get("content")

		return (param, token)

	def login(self):
		#Get initial key pair

		self.getRequestCredentials("http://192.168.254.254")

		pass_token = self.getToken(self.param, self.token)

		data = {"csrf":{"csrf_param": self.param, "csrf_token": self.token},"data":{"UserName": "user", "Password": pass_token}}

		self.s.post(self.login_page, data=json.dumps(data))

		# Get the csrf keys from the wizard page

		self.getRequestCredentials(self.wizard)

	def cleanUpResponse(self,text):
		return text.lstrip("while(1); /*").rstrip("*/")

	def getHostInfo(self):

		resp = self.s.get(self.host_info).text

		resp_text = self.cleanUpResponse(resp)

		resp_text_json = json.loads(resp_text)

		print("Name\t\t\tIP Address")
		print("*"*50)
		for i in resp_text_json:
			if i["Active"] == True:
				print(+i["HostName"]+"\n\n\t - "+i["IPAddress"]+"\n")

	def rebootGateway(self):
		csrf = {"csrf":{"csrf_param": self.param, "csrf_token": self.token}}

		csrf_data = json.dumps(csrf)

		resp = self.s.get(self.reboot, data=csrf_data)

		print(resp.text)

	def changeDNSSetting(self,dnsPrimaryIP):
		data = {"csrf":
		{"csrf_param":self.param,"csrf_token":self.token},
		"data":{
		"PassthroughMACAddress":"",
		"MinIP":"192.168.254.1",
		"UseAllocatedWAN":"Normal",
		"dnsmode":"false",
		"DNSServerone":dnsPrimaryIP,
		"PassthroughLease":60,
		"ServerEnable":True,
		"DHCPLeaseTime":86400,
		"ID":"InternetGatewayDevice.LANDevice.1.LANHostConfigManagement.",
		"AssociatedConnection":"",
		"DNSServertwo":"192.168.254.254",
		"MaxIP":"192.168.254.100",
		"isInstance":True,
		"isDestroyed":False,
		"isDestroying":False,
		"isObserverable":True}}

		self.postRequestCredentials(self.dns_settings, json.dumps(data))

		print("Changed to: " + dnsPrimaryIP)

	def getPortmapping(self):
		response = self.s.get(self.portmapping)

		mapping_contents = json.loads(self.cleanUpResponse(response.text))

		print("Name\t\t\tApplication ID")
		print("*"*50)

		for p in mapping_contents:
			print(p["Name"])
			print("\n\t- " + p["ApplicationID"]+"\n")