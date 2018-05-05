# Reference: https://github.com/clickthisnick/CraigLister/blob/master/README.md
1. Install Python (sudo yum install python)
2. Install python selenium Library (sudo pip install selenium)
3. Install python gmail Library (sudo pip install gmail)
4. Install python Pillow Library (sudo pip install Pillow)
5. Install Chrome Browser (curl https://intoli.com/install-google-chrome.sh | bash)
6. Get chromedriver for appropriate Chrome Version (Link - http://chromedriver.storage.googleapis.com/index.html)
7. As we have to run automation on server so browser is not able to initiate there. So for this we have to disable the display setting mode. So we need to install pyvirtualdisplay python Library (sudo pip install pyvirtualdisplay) and add some code line in the python script.
8. Also need other packages like xvfb (sudo yum install xorg-x11-server-Xvfb.x86_64) and python xvfbwrapper library (sudo pip install xvfbwrapper)

The python script avaiable on GitHub is for Python2 versions. We tried to run the script on the server but we got some errors while locating HTML elements on the page. So we will need to make some modification in Script.
