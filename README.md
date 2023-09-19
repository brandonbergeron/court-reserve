# court-reserve
A Python script that automatically makes tennis court reservations on Court Reserve

## Installation (Windows):

### Prerequisites
- [Python 3.9+][0]
- [Pip][1] (comes with the standard install of python)
- [Chromedriver][2]


First, download the script:
```shell
git clone https://github.com/brandonbergeron/court-reserve.git
cd court-reserve
```
    
It is recommended that you install the requirements in a virtual environment [using venv][3] which comes with the standard Python install. To create and activate an environment run the following commands:
```shell
py -m venv court-reserve
.\court-reserve\Scripts\activate
```

After activating your virtual environment, install the project requirements by running:
```shell
pip install -r requirements.txt
```

To update the script, simply run:
```shell
git pull
```

## Local Setup:
You will need to enter your login credentials as well as edit the Court Reserve urls with your organizations ID in the ```utils/creds.py``` file. 

## Using the Script (Windows):
To run the script, navigate to the court-reserve directory and activate your virtual environment if needed(created above):
```shell
.\court-reserve\Scripts\activate
```
Then run the script:
```shell
py app.py
```

You will encounter several input prompts. The first prompt asks if you are running in test mode. Answer 'y' to avoid submitting actual reservation requests. If answering 'n', the script must be run and all prompts answered by 7:45am CT to allow the scheduler to start up the browsers. Otherwise the script will wait until the following day to run. 
```
Are you running in test mode? (y/n):
```

The second prompt asks for the amount of browsers you wish to run. A max of 15 browsers should be sufficient to cover the desired 1.5-2 second time window for reservation requests. 
```
? How many browsers to boot up?
```
If at any point you enter the wrong input, you can exit the script by typing ```ctrl+z``` and run it again from the beginning with: ```py app.py```

The script is scheduled to quit 2 minutes after submitting the requests. You can still quit it at any moment by typing ```ctrl+z```.

### Good Luck!

[0]: https://www.python.org/downloads/
[1]: https://pip.pypa.io/en/stable/installation/
[2]: https://chromedriver.chromium.org/downloads
[3]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/