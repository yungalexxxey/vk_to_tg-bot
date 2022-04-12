from yaml import safe_load

with open('config.yml', 'r') as f:
    data = safe_load(f)

CHATS_ID = data['CHATS_ID']
VKTOKEN = data['VKTOKEN']
TGTOKEN = data['TGTOKEN']
