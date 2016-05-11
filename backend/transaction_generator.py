import requests
import datetime
import dateutil.parser
from random import randint
import random
from faker import Factory
import json
from pprint import pprint
import csv
import json

# BASE_URL = "http://10.0.150.54:8080"
# BASE_URL = "http://brewhacks.appspot.com"
BASE_URL = "http://localhost:8080"
fake = Factory.create()


def genenerate_product_keys():
    res = requests.get(BASE_URL + "/api/v1/products")
    list = json.loads(res.text).get('list')
    product_keys = []
    for m in list:
        product_keys.append(m.get('key'))
    return product_keys


product_keys = genenerate_product_keys()


def genenerate_product_map():
    res = requests.get(BASE_URL + "/api/v1/products")
    list = json.loads(res.text).get('list')
    product_map = {}
    for m in list:
        product_map[m.get('key')] = m.get('name')
    return product_map


product_map = genenerate_product_map()
# for i, p in enumerate(product_keys):
#     print i, p, product_map.get(p)
# pprint(product_map)

merchant_keys = [
#    "ag1kZXZ-YnJld2hhY2tzchgLEg1NZXJjaGFudE1vZGVsIgUyNzQ4NAw"
"agtzfmJyZXdoYWNrc3IaCxINTWVyY2hhbnRNb2RlbBiAgICAgOSRCgw"
]


def create_gender():
    return 'Male' if randint(0, 1) == 1 else 'Female'


def create_a_group():
    age_groups = ['21-25', '26-30', '31-35', '36-40', '41-45', '46-50', '51-55', '56-60', '61-65']
    return age_groups[randint(0, len(age_groups) - 1)]

def get_weighted_p_keys():
    r = randint(1, 10)
    if r >= 0 and r <=6:
        return product_keys[16] # amstel
    elif r > 6 and r <=7:
        return product_keys[28]
    else:
        return product_keys[randint(0, len(product_keys) - 1)]


def get_weighted_p_keys2():
    r = randint(1, 10)
    if r >= 0 and r <=6:
        return product_keys[37]
    elif r > 6 and r <=7:
        return product_keys[41]
    else:
        return product_keys[randint(0, len(product_keys) - 1)]


def get_weighted_p_keys3():
    return product_keys[41]  # 28 bud

def create_p_key(preferred_beer_index=None):
    # global product_keys
    if preferred_beer_index == 0:
        return product_keys[random.sample([0, 0, 0, 1, 2], 1)[0]]
    elif preferred_beer_index == 1:
        return product_keys[random.sample([3, 16, 16, 16, 5], 1)[0]]
    elif preferred_beer_index == 2:
        return get_weighted_p_keys()
    elif preferred_beer_index == 3:
        return get_weighted_p_keys2()
    elif preferred_beer_index == 4:
        return get_weighted_p_keys3()
    else:
        return product_keys[randint(0, len(product_keys) - 1)]


def create_m_key():
    return merchant_keys[randint(0, len(merchant_keys) - 1)]


def create_name():
    return fake.name().lower().replace(' ', '_')


def create_timestamp(date, busy_hour=7, busy_hour_sigma=4):
    # create_timestamp('2016-04-16')
    # print datestr
    # y, month, d = int(datestr.split('-')[0]), int(datestr.split('-')[1]), int(datestr.split('-')[2])
    y, month, d = date.year, date.month, date.day
    # r = random.gauss(7, 4)
    r = random.gauss(busy_hour, busy_hour_sigma)
    h = min(23, max(0, 12 + int(r)))
    m = randint(0, 59)  # min(60, max(0, int(60 * (r - int(r)))))
    # t = datetime.datetime(2016, 4, 16, h, m)
    #     t = datetime.datetime(y, month, d, h, m)
    t = datetime.datetime(y, month, d, h, 0)
    return t.isoformat()
    # return t.time()
    # return str(t.hour)


def create_coord(loc):
    random.random()
    r_x = random.randint(1, 99999)
    r_y = random.randint(1, 99999)

    # x = 40.752067
    # y = -74.005111
    x, y = float(loc.split(",")[0]), float(loc.split(",")[1])

    new_x = float(int(x * 1000) * 100000 + r_x) / 100000000
    new_y = float(int(y * 1000) * 100000 + r_y) / 100000000
    return str("%s, %s" % (new_x, new_y))


def execute_post(data):
    res = requests.post(
        # "http://brewhacks.appspot.com/api/v1/transactions",
        BASE_URL + "/api/v1/transactions",
        json=data)
    return res.status_code


def create_farenheit():
    farenheit = int(random.gauss(60, 10))
    return farenheit


def create_precipitation(is_default_raining=False):
    is_raining = randint(0, 6) == 6
    if is_raining or is_default_raining:
        precipitation = int(random.gauss(60, 10))
    else:
        precipitation = int(random.gauss(10, 5))
    return precipitation


def create_rdm_tx(date=datetime.datetime(2016, 2, 1, 0, 0, 0), debug=False, busy_hour=7, preferred_beer_index=None,
                  is_default_raining=False, busy_hour_sigma=7):
    name = create_name()
    transaction = {
        "timestamp": create_timestamp(date, busy_hour=busy_hour, busy_hour_sigma=busy_hour_sigma),
        "email": name + "@gmail.com",
        "profile": name + ".jpg",
        "gender": create_gender(),
        "age_group": create_a_group(),
        "job": "",
        "product_key": create_p_key(preferred_beer_index),
        "product": "",
        "merchant_key": create_m_key(),
        "merchant": "",
        "location": create_coord("40.729319,-73.986984"),  # create_coord("40.742326,-73.982513"),
        "farenheit": create_farenheit(),
        "precipitation": create_precipitation(is_default_raining),
    }
    # pprint(transaction)
    status = '200'
    if not debug:
        status = execute_post(transaction)
    print "%s %s" % (status, transaction)
    return transaction


### MAIN



for i in xrange(1):
    create_rdm_tx()

for i in xrange(100):
    create_rdm_tx()

# generate fake data -- 100
for i in xrange(100):
    create_rdm_tx('2016-04-16')

# timestamp order by
transactions = []
for i in xrange(100):
    transactions.append(create_rdm_tx('2016-04-05', debug=True, busy_hour=2, preferred_beer_index=1))
transactions.sort(key=lambda x: x.get('timestamp'))
pprint(transactions)
for tx in transactions:
    print tx.get('timestamp'), tx.get('product_key')

###
# different events

# sport events
for i in xrange(200):
    create_rdm_tx('2016-04-05', debug=True, busy_hour=2, preferred_beer_index=1)

# sunny day
for i in xrange(100):
    create_rdm_tx('2016-04-11', debug=True)
# rainy day
for i in xrange(30):
    create_rdm_tx('2016-04-12', debug=True, preferred_beer_index=0)

### generate for 60 days
date = datetime.datetime(2016, 2, 1, 0, 0, 0)
for i in range(30):
    for j in range(400 + randint(-2, 2)):
        create_rdm_tx(date, debug=False)
    date += datetime.timedelta(days=1)


### write to csv
def to_csv_time(date_str):
    date = dateutil.parser.parse(date_str)
    return date.strftime("%m/%d/%Y %H:%M:%S")


def to_csv_time_only(date_str):
    date = dateutil.parser.parse(date_str)
    return date.strftime("%H:%M:%S")


f = csv.writer(open("transactions3.csv", "wb+"))
f.writerow(["timestamp", "product", "gender", "age_group", "farenheit", "precipitation"])  # , "precipitation"

date = datetime.datetime(2016, 2, 1, 0, 0, 0)
for i in range(3):
    for j in range(100 + randint(-2, 2)):
        tx = create_rdm_tx(date, debug=True)
        f.writerow([
            to_csv_time(tx.get("timestamp")),
            # to_csv_time_only(tx.get("timestamp")),
            product_map.get(tx.get("product_key")),
            tx.get("gender"),
            tx.get("age_group"),
            tx.get("farenheit"),
            tx.get("precipitation"),
        ])
    date += datetime.timedelta(days=1)

# skews data too much
for i in xrange(200):
    tx = create_rdm_tx(datetime.datetime(2016, 2, 4, 0, 0, 0), debug=True, busy_hour=2, preferred_beer_index=1)
    f.writerow([
        to_csv_time(tx.get("timestamp")),
        product_map.get(tx.get("product_key")),
        tx.get("gender"),
        tx.get("age_group"),
        tx.get("farenheit"),
        tx.get("precipitation"),
    ])

for i in xrange(30):
    tx = create_rdm_tx(datetime.datetime(2016, 2, 5, 0, 0, 0), debug=True, busy_hour=2, preferred_beer_index=0,
                       is_default_raining=True)
    f.writerow([
        to_csv_time(tx.get("timestamp")),
        product_map.get(tx.get("product_key")),
        tx.get("gender"),
        tx.get("age_group"),
        tx.get("farenheit"),
        tx.get("precipitation"),
    ])

### generate for live demo
txs = []
date = datetime.datetime(2016, 4, 17, 0, 0, 0)
for j in range(200):
    tx = create_rdm_tx(date, debug=True, busy_hour=3, busy_hour_sigma=2)
    txs.append(tx)
txs.sort(key=lambda x: x.get('timestamp'))
for tx in txs:
    print tx.get('timestamp'), tx.get('product_key')


txs = []
date = datetime.datetime(2016, 4, 17, 0, 0, 0)
for j in range(200):
    tx = create_rdm_tx(date, debug=True, busy_hour=3, busy_hour_sigma=2, preferred_beer_index=2)
    txs.append(tx)
txs.sort(key=lambda x: x.get('timestamp'))
for tx in txs:
    print tx.get('timestamp'), product_map.get(tx.get('product_key'))
    # execute_post(tx)

###

date = datetime.datetime(2016, 2, 2, 0, 0, 0)
for i in range(5):
    txs = []
    for j in range(100):
        tx = create_rdm_tx(date, debug=True)
        txs.append(tx)
    txs.sort(key=lambda x: x.get('timestamp'))
    for tx in txs:
        s = execute_post(tx)
        print s, tx.get('timestamp'), product_map.get(tx.get('product_key'))
    date += datetime.timedelta(days=1)


txs = []
date = datetime.datetime(2016, 2, 9, 0, 0, 0)
for j in range(100):
    tx = create_rdm_tx(date, debug=True, busy_hour=3, busy_hour_sigma=2, preferred_beer_index=3)
    txs.append(tx)
txs.sort(key=lambda x: x.get('timestamp'))
for tx in txs:
    s = execute_post(tx)
    print s, tx.get('timestamp'), product_map.get(tx.get('product_key'))



# single update

txs = []
date = datetime.datetime(2016, 4, 22, 0, 0, 0)
for j in range(1):
    tx = create_rdm_tx(date, debug=True, busy_hour=3, busy_hour_sigma=2, preferred_beer_index=4)
    txs.append(tx)
txs.sort(key=lambda x: x.get('timestamp'))
for tx in txs:
    s = execute_post(tx)
    print s, tx.get('timestamp'), product_map.get(tx.get('product_key'))
