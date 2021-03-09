# Connection Analyzer

:stopwatch: :stopwatch: :stopwatch: 

Connection analyzer is a utility tool to monitor your internet connection. It's a simple Python script that does a speedtest every 8 hours and sends you an email with the latest values.

# Installation

To use the script you have to download it (and its dependencies) and give it permissions to execute.
```
$ pip install speedtest-cli
$ git clone https://github.com/0xfederama/connection-analyzer.git
$ cd connection-analyzer
$ chmod +x script.py
```
Now you can launch the script with  `./script.py`
If you want to execute the script every time you turn on your computer (or your raspberrypi) you just have to `todo`.

# Customization
You can customize the script as you want.
The first thing that you can customize is the email (row 9): if you don't want to receive an email leave the field as it is, otherwise write your own email. If you don't want to receive emails, **only** change this field.
You can customize also the value of the hours (row 10). With a default value of 6, you will receive an email every 6 hours. After 8 hours, the dictionary will be reset to default values, in order to see if, in a 6-hour span, the connection have had problems (otherwise, the average in a long span of hours will flatten the curve).