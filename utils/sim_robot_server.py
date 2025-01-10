from flask import Flask, request
from gevent import pywsgi
import os, logging, sys, argparse
import base64, json
import datetime, logging, math
from ctypes import *
from scipy.spatial.transform import Rotation as R
import numpy as np
import requests

app = Flask(__name__)

@app.route("/clearerr", methods=['POST'])
def GenerateP0Demo():
    logger.info("start clearerr ...")
    # param = request.get_json()
 

    return {"res": 1}

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建FileHandler对象
    fh = logging.FileHandler('log.log')
    fh.setLevel(logging.DEBUG)
    # 创建Formatter对象
    formatter = logging.Formatter('%(asctime)s[%(levelname)s]: %(message)s')
    fh.setFormatter(formatter)
    # 将FileHandler对象添加到Logger对象中
    logger.addHandler(fh)

    # 记录日志信息
    logger.info('start server ...')
    server = pywsgi.WSGIServer(('127.0.0.1', 5001), app)
    server.serve_forever()