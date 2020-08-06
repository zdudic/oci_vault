#!/usr/bin/python3

import os
import sys
import oci
import base64
import argparse

parser = argparse.ArgumentParser(
         description="Read OCI secret")
parser.add_argument("-s", "--secret_id", help="OCI secret ID", required=True)
parser.add_argument("-c", "--config", help="OCI config file, default is ~/.oci/config", default="~/.oci/config")
parser.add_argument("-p", "--profile", help="Config profile, default is DEFAULT", default="DEFAULT")
args = parser.parse_args()
config=args.config
secret_id=args.secret_id
profile=args.profile

ociconfig = oci.config.from_file(config, profile)

try:
    secret_client = oci.secrets.SecretsClient(ociconfig)
    response = secret_client.get_secret_bundle(secret_id)
    base64_Secret_content = response.data.secret_bundle_content.content
    base64_secret_bytes = base64_Secret_content.encode('ascii')
    base64_message_bytes = base64.b64decode(base64_secret_bytes)
    secret_content = base64_message_bytes.decode('ascii')
    print(secret_content)
except oci.exceptions.ConfigFileNotFound:
    sys.exit("oci.exceptions.ConfigFileNotFound: {0}")
except oci.exceptions.ProfileNotFound:
    sys.exit("oci.exceptions.ProfileNotFound: {0}")
except:
    sys.exit("Cannot get secret " + args.secret_id)


