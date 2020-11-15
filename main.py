import cx_Oracle
from config import API_SERVER, ORACLE
import requests
import json

class ApiServerInvoker():
    foods_in_api_server = []
    def __init__(self, base_url, keyword):
        self.base_url = base_url.rstrip('/')
        self.keyword = keyword

    def openApi(self, path):
        endpoint = self.base_url + '/' + path.lstrip('/')
        response = requests.get(endpoint)
        if response.ok:
            data = json.loads(response.content)
            _foods = data['foods']
            for food in _foods:
                if food['code'] == self.keyword:
                    self.foods.append(food['name'])
                else:
                    print(food['name'])

        print('The number of foods retrieved from API SERVER: ' + str(len(self.foods)))

    def getFoods(self):
        return self.foods

class FoodDB():
    def __init__(self, host, port, sid, username, password):
        self.dsn = cx_Oracle.makedsn(host, port, sid)
        self.username = username
        self.password = password
        self.connection = None
        self.cur = None

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(
                self.username,
                self.password,
                self.dsn,
                encoding=ORACLE.encoding)
            self.cur = self.connection.cursor()

        except cx_Oracle.Error as error:
            print(error)

    # After receiving active(not expired) foods from api server, update foods expiration in oracle database
    def process(self, query_select, query_update, foods):
        active_foods_in_api_server = foods
        self.cur.execute(query_select)
        active_foods_in_oracle = []
        for food in self.cur:
            active_foods_in_oracle.append(food[0])
        print('The number of non expired foods from Oracle DB: ' + str(len(active_foods_in_oracle)))

        set_difference = set(active_foods_in_oracle) - set(active_foods_in_api_server)
        to_be_updated_foods = list(set_difference)
        print('The number of to-be-udpated sybmols: ' + str(len(to_be_updated_foods)))

        params = []
        for food in to_be_updated_foods:
            print(food)
            params.append([food])

        print('updating starts...')
        print(query_update)
        # self.cur.executemany(query_update, params)
        seq = 1
        for param in params:
            self.cur.execute(query_update, param)
            print('   * ' + str(seq) + '. food: [' + param[0] + '] is updated')
            seq += 1
        self.connection.commit()
        print('updating foods is done')

    def close(self):
        if self.cur:
            self.cur.close()
        if self.connection:
            self.connection.close()

if __name__ == '__main__':
    api_server = ApiServerInvoker(API_SERVER.base_url, API_SERVER.keyword)
    api_server.openApi('foods')
    foods_in_api_server = api_server.getFoods()

    sql_select_food = "SELECT food FROM food WHERE expired is NULL"
    sql_update_food = "UPDATE food SET expired=trunc(SYSDATE) WHERE food=:1"
    fooddb = FoodDB(ORACLE.host, ORACLE.port, ORACLE.sid, ORACLE.username, ORACLE.password)
    fooddb.connect()
    fooddb.process(sql_select_food, sql_update_food, foods_in_api_server)
    fooddb.close()