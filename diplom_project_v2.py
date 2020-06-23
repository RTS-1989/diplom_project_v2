import requests
import json
from time import sleep

token = 'e0a78f977408fc69391681a9d55772ebf517ca4359298f6f82f16394ab354cfd126c2be888762e01a61ff'
user_id = 175876682
API = 'https://api.vk.com/method'


class User:

    def __init__(self, user_id: int):
        self.token = token
        self.user_id = user_id

    def get_friends(self):

        friends_list = []
        params = {
                  'access_token': self.token,
                  'user_id': self.user_id,
                  'v': 5.107,
                  'count': 25,
                  'fields': 'domain'
                  }

        response = requests.get(f'{API}/friends.get', params).json()

        for user in response['response']['items']:
            friends_list.append(user['id'])

        return friends_list

    def get_groups(self):

        groups_list = []
        params = {
                  'access_token': self.token,
                  'user_id': self.user_id,
                  'v': 5.107,
                  'extended': 1,
                  'fields': ['id', 'name', 'members_count']
                  }

        response = requests.get(f'{API}/groups.get', params).json()

        for group in response['response']['items']:
            groups_list.append({'gid': group['id'], 'name': group['name'], 'members_count': group['members_count']})

        return groups_list

    def get_group_difference(self, group_id):

        difference_list = []

        params = {
              'access_token': self.token,
              'group_id': group_id,
              'v': 5.107,
              'filter': 'friends'
              }

        response = requests.get(f'{API}/groups.getMembers', params=params).json()

        return response

user1 = User(user_id)

if __name__ == '__main__':
    with open('get_difference.json', 'w', encoding='utf-8') as fo:
        info_list = []
        for group_id in user1.get_groups():
            print('In process...')
            sleep(3)
            if user1.get_group_difference(group_id['gid'])['response']['count'] == 0:
                info_list.append(group_id)
                print(f'Группа {group_id} есть только у id{user_id}')
        json.dump(info_list, fo, ensure_ascii=False, indent=4)
