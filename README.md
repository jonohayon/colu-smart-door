#Colu Smart Door

####Disclaimer
This guide is still WIP, so it's not complete yet.

####What is this thing?
The colu smart door project is literally, a smart door powered by the Colu platform.

####What is Colu?
[Colu](http://colu.co) is an Israel-based startup aimed at digitizing the ownership of all your things through the blockchain — the public feed of Bitcoin transactions. The service provides an easy way to use the blockchain technology, originally meant for Bitcoin transactions, for anything, from cars, to art, to concert tickets.

####Where do I sign up?
There's no need to sign up, just follow the tutorial!

#Tutorial

####Before we start...
The code for the Raspberry Pi is written in Python and the server code is written in NodeJS. There's no need to install neither of them (if you deploy to Heroku and not to your VPS or something else) because Heroku will install Node for you and Python is already on the Pi.

####Requirments

 - Colu API key (you can get one [here](http://colu.co/getapikey))
 - Raspberry Pi
 - 1x P2N2222A Transistor
 - 1x Relay
 - 1x Electric door strike
 - A few jumper wires
 - Soldering Iron and Soldering Wire
 - A bit of technical 

##First - the server
So the server is written in NodeJS, which is in one of Heroku's native supported languages (which means that there's no need to install Node at all, which can sometimes be a pain in the ass).
Deploying the server to Heroku is easy as clicking a button which will let you deploy the script to a new Heroku app. The only parts that are needed configuration are some environment variables (read more [here](https://en.wikipedia.org/wiki/Environment_variable)) for the database (MongoDB, btw), called *DB_URI*, *DB_USER* and *DB_PASS*. Some other environment variables that needs to be declared are the *API_KEY* and the *PRIVATE_SEED* (an optional one), for the Colu Access module.

For the database, I would recommend using [Mongolab](http://mongolab.com), since it gives you free 500MB of DB storage for your needs (it's good for about 10 users I guess, but for more than that I would recommend to buy a bigger DB).

###Configuring the server
####1. DB (Mongolab)
Click on the "GET 500MB FREE" button:
![Mogolab main screen](https://www.evernote.com/shard/s471/sh/e490ae5b-3c8a-43be-873b-d12cc9ea7928/cb4486415b40b535/res/f6e7badb-5aba-4e38-8f22-e1c52b440c49/skitch.png?resizeSmall&width=832)

Signup to the service:
![Mongolab signup form](https://www.evernote.com/shard/s471/sh/6addc977-3bdb-4579-8179-f09e2f98aa7d/d428a5d31e4b1196/res/f137142d-86e0-4b4a-9a61-67591c17bcf7/skitch.png?resizeSmall&width=832)

After signing up and verifying the email, click on the "Create New" button to create a new database:
![Mongolab after signup](https://www.evernote.com/shard/s471/sh/878473c1-b02c-4673-b7fb-4640d4d58694/e3da3a4dee4c0473/res/bae69217-29dc-4f8a-aceb-465af49639ae/skitch.png?resizeSmall&width=832)

Now there will be a page with a lot of options. This is what you need to do:
![Mongolab change DB options](https://www.evernote.com/shard/s471/sh/b05a76d2-62bb-44c9-adcd-d84e15aac062/9c9f16b49b511d1e/res/b838ef77-f21d-4590-a801-37272f5a54ff/skitch.png?resizeSmall&width=832)

Then, set the DB's name and submit the form:
![Mongolab set DB name and submit form](https://www.evernote.com/shard/s471/sh/a768c7d5-925a-4d31-af29-057dda8a9192/fa91af67ecfcd6d3/res/27292620-8c26-4177-9a96-4e34497cbc61/skitch.png?resizeSmall&width=832)

On the DB page, go to the "Users" tab and click on "Add databse user":
![Mongolab add new user #1](https://www.evernote.com/shard/s471/sh/9d6011a2-b8ca-486a-add6-47e30435802a/d2fda13ab75c4156/res/c9362564-ba4c-4cc8-99cf-91dff812a672/skitch.png?resizeSmall&width=832)

Then, fill the form with the desired user credentials and click on the "Create" button (save the credentials for later use, you will need them):
![Mongolab add new user #2](https://www.evernote.com/shard/s471/sh/3e8ff840-67f3-4c39-ac89-ace9f8433e67/12ac751de8f919bc/res/eff51a5a-41da-4e37-9da0-6229a7eea8c9/skitch.png?resizeSmall&width=832)

Then, get the DB url from the page:
![Mongolab get the DB url](https://www.evernote.com/shard/s471/sh/244031b4-e491-4db6-8540-53d305bb829f/5d0cbae02b669418/res/e9fbb7b4-c033-45e4-bf9c-02fd59dbf07a/skitch.png?resizeSmall&width=832)

Now let's add the admin user so we can access the control panel itself.

First, let's add the "users" MongoDB collection: 
![Mongolab add collection step 1](https://www.evernote.com/shard/s471/sh/d7f7745f-cae8-44cc-aa8c-4de91cfd31d2/f2d8d0f2c494fbc9/res/47815c1c-e3a7-45d5-b9ad-1baf0cc6e2ac/skitch.png?resizeSmall&width=832)
![Mongolab add collection step 2](https://www.evernote.com/shard/s471/sh/ff120215-4f58-460a-b7c9-ba99deb9a668/49f62a3cffba9899/res/d51cc8df-617e-4d74-915e-d6a0fdaf76ca/skitch.png?resizeSmall&width=832)

Now, let's add the admin user to the collection. Click on the "Add document" button:
![Mongolab add admin step 1](https://www.evernote.com/shard/s471/sh/d4143037-6e95-4871-a1ed-d9d588b0a1ef/236324cea80c18c9/res/271c59bc-eae1-48ad-a495-3e388c793063/skitch.png?resizeSmall&width=832)

This will redirect you to a new page with a big textfield. Inside of it, put the next text portion after you change it to your needs:
```javascript
{
  "firstName": "<your name here",
  "lastName": "<your name here>",
  "type": "admin",
  "phone": "<your phone here>",
  "username": "coluadmin",
  "email": "<your email here>"
  "assetId": null
}
```
Then, click on the "Create and go back" button to create the document:


Now we can set up the server for our door!

####Server (Heroku)

For this part, you will need an Heroku account. You can sign up [here](http://heroku.com).

After you've signed up, click on this button to deploy the newest version of the server scripts to a new Heroku instance:

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/rezozo/colu-smart-door/tree/master/)

After the deployment has ended click on "manage app" to go to your app's dashboard and then choose the "Settings" tab:
![Heroku manage app button](https://www.evernote.com/shard/s471/sh/e25bf6bd-a73e-4be8-8d9d-c08b93e5ade0/e13bee11d3523c2e/res/e43b4f7d-66d6-40f6-ad1f-6c7be9b61892/skitch.png?resizeSmall&width=832)
![Heroku settings tab](https://www.evernote.com/shard/s471/sh/f11f77fa-8da2-4a55-98ec-30fc0d673a34/96399433e6b78444/res/c6658a4a-e1b0-4c4f-81ca-760453fd9b92/skitch.png?resizeSmall&width=832)

Inside of the "Settings" tab, click on "Reveal config vars":
![enter image description here](https://www.evernote.com/shard/s471/sh/96d4b534-f106-4c00-8404-221925a51308/f0e8da21f538f57a/res/dc0f8f5c-1b18-4f90-a183-23278823e7c1/skitch.png?resizeSmall&width=832)

Now we can see all of the config variables that our server needs to setup:
![Heroku config vars view](https://www.evernote.com/shard/s471/sh/2471fa30-958d-4750-8fa3-47e89fabb638/933b25a199d477a3/res/2a1239d1-3a35-4396-b410-d12fad8c61c6/skitch.png?resizeSmall&width=832)

But there are no config vars at the moment... so let's add them! For this step you'll need the DB URL, Username and Password, as well as your Colu API Key.
![Heroku add config var step 1](https://www.evernote.com/shard/s471/sh/ea5e7d4d-5b4b-4c52-9378-fb0ed6daa5d8/455ae2ef2e760dc5/res/2c826ef1-2240-4921-bae7-9701cd683056/skitch.png?resizeSmall&width=832)

Here is how you add a new config var + the names of the config vars that you need to add:
![Heroku config vars step 2](https://www.evernote.com/shard/s471/sh/02ee60fa-6a6d-4dd7-9cb5-aa953e066c20/62c1035521a90041/res/b9763a16-9bc8-4920-8d2a-fb7d22efe699/skitch.png)

Then, to make the changes actually matter, you'll need to restart the server like this:
![Heroku restart instance](https://www.evernote.com/shard/s471/sh/16d60f30-741f-475e-94b8-968d3763eef4/385d1aee0ac6f306/res/bfaa66bb-ed8a-4d76-b30f-4751fb81eaac/skitch.png?resizeSmall&width=832)

Done! The server is live now! You can now access your door's control panel like this: `<your app's name here>.herokuapp.com`