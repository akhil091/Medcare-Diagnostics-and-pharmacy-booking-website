import requests
import random
import time
from All_Users.models import Profile
import json

url = 'https://2factor.in/API/V1/6f79feae-90b3-11eb-a9bc-0200cd936042/SMS/+91'

char = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
        'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
        'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

def random_num():
    otp = 0
    for i in range(6):
        otp = 10 * otp + random.randint(0, 9)
        if otp == 0:
            otp = 1
    return otp


def generate_otp(num):
    otp = random_num()
    try:
        req = requests.get(url = url + num + '/' + str(otp))
        req = req.json()
        if req['Status'] == 'Success':
            return str(otp)
        else:
            return '-1'
    except requests.RequestException:
        return '-1'


def from_utc_to_local(offset):
    t1 = (time.time() - offset)
    print(time.time())
    print(offset)
    print(t1)
    if t1 > 3600:
        return True
    else:
        return False



def update_otp(mob, otp):
    try:
        otpObj = Profile.objects.get(Phone=mob)
        otpObj.otp = str(otp)
        otpObj.date = time.time()
        otpObj.save(update_fields=['otp', 'date'])
    except Profile.DoesNotExist:
        otpObj = Profile.objects.create(Phone=mob, otp=str(otp), date=time.time())
        otpObj.save()


def get_otp(mob, otp):
    try:
        otpObj = Profile.objects.get(Phone=mob)
        return otpObj.otp == otp and not from_utc_to_local(otpObj.date)

    except Profile.DoesNotExist:
        return False
