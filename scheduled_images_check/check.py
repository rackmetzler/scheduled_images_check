from prettytable import PrettyTable
import threading
import argparse
import sys
from libs.auth import CloudAuth
from libs.auth import convert_to_datetime
from libs.common import http_request
import requests
import time
from datetime import datetime
from datetime import timedelta


RESULTS = []


class Images(object):
    def __init__(self, auth, region):
        self.auth = auth
        self.region = region
        self.marker = None
        self.images = []
        self.getting_images = False

        if self.getting_images is False:
            print("Getting Images List for {}".format(region))
            self.get_latest_image("NONE")
            self.getting_images = True
        else:
            while not self.getting_images:
                time.sleep(10)

    def get_latest_image(self, server_id):
        url = self.auth.get_service_url('compute', self.region)
        url = "{0}/images/detail".format(url)

        latest_image = None
        latest_created_at = None

        if not self.images:
            response = http_request('get', url, self.auth.get_headers())
            response.raise_for_status()

            response_images = response.json()['images']
            for image in response_images:
                if ('org.openstack__1__created_by' in image['metadata'] and
                        image['metadata']['org.openstack__1__created_by'] ==
                        'scheduled_images_service'):
                    self.images.append(image)

        if server_id == "NONE":
            return

        for image in self.images:
            if image['server']['id'] == server_id:
                if not latest_created_at or \
                        latest_created_at < convert_to_datetime(
                        image['created'], format='%Y-%m-%dT%H:%M:%SZ'):
                    latest_created_at = convert_to_datetime(
                        image['created'], format='%Y-%m-%dT%H:%M:%SZ')

                    latest_image = {
                        'name': image['name'],
                        'id': image['id'],
                        'status': image['status'],
                        'created_at': image['created'],
                        'updated_at': image['updated']
                    }

        return latest_image


def start_verify(auth, region, server_uuid, server_name, images):
    url = auth.get_service_url('compute', region)

    try:
        response = http_request(
            'get',
            '{0}/servers/{1}/rax-si-image-schedule'.format(url, server_uuid),
            auth.get_headers())
    except requests.exceptions.HTTPError as e:
        print(
            "Error while communicating with API: Region {0} Server {1} "
            "Server Id {2} Error {3}".format(region, server_name,
                                             server_uuid, e))
        return
    if response.status_code == 404:
        RESULTS.append(
            {'region': region, 'id': server_uuid,
             'name': server_name, 'schedule': 'Not Configured',
             'retention': '', 'latest': {}})
        return

    image_schedule_data = response.json()['image_schedule']

    latest_image = images.get_latest_image(server_uuid)
    if 'day_of_week' in image_schedule_data:
        RESULTS.append(
            {'region': region, 'id': server_uuid, 'name': server_name,
             'schedule': 'Weekly on {0}'.format(
                 image_schedule_data['day_of_week']),
             'retention': image_schedule_data['retention'],
             'latest': latest_image})
    else:
        RESULTS.append(
            {'region': region, 'id': server_uuid, 'name': server_name,
             'schedule': 'Daily',
             'retention': image_schedule_data['retention'],
             'latest': latest_image})

    return


def main():
    desc = 'QC scripts for public cloud server creation'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('username', help='Cloud Account Username')
    parser.add_argument('apikey', help='Cloud Account API Key')
    parser.add_argument(
        '-f', '--failed_only', dest='failed_only', action='store_true',
        help="Show only instances where latest image is older "
             "than 24 hours and scheduled images is enabled")

    args = parser.parse_args()
    now = datetime.utcnow()
    threads = []

    auth = CloudAuth(args.username, args.apikey)

    regions = auth.get_regions(service_type='compute')

    for region in regions:
        print("Retrieving server list from region {}".format(region))
        url = auth.get_service_url('compute', region)

        response = http_request('get', '{}/servers'.format(url),
                                headers=auth.get_headers())

        images = Images(auth, region)
        print(
            "Starting to iterate through servers in region {}".format(region))
        for server in response.json()['servers']:
            t = threading.Thread(
                target=start_verify,
                args=(auth, region, server['id'],
                      server['name'], images)
            )
            t.start()
            threads.append(t)
            # If you want to run it not in threads:
            # start_verify(auth, region, server['id'], server['name'], images)

    print("Waiting for all servers, in all regions to finish")
    for thread in threads:
        print(
            "{0} Still waiting for all servers to complete".format(now))
        thread.join()

    print("Making data pretty")

    table = PrettyTable()
    table.field_names = ["Region", "Server Id", "Server Name",
                         "Schedule", "Retention", "Latest Scheduled Image",
                         "Image < 24 hrs"]

    for result in RESULTS:
        latest_image = None
        if result['latest']:
            latest_image = result['latest']

        if result['schedule'] == 'Not Configured':
            continue

        if latest_image:
            image_datetime = convert_to_datetime(latest_image['created_at'],
                                                 format='%Y-%m-%dT%H:%M:%SZ')
            if (latest_image['status'] in ['ACTIVE', 'SAVING'] and
                    now - timedelta(hours=24) < image_datetime):
                # If last image is less than 24 hours old from its
                # creation start

                if args.failed_only:
                    continue
                image_verified = "True"

            else:
                # Either the image is in an invalid status, or greater than
                #  24 hrs
                image_verified = "False"
        else:
            # Either the image is in an invalid status, or greater than 24 hrs
            image_verified = "False"

        tmp_row = [
            result['region'],
            result['id'],
            result['name'],
            result['schedule'],
            result['retention']
        ]
        if latest_image:
            image_table = PrettyTable(header=False)
            image_table.add_row(["Id", latest_image['id']])
            image_table.add_row(["Name", latest_image['name']])
            image_table.add_row(["Status", latest_image['status']])
            image_table.add_row(["Created At", latest_image['created_at']])
            image_table.add_row(["Updated At", latest_image['updated_at']])
            tmp_row.append(image_table.get_string())
            tmp_row.append(image_verified)
        else:
            tmp_row.append("None")
            tmp_row.append(image_verified)

        table.add_row(tmp_row)

    print(table)
    return 0


if __name__ == '__main__':
    sys.exit(main())
