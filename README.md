# Connection Analyzer

:stopwatch: :stopwatch: :stopwatch: 

Connection analyzer is a utility tool to monitor your internet connection. It's a simple Python script that does a speedtest every 8 hours and sends you an email with the latest values.

***Emails are temporary disabled***


# Installation

To use the script you have to download it (and its dependencies) and give it permissions to execute.
```
$ pip install speedtest-cli
$ git clone https://github.com/0xfederama/connection-analyzer.git
$ cd connection-analyzer
$ chmod +x script.py
```
Now you can launch the script with `python3 script.py`.

If you want to execute the script every time you turn on your computer (or your raspberrypi) you have to add `python3 /absolute/path/to/script.py &` at the end of the file `/etc/rc.local`, just before the line that has `exit 0`, and reboot.

# Customization

You can customize the script as you want.
The first thing that you can customize is the email (line 4-5): if you don't want to receive an email leave the field as it is, otherwise write your own email and password. If you don't want to receive emails, **only** change this field.

You can customize also the value of the hours (line 6). With a default value of 6, you will receive an email every 6 hours. After 8 hours, the dictionary will be reset to default values, in order to check if, in a 6-hour span, the connection has had problems (otherwise, the average in a long span of hours will flatten the curve).

Since the json file is never read by the program, if you change the values of the json it doesn't affect the program.

# How to check internet speed values

When you want to check the latest values of your internet speed, you can view the json file stored in `~/.config/connection-analyzer`. That file will be overwritten the next time that your internet speed is tested (in 15 minutes). 

If you want to save a file, you can just change the name of the json file that you don't want to be overwritten. Anyway, if your connection speed drops by 75%, the script will automatically save a new json with the date of the issue in the same directory.
