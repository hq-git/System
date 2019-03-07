#!/usr/bin/env python                                                              

import boto.ec2
import helper.region
import argparse

# Get regions from AWS                                                             
regions = boto.ec2.regions()
# Create region name list                                                          
regions = [reg.name for reg in regions]
# Get current region                                                               
current_region = helper.region.get_default()
print("-" * 30)
print("Current region: \033[1m{0}\033[0m".format(current_region))
print("-" * 30)


def main():
    parser = argparse.ArgumentParser(description='Edanz AWS CLI Tool - Change default region')
    parser.add_argument('region', choices=regions, help='The region set to default region')
    parser.add_argument('-v', '--version', default=0.1, action='version', version='%(prog)s 0.1')
    args = parser.parse_args()
    region = args.region
    if helper.region.set_default(region):
        print("Default region was changed to %s" % region)
    else:
        print("Failed setup default region to %s" % region)


if __name__ == "__main__":
    main()               