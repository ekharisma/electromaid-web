import requests, random, json
import time
import paho.mqtt.client as paho


# Create your models here.


class Auth:
    def __init__(self):
        self.response = None
        self._token = None
        self.url = None
        self._data = None
        self._name = None
        self._email = None
        self._password = None

    def login(self):
        self.url = 'https://elektromaid.herokuapp.com/v1/auth/login'
        self._data = {'email': self._email, 'password': self._password}
        response = requests.post(self.url, json=self._data)
        token = response.json()
        self._token = token.get('token')
        if response.ok:
            print("Login success")
            return True
        return False

    def register(self):
        self.url = 'https://elektromaid.herokuapp.com/v1/auth/signup'
        self._data = {'name': self._name, 'email': self._email, 'password': self._password}
        self.response = requests.post(self.url, json=self._data)
        token = self.response.json()
        self._token = token.get('token')

    def get_email(self):
        return self._email

    def get_password(self):
        return self._password

    def set_email(self, email):
        self._email = email

    def set_password(self, password):
        self._password = password


class Sensor_data:
    def __init__(self):
        self.id = ""
        self.master_id = ""
        self.device_list = list()
        self.date = ""
        self.url = "https://elektromaid.herokuapp.com/v1/sensor"
        self.url_put = "https://elektromaid.herokuapp.com/v1/sensor/5fe1542d34c511565e0fb8a4"


class Usage_properties(Sensor_data):
    def __init__(self):
        super().__init__()
        self.data = ""

    def get_data(self):
        data = requests.get(self.url).json()
        return data[0]

    def data_to_use(self):
        self.data = self.get_data()
        print(self.data)

    def get_id(self):
        self.data_to_use()
        return self.data.get('_id').get('$oid')

    def get_master_id(self):
        self.data_to_use()
        return self.data.get('master_id')

    def get_watt_total(self):
        self.data_to_use()
        print(self.data)
        return self.data.get('watt_total')

    def get_device_by_id(self):
        self.data_to_use()
        return self.data.get('device')


class Control_properties(Sensor_data):
    def __init__(self):
        super().__init__()
        self.data = ""
        self.form_data = ""
        self.header = {
            'x-api-key': 'eiWee8ep9due4deeshoa8Peichai8Eih'
        }

    def set_data(self):
        self.data = requests.get(self.url).json()

    def get_from_data(self, data):
        self.form_data = data

    def get_device(self):
        self.set_data()
        return self.data[0].get('device')

    def put_data(self):
        print("Call me ?")
        devices = self.data
        master_id = devices.get('master_id')
        key_to_delete = ['_id', 'master_id', 'watt_total', 'date']
        for key in key_to_delete:
            del devices[key]
        devices = devices.get('device')
        data_value = {
            'id': self.form_data.get('id'),
            'daya': self.form_data.get('daya'),
            'status': self.form_data.get('status'),
            'aktif': self.form_data.get('aktif')
        }

        self.publish_data(master_id, self.form_data.get('id'), self.form_data.get('status'), self.form_data.get('aktif'))

        is_found = True;
        for i in range(devices.__len__()):
            if devices[i].get('id') == data_value.get('id'):
                devices[i] = data_value
                print("Found !")
                is_found = True
                break
            else:
                is_found = False
                print("Not Found")

        if not is_found:
            devices.append(data_value)
        data_to_sent = {'device': devices}
        response = requests.put(self.url_put, json=data_to_sent, headers=self.header)
        if response.ok:
            return True
        else:
            return False

    def on_message(self, client, userdata, message):
        time.sleep(1)
        print("received message =", str(message.payload.decode("utf-8")))

    def publish_data(self, master_id, device_id, status, aktif):
        client_id = self.random_generator()
        broker = "broker.mqtt-dashboard.com"
        client = paho.Client('client-' + str(client_id))
        url = "elektromaid/" + master_id + "/" + device_id
        print(url)
        client.on_message = self.on_message
        client.connect(broker)
        client.loop_start()
        print("subscribing ")
        client.subscribe(url)  # subscribe
        time.sleep(2)
        print("Publishing")
        client.publish(url, status)
        time.sleep(4)
        client.publish(url, aktif)
        time.sleep(4)
        client.disconnect()
        client.loop_stop()

    def random_generator(self):
        return random.randint(0, 999)

    def delete_data(self):
        global i
        devices = self.data[0]
        key_to_delete = ['_id', 'master_id', 'watt_total', 'date']
        for key in key_to_delete:
            del devices[key]
        devices = devices.get('device')
        for i in range(devices.__len__()):
            if devices[i].get('id') == self.form_data.get('id'):
                break

        del devices[i]
        data_to_sent = {'device': devices}
        response = requests.put(self.url_put, json=data_to_sent, headers=self.header)
        print(response.json())


def blog_request():
    post_call = requests.get("https://elektromaid.herokuapp.com/v1/post")
    post = post_call.json()
    return post


def chart_data():
    labels = [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
    ]
    data = []

    for x in range(7):
        data.append(random.randint(0, 200))

    return labels, data
