# Flask-SQLAlchemy-REST

Small, Flask app that demonstrates skeleton of a Flask-SQLAlchemy RESTFul api

# Understanding Serializing/De-serializing

- https://stackoverflow.com/questions/7907596/json-dumps-vs-flask-jsonify

# Introduction

- This Flask application uses SQLAlchemy and marshmallow(for serializing/de- serializing) to make a small, REST + CRUD(create, read, update, delete) API.

# Getting started

- `git clone` the repo!

- If you're using a virtual environment activate it!(I'll assume virtualenv with the named environment "venv"),

- Use `pip install -r requirements.txt` to get all the dependencies.

- `python app.py` should get you up and running!

- Try it out in Postman! (postman is a API development environment that lets you test PUT, GET, DELETE, POST functionality)

# Handling json and python dictionaries

If you're processing a request in flask (hopefully using the request import), you'll need a way to turn a json request into a python readable form. Additionally, you're

## Handling an incoming json response

A good way to do this is to take your request and invoke the `.get_json()` method on request. This goes into the request and "parses-out" the data from the json into python ready code! One important thing to note is that the content type header and form of the json must already be valid, otherwise a error will be thrown. Using flask request already does this for us, but it's important to keep in mind.

See the example code below

```
from flask import Flask, request, render_template_string
...
@app.route('/takejson',methods=["POST"])
def takejson():	#Let's say we sent the following json: {"name":"Anton"}
    data = request.get_json() #The data var is now a python dictionary with the json values!
    return render_template_string('hello {{ what }}', what=data["name"])
    #Return a h1 with the data that we pulled out and have in our data!

```

## Sending a JSON response

After we have handled data, or done whatever was needed, we're going to want our API to send a response in JSON form so that our API can talk to any(almost) interface. A simple way to do this is to use flask's jsonify module that returns a flask.Response() object that does some of the grunt work for us (setting the header's content type to application/json and so on) vs using alternative methods like json.dumps() which simply attempts to converted to json string.

Let's take a look at an example below

```
from flask import Flask, request, jsonify
...
@app.route('/takejson',methods=["GET"])
def takejson():	#Let's say we sent the following json: {"name":"Anton"}
    data = {"Is the earth flat?":"Maybe"} # Make a python dict (could have been generated from the user)    return render_template_string('hello {{ what }}', what=data["name"])
    return jsonify(data) #Return a valid-form json as a flask.Response object.
```

Try this out using a API interface such as Postman!
