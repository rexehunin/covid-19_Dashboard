# Covid-19 Dashboard Readme
---
This python package is a Covid-19 Dashboard, designed to help users keep up-to-date with current
Covid data, and in the know with news articles regarding the ongoing coronavirus pandemic.
This readme, and the program itself, is formatted for use on Windows 10, and use on other platforms cannot be assured.

## Installations and Requirements
### Pip
This package requires a working version of python 3.9 to be installed on your machine. See [here][1] to
download the latest versions of python.

There are also several non-standard modules that must be installed using the [pip][2]
These modules are uk-covid19 and flask, and should be installed in the Command Prompt as shown
```bash
>pip install uk-covid19
>pip install flask
```

### News API
The program also utilises a News API system provided by the third party [newsapi.org][3]. In order to use the program, you must create an account and get a personal news API key. This key must then be written into the config.json file in the line marked "News_API" (Shown below)
```
{
    "Credentials":{
      "News_API": "" <------
    },
    ...
  }
```

## Usage
In order to utilise this program, simply open the flask_formatting.py file (within the Project folder) with your chosen python interpretter (if you downloaded python using the link above, you will have downloaded IDLE with the latest version of Python. This is what you should use)
Once opened, [run][4] the code.
Alternately, run the module from your Command Prompt as shown below (once you have [navigated to the file in your directory][5])
```bash
>python flask_formatting.py
```

Once the code is running, using any web browser, enter 127.0.0.1:5000/ into the address bar

![Image][6]

## Personalisation and Configuration
The file config.json allows for aspects of the program to be altered easily and safely. Just look for the key for the data you wish to change and enter the relevant data you want instead, following the rules specified below. The config file allows for altering of:
### 1. The Lower Tier Local Authority.
You may enter any region specified [here][7]. 
### 2. The Relevant Nation.
This must match with the nation the above Lower Tier Local Authority resides in.
### 3. Number of news articles added per update.
The number of articles fetched every news refresh. *Note: This number is only guaranteed for the initial news request. Later updates will not insert repeat articles, so the number specified is the maximum possible to be added, not the amount that will be added every time*
### 4. The terms searched for by the news article finder.
The words given to the news api request to find articles. These must be separated by a single space where multiple keywords are specified
### 5. The title of the dashboard.
The words that appear at the top of the web page


## Licence

Copyright (c) [2021]

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


[1]:https://www.python.org/downloads/
[2]:https://packaging.python.org/en/latest/tutorials/installing-packages/
[3]:https://newsapi.org/
[4]:https://realpython.com/run-python-scripts/#how-to-run-python-scripts-from-an-ide-or-a-text-editor
[5]:https://www.howtogeek.com/659411/how-to-change-directories-in-command-prompt-on-windows-10/
[6]:https://carldesouza.com/wp-content/uploads/2020/01/img_5e30bf192167a.png
[7]:https://www.google.com/maps/d/viewer?hl=en&authuser=0&mid=1S_AbfmYbOpHBeyLEcmB9f-wRD4Y&ll=52.82654487488067%2C0.5039275520141473&z=7

