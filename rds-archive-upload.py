# -*- coding: utf-8 -*-
import argparse
import logging
from os.path import getsize, isfile
import sys
import time

import tqdm
import oss2

import common

fmt = '[%(name)s %(levelname)s] %(message)s'

logging.basicConfig(level=logging.WARNING, format=fmt)
logging.getLogger('oss2').handlers.clear()
logging.getLogger('oss2').setLevel(logging.WARNING)

ap = argparse.ArgumentParser()
ap.add_argument('--file', required=True)
ap.add_argument('--name', required=True)

options = ap.parse_args()

endpoint = 'http://oss-cn-hangzhou.aliyuncs.com'

AccessKeyId = common.config['ACCESS_KEY_ID']
AccessKeySecret = common.config['ACCESS_KEY_SECRET']

auth = oss2.Auth(AccessKeyId, AccessKeySecret)
bucket = oss2.Bucket(auth, endpoint, 'rds-archive')


fn = options.file
on = options.name

if not isfile(fn):
    print('--file "{}" is not a file readable!'.format(fn))
    sys.exit(1)

totalSize = getsize(fn)
partSize = oss2.determine_part_size(totalSize, preferred_size=128 * 1024)

multiRequest = bucket.init_multipart_upload(on)
uploadId = multiRequest.upload_id

ts = time.time()
with tqdm.tqdm(
        total=totalSize, unit='byte',
        unit_scale=True, unit_divisor=1024) as bar:

    with open(fn, 'rb') as fh:
        parts = []
        partNumber = 1
        offset = 0
        while offset < totalSize:
            sizeToUpload = min(partSize, totalSize - offset)
            fo = oss2.SizedFileAdapter(fh, sizeToUpload)
            result = bucket.upload_part(on, uploadId, partNumber, fo)
            partInfo = oss2.models.PartInfo(
                partNumber, result.etag,
                size=sizeToUpload, part_crc=result.crc)
            parts.append(partInfo)
            bar.update(sizeToUpload)
            offset += sizeToUpload
            partNumber += 1

        bucket.complete_multipart_upload(on, uploadId, parts)
te = time.time()
tc = (te - ts)

print('upload completed in %.2fs' % tc)
