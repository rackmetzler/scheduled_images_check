# scheduled_images_check
Check if Scheduled Images are working properly

This package is used to verify that the latest image is less than 24 hours, for each server in each region for a Cloud Account.

This was created with Python 3.6 as a target environment, as this is the most prominate version of Python in the wild.

I always suggest running any custom scripts in a seperate Virtual Environment.  There are multiple projects out there to create those environments.

I use 'virtualenv' (python-virtualenv or python3-virtualenv) on Ubuntu 18.04 LTS.  This does not mean that this package won't work on other operating systems.

It was only manually developed and tested on that Operating System.


## Installing

* Clone this repo

git clone https://github.com/rackmetzler/scheduled_images_check

* Change Directory

cd scheduled_images_check

* Create Virtual Environment

virtualenv --python /usr/bin/python3.6 venv

* Activate Virtual Environment

source venv/bin/activate

* Install Requirements

pip install -r requirements.txt


## Example

In the scheduled_images_check directory, inside an Activated Virtual Environment with requirements installed.

### Show all servers on account, and define if it is valid or not.

python scheduled_images_check/check.py CLOUDUSER CLOUDAPIKEY

### Show only servers with scheduled images, where the latest image is over 24 hours old

python scheduled_images_check/check.py --failed_only CLOUDUSER CLOUDAPIKEY