## Util scripts for Aliyun OSS

```shell
$ python3 -m venv local
$ local/bin/pip install -r requirements.txt
```

fill in the `access_key_id` and `access_key_secret`

```
# config.py
ACCESS_KEY_ID = 'YOUR KEY ID'
ACCESS_KEY_SECRET = 'YOUR KEY SECRET'
```

see more help

```shell
$ local/bin/python oss-upload.py --help
```
