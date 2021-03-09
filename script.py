import speedtest
import sys
import json
import pathlib
import smtplib
import time
from datetime import datetime

internet_data = {
	"email": "", #Change with your own email address if you want to receive emails
	"hours": 6, #Change if you want a different interval between two different emails
	"last_hours": {
		"date": datetime.today().strftime('%Y-%m-%d'),
		#The download/upload values are in Mbit/s and the ping is measured in ms
		"avg_download": 0.000,
		"avg_upload": 0.000,
		"avg_ping": 0.000,
		"min_download": sys.maxsize,
		"max_download": -sys.maxsize,
		"min_upload": sys.maxsize,
		"max_upload": -sys.maxsize,
		"min_ping": sys.maxsize,
		"max_ping": -sys.maxsize}	
}

last_hours = internet_data["last_hours"]
times_analyzed = 0

def default_today_dict():
	d = {
		"date": datetime.today().strftime('%Y-%m-%d'),
		"avg_download": 0.000,
		"avg_upload": 0.000,
		"avg_ping": 0.000,
		"min_download": sys.maxsize,
		"max_download": -sys.maxsize,
		"min_upload": sys.maxsize,
		"max_upload": -sys.maxsize,
		"min_ping": sys.maxsize,
		"max_ping": -sys.maxsize
	}
	return d


while True:

	#Launch the speedtest
	st = speedtest.Speedtest()
	try:
		st.get_best_server()
	except speedtest.SpeedtestBestServerFailure:
		continue
	download = round(st.download() / 1000000, 3)
	upload = round(st.upload(pre_allocate=False) / 1000000, 3)
	ping = round(st.results.ping, 3)

	#Calculate average/minimum/maximum every cycle (5 minutes)
	last_hours["avg_download"] = round(((last_hours["avg_download"]*times_analyzed)+download)/(times_analyzed+1), 3)
	last_hours["avg_upload"] = round(((last_hours["avg_upload"]*times_analyzed)+upload)/(times_analyzed+1), 3)
	last_hours["avg_ping"] = round(((last_hours["avg_ping"]*times_analyzed)+ping)/(times_analyzed+1), 3)
	last_hours["min_download"] = min(download, last_hours["min_download"])
	last_hours["min_upload"] = min(upload, last_hours["min_upload"])
	last_hours["min_ping"] = min(ping, last_hours["min_ping"])
	last_hours["max_download"] = max(download, last_hours["min_download"])
	last_hours["max_upload"] = max(upload, last_hours["min_upload"])
	last_hours["max_ping"] = max(ping, last_hours["min_ping"])
	times_analyzed += 1

	#Serialization every 3 cycles (15 minutes)
	if times_analyzed==1 or times_analyzed%3==0:
		internet_data["last_hours"] = last_hours
		path = pathlib.Path(str(pathlib.Path.home())+"/.config/connection-analyzer")
		path.mkdir(parents=True, exist_ok=True)
		with open(str(pathlib.Path.home())+"/.config/connection-analyzer/internet_data.json", "w") as outfile:
			json.dump(internet_data, outfile, indent=4)
	
	#Send email every X hours (default 6)
	if times_analyzed % (12*internet_data["hours"]) == 0:
		if internet_data["email"] != "":
			SERVER = "localhost"
			FROM = "connection-analyzer@example.com" #TODO
			TO = [internet_data["email"]]
			SUBJECT = "Your connection data of the last 8 hours"
			TEXT = "This message is sent automatically" #TODO
			message = """\
			From: %s
			To: %s
			Subject: %s

			%s
			""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
			server = smtplib.SMTP(SERVER, 10000)
			server.sendmail(FROM, TO, message)
			server.quit()
			print("Email sent")
		last_hours = default_today_dict()

	print("Going to sleep")

	#Sleep for 5 minutes before doing another test
	time.sleep(270) # 270 intead of 300 because it takes about 30 seconds for the code above
