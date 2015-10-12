# $language = "python"
# $interface = "1.0"
import sys
# host = sys.argv[1]
# port = sys.argv[2]
# user = sys.argv[3]
# passwd = sys.argv[4]
hosts = []

def main():
	for x in hosts:
		host, port, user, passwd = x[1:5]
		cmd = "/SSH2 /P %s /L %s  /PASSWORD %s /C 3DES /M MD5 %s" % (port, user, passwd, host)
		newtab = crt.Session.ConnectInTab(cmd)
		newtab.Caption = host
		if user != 'root':
			newtab.Screen.Send("sudo su\r")
			newtab.Screen.WaitForStrings("password",5)
			newtab.Screen.Send(passwd + '\r')       

main()


