import requests
from datetime import datetime
import smtplib
import sys
import getpass

resources = ["/<xyz>.html"]

sites = {
        "https://jsdbv.com":"",
        "https://sadnvl.com":"",
        "http://dvbk.com":resources
		}


def check_internet_connection():
	response = requests.get("https://google.com")
	if response.status_code == 200:
		return 1
	else: return 0


def checker(site_name):
	response = {}
	try:
		request_response = requests.get(site_name)
		time = datetime.now()
		status = request_response.status_code
		msg = "\n{1} The status for site {0} is {2}" .format(site_name, time, status)
		response[site_name] = (status,msg)
		return response
	except requests.exceptions.ConnectionError as e:
		print ("Check the wed address!")
		response[site_name] = "400"
		return response


def log(text):
	file_name = "/home/richie/.siteupchecker.txt"
	with open(file_name, "a") as f:
		f.write(text)
	f.close()


def send_email(msg):
    from_add = "a@gmail.com"
    to_add = "b@gmail.com"
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    try:
        password = getpass.getpass("Enter password for {} ".format(from_add))
        server.login(from_add, password)
    except smtplib.SMTPAuthenticationError as e:
        print ("GOOGLE login authentication error!!\n")
        sys.exit(e)
    
    server.sendmail(from_add, to_add, msg)
    server.quit()
    
	
def main():
	msg_list = []
	if check_internet_connection():
		for site,resource in sites.items():
			if resource:
				for r in resource:
					result = checker(site+r)
					if result[site+r][0] != 200:
						msg_list.append(result[site][1])
			else:
				result = checker(site)
				if result[site][0] != 200:
					msg_list.append(result[site][1])

		if msg_list:
			final_message = "".join(msg for msg in msg_list)
			log(final_message)
			print ("Sending Email notification!")
			send_email(final_message)
			print ("Email Sent.")
		else:
			print ("All sites up!\nNo logs were made.")
		

if __name__ == "__main__":
    main()
