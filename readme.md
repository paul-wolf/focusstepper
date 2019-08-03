

https://medium.com/@cgulabrani/controlling-your-dslr-through-raspberry-pi-ad4896f5e225

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


For there server or wherever you are doing post-processing: 

```
sudo apt-get update
sudo apt-get install libltdl-dev libusb-dev libexif-dev libpopt-dev
sudo apt-get install -y imagemagick && \
sudo apt-get install -y ufraw && \
sudo apt install -y hugin-tools && \
sudo apt-get install -y enblend
```


##Notes for Mac

Install ufraw for imagemagick to be able to convert nef to tiff:

```
brew update
brew install ufraw
```

##References

<http://zerenesystems.com/cms/stacker>

<https://www.photomacrography.net/>

<https://blogs.scientificamerican.com/compound-eye/build-a-world-class-insect-imaging-system-for-under-6-000/>

<https://www.cognisys-inc.com>

<https://github.com/jim-easterbrook/python-gphoto2>

<http://www.gphoto.org/proj/libgphoto2/support.php>

<http://www.microscopy-uk.org.uk/mag/artjun09/rp-stack.html>

<http://www.superrobotica.com/download/s310405/es3000-guide.pdf>
