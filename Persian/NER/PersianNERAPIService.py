import requests,json

def callApi(url, data, tokenKey):
    headers = {
        'Content-Type': "application/json",
        'Authorization': "Bearer " + tokenKey,
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=data.encode("utf-8"), headers=headers,verify=False)
    return response.text,response.status_code

API_KEY='c1c3bbed-ea5e-ea11-80eb-98ded002619b'

def getToken(API_KEY):
    baseUrl = "http://api.text-mining.ir/api/"
    url = baseUrl + "Token/GetToken"
    querystring = {"apikey": str(API_KEY)}
    response = requests.request("GET", url, params=querystring)
    data = json.loads(response.text)
    tokenKey = data['token']
    return tokenKey


tokenKey = getToken(API_KEY=API_KEY)
print(tokenKey)
baseUrl = "https://api.text-mining.ir/api/"
url =  baseUrl + "NamedEntityRecognition/Detect"


input="عرض سلام و احترام ۵۶ متر لوکس موقعیت اداری موقعیت میدان کاج لابی و نگهبانی ۲۴ ساعته تابلو خور ساختمان ۱۰۰ درصد اداری دولاین آسانسور پارکینگ سالن اجتماعات یک اتاق کف پارکت آبدارخانه سند تک برگ ◾◼موارد مشابه را از ما بخواهید◼◾ لطفا فقط تماس بگیرید از ساعت 8 صبح تا 12 شب کارشناس اداری رحیمی 09127659558 ****گروه مشاورین املاک بزرگ مثلث**** آدرس دفتر : بلوار دادمان تقاطع حسن سیف تلفن دفتر : ۸۸۵۹۱۵۰۰ داخلی ۳۵۶"

payload = u'"{}"'.format(input)
result = callApi(url, payload, tokenKey)
print(result)
if result[1]==200:
    res = json.loads(result[0])
    for phrase in res:
        print("("+phrase['word']+","+str(phrase['tags']['NER'])+") ")
