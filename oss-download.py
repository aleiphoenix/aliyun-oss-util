# -*- coding: utf-8 -*-
import argparse
import logging
import pprint

import oss2

import common


fmt = '[%(name)s %(levelname)s] %(message)s'

logging.basicConfig(level=logging.WARNING, format=fmt)
logging.getLogger('oss2').handlers.clear()
logging.getLogger('oss2').setLevel(logging.WARNING)

ap = argparse.ArgumentParser()
ap.add_argument('--bucket', required=True)
ap.add_argument('--filename', required=True)

options = ap.parse_args()

endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'
AccessKeyId = common.config['ACCESS_KEY_ID']
AccessKeySecret = common.config['ACCESS_KEY_SECRET']

auth = oss2.Auth(AccessKeyId, AccessKeySecret)
bucket = oss2.Bucket(auth, endpoint, options.bucket)

oss2.resumable_download(
    bucket, options.filename, options.filename,
    multiget_threshold=200*1024,
    part_size=100*1024,
    num_threads=3,
)
