import requests, uuid, time#, json, hashlib
# This is where to insert your generated API keys (http://api.telldus.com/keys)
# define keys, tokens and secrets
pubkey =    "FEHUVEW84RAFR5SP22RABURUPHAFRUNU" # Public Key
privkey =   "ZUXEVEGA9USTAZEWRETHAQUBUR69U6EF" # Private Key
token =     "8aba8385b6f65e0f7bf274e5e673f04b05d541a1e" # Token
secret =    "ecd6a7203c64ec98469df1da577eeff3" # Token Secret



lights = []
class Light:
    def __init__(self, id, position, radius, on = False, comfort = 0.05) -> None:
        '''Initiates a light with id, position and radius'''
        self.id = id
        self.radius = radius
        self.position = position
        self.on = on
        self.comfort = comfort
    
    def isOn(self) -> bool:
        return self.on

    
    def turn(self, state:str) -> None:
        # make shure state is "On" or "Off"
        if state not in ["On", "Off"]:
            raise ValueError("state must be either On or Off")

        b = True if state == "On" else False

        # return if light in correct state
        if b == self.on:
            return

        self.on = b
        localtime = time.localtime(time.time())
        timestamp = str(time.mktime(localtime))
        nonce = uuid.uuid4().hex
        oauthSignature = (privkey + "%26" + secret)
        response = requests.post(
        url="https://api.telldus.com/device/turn"+state,
        params={"id": self.id,},
        headers={"Authorization": 'OAuth oauth_consumer_key="{pubkey}",oauth_nonce="{nonce}", oauth_signature="{oauthSignature}", oauth_signature_method="PLAINTEXT",oauth_timestamp="{timestamp}", oauth_token="{token}", oauth_version="1.0"'.format(pubkey=pubkey,nonce=nonce, oauthSignature=oauthSignature, timestamp=timestamp, token=token),},
        )
        responseData = response.json()  

    def illuminate(self, pos:float) -> None:
        should_be_on = self.position - self.radius < pos + self.comfort and pos - self.comfort < self.position + self.radius
        self.turn("On" if should_be_on else "Off")

def getLightsState() -> None:
    '''Gets the state of the lights of the lights according to the tellstick'''
    localtime = time.localtime(time.time())
    timestamp = str(time.mktime(localtime))
    nonce = uuid.uuid4().hex
    oauthSignature = (privkey + "%26" + secret)
    # GET-request
    response = requests.get(
        url="https://pa-api.telldus.com/json/devices/list",
        params={"includeValues": "1",},
        headers={"Authorization": 'OAuth oauth_consumer_key="{pubkey}",oauth_nonce="{nonce}", oauth_signature="{oauthSignature}", oauth_signature_method="PLAINTEXT",oauth_timestamp="{timestamp}", oauth_token="{token}", oauth_version="1.0"'.format(pubkey=pubkey,nonce=nonce, oauthSignature=oauthSignature, timestamp=timestamp, token=token),},
        )
    responseData = response.json()
    with open("tellstick_data.txt", "w") as f:
        f.write(response.text)

    for d,l in [(d,l) for d in responseData['device'] for l in lights]:
        if d['id'] == l.id:
            l.on = d['state'] == 1

with open("lights.txt") as f:
    for line in f:
        if line[0] == "#":
            continue
        id, position, radius = line.split()
        lights.append(Light(id, float(radius), float(position)))


getLightsState()