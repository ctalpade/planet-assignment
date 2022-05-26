import unittest
import requests

from sqlalchemy import create_engine
from sqlalchemy import text

from constants import dburl,hostname,port

unittest.TestLoader.sortTestMethodsUsing = None


class Test(unittest.TestCase):

    '''
        1) POST Create 2 groups grp1 , grp2
        2) POST create 3 users belonging to grp1 , 2 users belonging to grp2
        3) PUT modify grp membership grp1 , add 1 new user to group , 1 existing user from grp 2 
        4) PUT modify existing user from grp1 move him to grp2
        5) DEL existing user from grp1
        6) DEL existing group grp2
    '''

    @classmethod
    def cleanDBData(cls):
        engine = create_engine(dburl, echo=False, future=True)
        with engine.connect() as conn:
            conn.execute(text('delete from usergroup'))
            conn.execute(text('delete from user'))
            conn.execute(text('delete from "group"'))
            conn.commit()

    @classmethod
    def setUpClass(cls):
        cls.cleanDBData()

    @classmethod
    def tearDownClass(cls):
        cls.cleanDBData()

    def test_01_GroupPost(self):
        api_url = f"http://{hostname}:{port}/groups"
        data = {"groupname" : "grp1"}
        response = requests.post(api_url, json=data)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 201
        print(f'status code : {respcode} resp : {resp} ')
        data = {"groupname" : "grp2"}
        response = requests.post(api_url, json=data)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 201
        print(f'status code : {respcode} resp : {resp} ')
        

    def test_02_UserPost(self):
        api_url = f"http://{hostname}:{port}/users"
        datalist = [ 
            {
            "first_name": "First1",
            "last_name": "Last1",
            "userid": "user1",
            "groups": ["grp1"]
            },
            {
            "first_name": "First2",
            "last_name": "Last2",
            "userid": "user2",
            "groups": ["grp1"]
            },
            {
            "first_name": "First3",
            "last_name": "Last3",
            "userid": "user3",
            "groups": ["grp1"]
            },
            {
            "first_name": "First4",
            "last_name": "Last4",
            "userid": "user4",
            "groups": ["grp2"]
            },
            {
            "first_name": "First5",
            "last_name": "Last5",
            "userid": "user5",
            "groups": ["grp2"]
            }
            ]
        for data in datalist:
            response = requests.post(api_url, json=data)
            resp = response.json()
            respcode = response.status_code
            assert respcode == 201
            print(f'status code : {respcode} resp : {resp} ')

    def test_03_UserGet(self):
        api_url = f"http://{hostname}:{port}/users"
        response = requests.get(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        #check 5 users are created
        assert len(resp['userlist']) == 5
        print(f'status code : {respcode} resp : {resp} ')


    def test_04_GroupPut(self):
        api_url = f"http://{hostname}:{port}/groups/grp1"
        #user6 is new and user4 is in grp2 earlier now it will also belong to grp1
        data = [
                {
                "first_name": "First6",
                "last_name": "Last6",
                "userid": "user6"
                },
                {
                "first_name": "First4",
                "last_name": "Last4",
                "userid": "user4"
                }
                
            ]
        import json
        response = requests.put(api_url,json.dumps(data))
        resp = response.json()
        respcode = response.status_code
        assert respcode == 201
        print(f'status code : {respcode} resp : {resp} ')

    def test_05_UserPut(self):
        api_url = f"http://{hostname}:{port}/users/user1"
        #user1 is in grp1 move it to grp2
        data = {
        "first_name": "First1 Modified",
        "last_name": "Last1",
        "userid": "user1",
        "groups": ["grp2"]
        }
        import json
        response = requests.put(api_url,json.dumps(data))
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        print(f'status code : {respcode} resp : {resp} ')
        
    def test_06_UserDel(self):
        api_url = f"http://{hostname}:{port}/users/user2"
        import json
        response = requests.delete(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        print(f'status code : {respcode} resp : {resp} ')

    def test_07_GroupDel(self):
        api_url = f"http://{hostname}:{port}/groups/grp1"
        import json
        response = requests.delete(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        print(f'status code : {respcode} resp : {resp} ')

    def test_08_UserGet(self):
        api_url = f"http://{hostname}:{port}/users"
        response = requests.get(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        print(f'status code : {respcode} resp : {resp} ')


    def test_09_GroupGet(self):
        api_url = f"http://{hostname}:{port}/groups"
        response = requests.get(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 200
        print(f'status code : {respcode} resp : {resp} ')

    def test_10_GroupGet(self):
        api_url = f"http://{hostname}:{port}/groups/grp1"
        response = requests.get(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 404
        print(f'status code : {respcode} resp : {resp} ')

    def test_11_GroupGet(self):
        api_url = f"http://{hostname}:{port}/users/user2"
        response = requests.get(api_url)
        resp = response.json()
        respcode = response.status_code
        assert respcode == 404
        print(f'status code : {respcode} resp : {resp} ')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()