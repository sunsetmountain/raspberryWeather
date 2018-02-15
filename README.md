# raspberryWeather

You will build an IoT device (Raspberry Pi) that measures weather data and is ready to interact with the Google Cloud Platform. In conjunction with the steps included in a [Google Codelab](https://codelabs.developers.google.com/) ("Building a Serverless Data Pipeline: IoT to Analytics"), the weather data can be published to a data pipeline that includes a message queue, a serverless function, a Cloud-based data warehouse and an analytics dashboard using Google’s Cloud Platform.

## Getting Started

### Prerequisites

* [Raspberry Pi Zero W starter kit](https://www.canakit.com/raspberry-pi-zero-wireless.html) - $34.95

* [USB card reader](https://www.amazon.com/Anker-Portable-Reader-RS-MMC-Micro/dp/B006T9B6R2) - $9.99

* [USB hub](https://www.walmart.com/ip/Anker-Ultra-Slim-4-Port-USB-3-0-Data-Hub/178554397) (to allow for connecting a keyboard and mouse into the sole USB port on the Raspberry Pi) - $9.99

* [Female-to-female breadboard wires](https://www.adafruit.com/product/266) - $3.95

* [GPIO Hammer Headers](https://www.adafruit.com/product/3413) - $6.50

* [BME280 sensor](https://www.amazon.com/gp/product/B0118XCKTG/) - $9.99

* [Soldering iron](https://www.amazon.com/gp/product/B074V28ZVS/) (any will do, but this one is nice and includes solder) - $32.99

* Computer monitor or TV with HDMI input, HDMI cable, keyboard and a mouse

The Raspberry Pi Zero W is recommended for this codelab, but a Raspberry Pi 3 Model B will also work, won’t require hammer header pins or a USB hub, has a better CPU, but will cost more. If you choose to move forward with the alternate device, make certain that you have a power supply and an appropriate SD card.

### Assemble the Raspberry Pi and sensor

Solder the header pins to the sensor board. 

![alt text](screenshots/pins.png "Solder the header pins to the sensor board")

Carefully install the hammer header pins into the Raspberry Pi.

![alt text](screenshots/headerpins.png "Carefully install the hammer header pins")

Format the SD card and install the NOOBS (New Out Of Box Software) installer by following the [steps] here(https://www.raspberrypi.org/documentation/installation/noobs.md). Insert the SD card into the Raspberry Pi and place the Raspberry Pi into its case.

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

Use the breadboard wires to connect the sensor to the Raspberry Pi according to the diagram below.

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

Raspberry Pi pin -> Sensor connection
Pin 1 (3.3V) -> VIN
Pin 3 (CPIO2) -> SDA
Pin 5 (GPIO3) -> SCL
Pin 9 (Ground) -> GND




Connect the monitor (using the mini-HDMI connector), keyboard/mouse (with the USB hub) and finally, power adapter. 

### Configure the Raspberry Pi and sensor

After the Raspberry Pi finishes booting up, select Raspbian for the desired operating system, make certain your desired language is correct and then click on Install (hard drive icon on the upper left portion of the window).

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

Click on the Wifi icon (top right of the screen) and select a network. If it is a secured network, enter the password (pre shared key).

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

Click on the raspberry icon (top left of the screen), select Preferences and then Raspberry Pi Configuration. From the Interfaces tab, enable SSH and I2C. From the Localisation tab, set the Locale and the Timezone. After setting the Timezone, allow the Raspberry Pi to reboot.

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

After the reboot has completed, click on the Terminal icon to open a terminal window. 

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

Type in the following command to make certain that the sensor is correctly connected.


```
  sudo i2cdetect -y 1
```

The result should look like this -- make sure it reads 76.

![alt text](screenshots/wifi_selector.png "Select your wifi network and enter the password")

An all 0 result indicates that the sensor isn’t being read by the Raspberry Pi -- check the wiring and connections. 

A result other than 76 could indicate that the type of sensor doesn’t match the one recommended by this codelab and this will cause the sensor driver to not function correctly. To fix this situation, you’ll need to edit the Adafruit_BME280.py script that is downloaded in the “Install the sensor software and weather script” section below. For example, if the result is showing 74, you will need to change the BME280_I2CADDR to 0x74.

### Install the Google Cloud SDK

In order to leverage the tools on the Google Cloud platform, the Google Cloud SDK will need to be installed on the Raspberry Pi. The SDK includes the tools needed to manage and leverage the Google Cloud Platform and is available for several programming languages. In this Codelab, only a small portion of the SDK will be used (publishing messages to a queue using Google Cloud Pub/Sub).


Learn more about the Google Cloud SDK


Open a terminal window on the Raspberry Pi if one isn’t already open and set an environment variable that will match the SDK version to the operating system on the Raspberry Pi.

```
  export CLOUD_SDK_REPO=”cloud-sdk-$(lsb_release -c -s)”
```

Now add the location of where the Google Cloud SDK packages are stored so that the installation tools will know where to look when asked to install the SDK.

```
  echo “deb http://packages.cloud.google.com/apt $CLOUD_SDK_REPO main” |  sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
```

Add the public key from Google’s package repository so that the Raspberry Pi will verify the security and trust the content during installation

```
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
```

Make sure that all the software on the Raspberry Pi is up to date

```
  sudo apt-get update
```

Install the Google Cloud SDK using the Python package manager

```
  pip install --upgrade google-cloud
```

The installation speed of the SDK is dependent both on the network speed and the Raspberry Pi processor. The Raspberry Pi Zero W can take around 30 minutes to complete the install. If you are using the alternate hardware (Raspberry Pi 3 Model B), install times are typically much faster.


### Install the sensor software and weather script


From the command line on the Raspberry Pi, clone the needed packages for reading information from the input/output pins.

```
  git clone https://github.com/adafruit/Adafruit_Python_GPIO
```

Install the downloaded packages

```
  cd Adafruit_Python_GPIO

  sudo python setup.py install

  cd ..
```

Clone the project code that enables the weather sensor

```
  git clone https://github.com/sunsetmountain/raspberryWeather
```

Edit the script by typing…

```
  cd raspberryWeather

  nano checkWeather.py
```

Change the project to your Project ID and the topic to the name of your Pub/Sub topic (these were noted in the Getting Set-up and Create a Pub/Sub topic sections of this codelab). 

Change the sensorID, sensorZipCode, sensorLat and sensorLong values to whatever value you’d like. Latitude and Longitude values for a specific location or address can be found here.

When you’ve completed making the necessary changes, press Ctrl-X to begin to exit the nano editor. Press Y to confirm.

```
# constants - change to fit your project and location
SEND_INTERVAL = 10 #seconds
sensor = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
credentials = GoogleCredentials.get_application_default()
project="myProject" #change this to your Google Cloud project id
topic = "myTopic" #change this to your Google Cloud PubSub topic name
sensorID = "s-Googleplex"
sensorZipCode = "94043"
sensorLat = "37.421655"
sensorLong = "-122.085637"
```

Install the security key

Copy the security key (from the “Secure publishing to a topic” section) to the Raspberry Pi.

If you placed the security key into a storage bucket, use the link that you copied to download the file (i.e. change the bucket name and file name in the command below).

```
  wget https://storage.googleapis.com/yourStorageBucketName/yourSecurityKeyFilename.json
```

Since the security key stored in the storage bucket is publicly accessible, now would be a good time to go back into the Cloud Console and to turn off public sharing for this file.


If you instead have the security key downloaded on your local machine, use a method such as SFTP (secure file transfer protocol) to copy the file to the Raspberry Pi.


The default username for the Raspberry Pi should be “pi” and the password should be “raspberry”.


From the command line on the Raspberry Pi, export a path to the security key (change the filename to match what you have)

```
  export GOOGLE_APPLICATION_CREDENTIALS=/home/pi/yourSecurityKeyFilename.json
```

If you plan to utilize the Raspberry Pi extensively for weather measurement, placing the export statement into the .profile file to allow it to persist between reboots is advisable. The .profile file is in the /home/pi directory and can be edited using any available editor (e.g. vi or nano).

You now have a completed IoT weather sensor that is ready to transmit data to Google Cloud.


End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used
* Inspiration
* etc
