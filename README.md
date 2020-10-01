Simple Orange Proxy
=========================
Function: 

How to install:
=========================
Prerequisite: python3
brew install pipenv

install requeired packages in python virtual env
```
pipenv install requests
pipeen install flask
```

run the proxy server (only with python3)
```
pipenv shell
cd orange_proxy/orange_proxy/
export FLASK_APP=./__init__.py
flask run
```