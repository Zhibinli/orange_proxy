Simple Orange Proxy
=========================
Proxy features:
1) Inject x-forwarded-for and x-msisdn headers
2) Make request to url defined by ‘n’ param by incomming request by client
3) Forward any response and headers back to client 

How to install
=========================
Prerequisite: python3

Install requeired packages in python virtual env
```
brew install pipenv
pipenv install requests flask
```

run the proxy server (only with python3)
```
pipenv shell
cd orange_proxy/orange_proxy/
export FLASK_APP=./__init__.py
flask run
```

Open web browser and go:
http://127.0.0.1:5000?n=https://www.google.com


Set up HTTPS for proxy
=========================
TBA