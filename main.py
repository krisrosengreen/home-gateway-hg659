import gateway as g
import sys

a = sys.argv
gw = g.Gateway()

options = {"-d": gw.changeDNSSetting, "-h": gw.getHostInfo, "-p": gw.getPortmapping}

if (a[1] in options):
	if len(a)==2:
		options[a[1]]()
	elif len(a)==3:
		options[a[1]](a[2])
else:
	print("Not an option!")