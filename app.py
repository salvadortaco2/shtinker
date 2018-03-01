__author__ = "Asaf Gilboa"
__version__ = "1.0"

#TODO: 1st page -> input for one or many facebook URLs to profile
#Think about Snapchat later
#After the list is sent, show a bar of progress
# After the list is processed, load a new page with the results
import os, time
from flask import Flask, render_template, json, request, redirect, Response, stream_with_context
from instagram import Instagram
from image_analyzer import shtink_user
from shutil import rmtree
from time import sleep
app = Flask(__name__)

# Home Page
#@app.route("/")
#def main():
    #return render_template('index.html')
global usernames
# Use this to get the list of profiles
@app.route('/',methods=['GET', 'POST'])
def signUp():

    if request.method == 'GET':
        return render_template('signup.html')

    # These are all the URLs we will use
    global usernames
    usernames = request.form['inputUrls'].split('\r\n')
    return redirect("/results", code=302)

@app.route('/results')
def progress():

    privateUsers = []
    cleanUsers = []
    badUsers = []

    # Directory of /
    home_dir = os.path.dirname(os.path.realpath(__file__))

    global usernames
    
    def generate():
        for username in usernames:
            if username != "":

                # C:\..\static\asaf.gilboa
                userFolder = os.path.join(home_dir, "static", username)

                # Create directory for the user
                if not os.path.exists(userFolder):
                    os.makedirs(userFolder)
                else:
                    rmtree(userFolder)
                    os.makedirs(userFolder)

                insta = Instagram(username, userFolder)

                while insta.sum < insta.counter:
                    sleep(0.1)
                
                # Replace with Sagi's function
                list_of_bad = shtink_user(insta.pics_dic)
                user = User(insta.fullName, username, insta.profileUrl, list_of_bad)

                if user.badLinks:
                    badUsers.append(user)#User(url))
                elif insta.isPrivate:
                    privateUsers.append(user)
                else:
                    cleanUsers.append(user)
                yield "Scanned " + username + "'s profile...<br>"
        #x = 0
        #while x < 100:
            #print x
            #x = x + 10
            #time.sleep(0.2)
            #yield "data:" + str(x) + "\n\n"
        yield render_template('result.html', privateUsers = privateUsers, cleanUsers = cleanUsers, badUsers = badUsers)
    return Response(stream_with_context(generate()))
	
class User():
    def __init__(self, name, username, linkToProfile, badLinks):
        self.name = name
        self.username = username
        self.linkToProfile = linkToProfile
        self.badLinks = badLinks

if __name__ == "__main__":
    app.run()
