# scheduled_images_check
Check if Scheduled Images are working properly

This package is used to verify that the latest image is less than 24 hours, for each server in each region for a Cloud Account.

This was created with Python 3.6 as a target environment, as this is the most prominate version of Python in the wild.

I always suggest running any custom scripts in a seperate Virtual Environment.  There are multiple projects out there to create those environments.

I use 'virtualenv' (python-virtualenv or python3-virtualenv) on Ubuntu 18.04 LTS.  This does not mean that this package won't work on other operating systems.

It was only manually developed and tested on that Operating System.


## Installing

* Clone this repo

```
git clone https://github.com/rackmetzler/scheduled_images_check
```

* Change Directory

```
cd scheduled_images_check
```

* Create Virtual Environment

```
virtualenv --python /usr/bin/python3.6 venv
```

* Activate Virtual Environment

```
source venv/bin/activate
```

* Install Requirements

```
pip install -r requirements.txt
```

## Example

In the scheduled_images_check directory, inside an Activated Virtual Environment with requirements installed.

### Show all servers on account, and define if it is valid or not.

python scheduled_images_check/check.py CLOUDUSER CLOUDAPIKEY

#### Example Output

```
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
| Region |              Server Id               | Server Name  |     Schedule     | Retention |                 Latest Scheduled Image                | Image < 24 hrs |
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
|  DFW   | aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa |  server1     |      Daily       |     7     |                          None                         |     False      |
|  DFW   | bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb |  server2     |      Daily       |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | 49788dda-4eb9-4681-8ad4-83353ea3a27b | |                |
|        |                                      |              |                  |           | |    Name    |     Daily-server2-1491344769         | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2017-04-04T22:26:09Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2017-04-04T23:16:29Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | cccccccc-cccc-cccc-cccc-cccccccccccc |  server3     |      Daily       |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | 01cea5e0-c15c-4931-93e4-c3837d5fb3e4 | |                |
|        |                                      |              |                  |           | |    Name    |    Daily-server3-1491336129          | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2017-04-04T20:02:09Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2017-04-04T22:43:43Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | dddddddd-dddd-dddd-dddd-dddddddddddd |  server4     | Weekly on SUNDAY |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | d4d19c24-4375-48b1-b267-8346da1a8113 | |                |
|        |                                      |              |                  |           | |    Name    |       Weekly-server4-1544949255      | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2018-12-16T08:34:15Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2018-12-16T14:09:49Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee |  server5     |      Daily       |     7     | +------------+--------------------------------------+ |      True      |
|        |                                      |              |                  |           | |     Id     | 9b0dada9-b81b-47ae-a787-f0c4b59c2f5c | |                |
|        |                                      |              |                  |           | |    Name    |     Daily-server5-1545085273         | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2018-12-17T22:21:13Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2018-12-18T01:04:14Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | ffffffff-ffff-ffff-ffff-ffffffffffff |  server6     |      Daily       |     7     | +------------+--------------------------------------+ |      True      |
|        |                                      |              |                  |           | |     Id     | 212f960e-f095-46f9-ac08-64a07ddb67cc | |                |
|        |                                      |              |                  |           | |    Name    |     Daily-server6-1545095839         | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2018-12-18T01:17:20Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2018-12-18T07:34:37Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
```

### Show only servers with scheduled images, where the latest image is over 24 hours old

python scheduled_images_check/check.py --failed_only CLOUDUSER CLOUDAPIKEY

#### Example Output

```
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
| Region |              Server Id               | Server Name  |     Schedule     | Retention |                 Latest Scheduled Image                | Image < 24 hrs |
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
|  DFW   | aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa |  server1     |      Daily       |     7     |                          None                         |     False      |
|  DFW   | bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb |  server2     |      Daily       |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | 49788dda-4eb9-4681-8ad4-83353ea3a27b | |                |
|        |                                      |              |                  |           | |    Name    |     Daily-server2-1491344769         | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2017-04-04T22:26:09Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2017-04-04T23:16:29Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | cccccccc-cccc-cccc-cccc-cccccccccccc |  server3     |      Daily       |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | 01cea5e0-c15c-4931-93e4-c3837d5fb3e4 | |                |
|        |                                      |              |                  |           | |    Name    |    Daily-server3-1491336129          | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2017-04-04T20:02:09Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2017-04-04T22:43:43Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
|  DFW   | dddddddd-dddd-dddd-dddd-dddddddddddd |  server4     | Weekly on SUNDAY |     7     | +------------+--------------------------------------+ |     False      |
|        |                                      |              |                  |           | |     Id     | d4d19c24-4375-48b1-b267-8346da1a8113 | |                |
|        |                                      |              |                  |           | |    Name    |       Weekly-server4-1544949255      | |                |
|        |                                      |              |                  |           | |   Status   |                ACTIVE                | |                |
|        |                                      |              |                  |           | | Created At |         2018-12-16T08:34:15Z         | |                |
|        |                                      |              |                  |           | | Updated At |         2018-12-16T14:09:49Z         | |                |
|        |                                      |              |                  |           | +------------+--------------------------------------+ |                |
+--------+--------------------------------------+--------------+------------------+-----------+-------------------------------------------------------+----------------+
```
