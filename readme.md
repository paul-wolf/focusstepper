The purpose of this is to control a camera on a focus rail with a stepper motor, capture images for focus stacking. You'll need a focus rail, stepper mechanism, camera with usb port for control, a Raspberry PI and an AWS account to make any use of this.

MIT License, see the license file. No warranties whatsoever.

This is a very early version of this software and mainly for my own use. Use at your own risk, but feel free to get in touch if you want something. 

The main thing here is the ability to move files around cloud services. We use AWS S3 as a storage host. Once everything is installed, you can call the main utility:

    ./fs

This makes it easy to capture 100 images having them all uploaded to S3 as you go. You can then easily get them to a platform where you can process them with software like https://zerenesystems.com.

You'll need your own focus rail and usb connection to the camera. This setup runs on Raspberry PI 3 and up running Raspbian, as far as I know. I use an Automation Hat from Adafruit for the stepper motor control. 

     Linux raspberrypi 4.14.62-v7+ #1134 SMP Tue Aug 14 17:10:10 BST 2018 armv7l GNU/Linux

You need at least Python 3.5. 

Make sure you have a `.env` file that looks something like this:

```
AWS_ACCESS_KEY_ID=<YOUR AWS KEY ID HERE>
AWS_SECRET_ACCESS_KEY=<YOUR SECRET HERE>
BUCKET=<AWS BUCKET NAME>
PATH_DATA=./data
DEFAULT_STACK_COUNT=10
DEFAULT_STEP_INCREMENT=30
```

Install some system requirements:

```
sudo apt-get update
sudo apt-get install libltdl-dev libusb-dev libexif-dev libpopt-dev
```

Install gphoto2:

```
wget http://downloads.sourceforge.net/project/gphoto/gphoto/2.5.2/gphoto2-2.5.23.tar.bz2
tar xjvf gphoto2–2.5.23.tar.bz2
cd gphoto2–2.5.23/
./configure
make
sudo make install
cd ..
```


Install libgphoto:

```
wget http://downloads.sourceforge.net/project/gphoto/libgphoto/2.5.2/libgphoto2-2.5.23.tar.bz2
tar xjvf libgphoto2–2.5.23.tar.bz2
cd libgphoto2–2.5.23/
./configure
make
sudo make install
cd ..
```

Now create the virtual environment:

```
sudo apt install virtualenv
virtualenv -p python3 .venv && \
source ./.venv/bin/activate
pip install -r requirements.txt
```

Make sure the camera is turned on: 

gphoto2 --auto-detect


For the server or wherever you are doing post-processing: 

```
sudo apt-get update
sudo apt-get install libltdl-dev libusb-dev libexif-dev libpopt-dev
sudo apt-get install -y imagemagick && \
sudo apt-get install -y ufraw && \
sudo apt install -y hugin-tools && \
sudo apt-get install -y enblend
```

In the end, I decided to use https://zerenesystems.com. It's very reasonably priced and easy to use with excellent documentation and support. Runs on all platforms you might want. 

##Notes for Mac

Install ufraw for imagemagick to be able to convert nef to tiff:

```
brew update
brew install ufraw
```

Commands:

In the base directory, use these commands:

   fs session: start an image stack capture session
   fs list: get all files in a stack session store in local data directory
   fs get: get files from S3
   fs put: put files to S3

First, make sure your virtualenv is activated:

       source .venv/bin/activate

Start a session: 

```
(.venv) pi@raspberrypi:~/prj/photo $ ./fs session

    use keys:

    i, j: forward by increment (100 by default)
    k, l: backward by increment (100 by default)
    p: set parameters (step increment)
    e: edit stack id
    n: new stack id
    s: session info
    c: capture, move files to s3
    a: capture entire stack
    h, ?: help (this message)
    q: quit
```					

etc.

##References

<http://zerenesystems.com/cms/stacker>

<https://www.photomacrography.net/>

<https://blogs.scientificamerican.com/compound-eye/build-a-world-class-insect-imaging-system-for-under-6-000/>

<https://www.cognisys-inc.com>

<https://github.com/jim-easterbrook/python-gphoto2>

<http://www.gphoto.org/proj/libgphoto2/support.php>

<http://www.microscopy-uk.org.uk/mag/artjun09/rp-stack.html>

<http://www.superrobotica.com/download/s310405/es3000-guide.pdf>
