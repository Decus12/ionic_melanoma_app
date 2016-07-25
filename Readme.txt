Readme on how to get ionic melanoma app debug version and it's server running for testing. At the moment only Android is supported. 

==========Requirements============
Ionic Framework
OpenCV2 (Anaconda includes it on Windows, for MacOS follow these instructions: http://www.pyimagesearch.com/2015/06/15/install-opencv-3-0-and-python-2-7-on-osx/)

To lib folder:
AngularJS
Jquery (currently the app uses 2.2.3)

Server requires NodeJS to be installed

MongoDB for database

npm install should install the rest but in case it doesn't you will need cordova file transfer and cordova file plugins. Cordova itself should be installed with ionic.


==========Server and Database============

Start MongoDB through mongod executable

Windows:
Navigate to the projects www folder and type "node server.js" on command prompt or "nodemon server.js" if using nodemon.

MacOS:
Every time the server is started you have to first make virtual environment for OpenCV to work. 
Type "source ~/.bash_profile" and then "mkvirtualenv cv" to terminal. Once that is done you will see (cv) to left of your prompt and you can start the server the same way like in Windows.


==========Installing to the device============
android-debug.apk used for installation is located in the main folder (ionic_melanoma_app). Follow the normal apk installation procedure. However, due to server not having set IP-address it may change and you may have to set it manually to the apps code beforehand. There are two locations to set it, one is in services.js and the other is in controllers.js. They are set to 192.168.1.9 at default.

Once server is started use ipconfig on command prompt (ifconfig on Mac terminal) and see what ip the server is using. If it's 192.168.1.9 you can use the apk file for installation, if not change the IP address in services.js and controllers.js to match the one that server is using. You can then build and install the app on the device by typing "ionic run android" to command prompt while in the ionic_melanoma_app folder and your phone or tablet is plugged in with a usb cable.

Mac users may need to use "sudo ionic run android".

==========Usage============
Once mongoDB and server are running and app has been installed to the mobile device it can be found among the other apps. It's named Melanoma App. There are currently two tabs in the app. First one is the starting screen and has basic info about the melanoma symptoms and a button to take a picture. The other one is status tab that shows the sent images and has more detailed info about them.

TAKING A PICTURE
Pressing the "Take picture" button opens the device's default camera. It doesn't have the guiding overlay yet so here's a guide how to take a picture as intended. Position the object (mole, but can be any dark object against lighter background) you want to analyse dead center of the screen. Zoom in as neccessary so that object and it's details are clearly visible in the image, but leave healthy skin visible at the edges of the screen. This is important so that analysis algorithms can find the object from the middle and healthy skin as reference from the sides. 

Once you have taken a picture your device will show it and ask whether to save or discard it. Discarding it returns you to camera view while saving it will send the image to server to be stored and analysed. Server will print out the results of the analysis, name of the picture and finally will print "sent" to the console if all went well, meaning the picture and the results of it's analysis were written to database. The database is called "melanoma" and results are saved into "images" collection.

STATUS SCREEN
Once you have succesfully taken a picture you can find it's details in this screen. At first you will see a thumbnail of the picture you took, the date you took it and a 0 underneath it. 0 is written to the database always as it marks the status doctor would give to the mole once s/he has taken a look at it. 0 simply means doctor hasn't taken a look at the picture yet. Doctor's app hasn't been implemented yet so this is just a placeholder for now. In the final version of the client side app 0 will be replaced by a colored icon.

0 = grey, doctor hasn't taken a look yet.
1 = green, doctor has taken a look and all is well.
2 = yellow, doctor would like to take a closer look at the mole. Nothing to worry, but just in case.
3 = red, danger, go see a doctor as soon as possible.

App analyses the found mole to help doctors to prioritize and dignose them. You can see these results yourself by pressing any of the entries in the status screen list. This will hide the list and opens a screen that show a larger picture and underneath it are listed the results of the algorithms. These are symmetry, color eveness and border eveness. You can also see afore mentioned doctor's analysis here. In the current version of the analysis results are also displayed as numbers. 0 means nothing abnormal found, 1 means maybe something found and 2 means something abnormal was found. You can return to list by bressing the back button underneath the analysis results.

==========Known Bugs============
- At least with the test phone I used, sending a second picture would always fail after the first picture had been sent succesfully. Simply taking a third picture and sending it always worked. This might be due to fact that the phone was an old model.
- In the status screen, pictures that were just taken are not shown in thumbnail or larger image in details screen initially. This is not a bug in get method however as the images become visible once the app is rebuild and reinstalled. Just restarting the app or phone won't fix this so it has to be reinstalled.