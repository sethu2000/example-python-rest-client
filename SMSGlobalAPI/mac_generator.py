import time
import hashlib
import base64
import requests
import hmac
import random
import string
import logging

# Action : calculates mac for authorization of Global service 
# Parameter : None
# Return : encrypted string mac
def mac_generator():
    try:
            apiKey = CONFIG['globalservice_apiKey']
            secretKey = CONFIG['globalservice_secretKey']
            port = 443
            extraData = ''
            method = 'POST'
            host = 'api.smsglobal.com'
            action = '/v2/sms'
            timestamp = int(time.time())
            

            # Random String
            nonce = hashlib.md5(''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(36))).hexdigest()
            raw_str = "%s\n%s\n%s\n%s\n%s\n%d\n%s\n" % (timestamp, nonce, method, action, host, port, extraData)
            hash = hmac.new(secretKey, raw_str, hashlib.sha256).digest()
            hash = base64.b64encode(hash)
            mac = "MAC id=\"%s\",ts=\"%s\",nonce=\"%s\",mac=\"%s\"" % (apiKey, timestamp, nonce, hash)
            logging.info("mac generated")
            return mac

    except Exception as e:
        logger.error(e,exc_info=True)
        
    
    
# Action : sends sms through Global service
# Parameter : recipient, message
def global_service_sms(recipient, message):
    
    try :
        mac_value = mac_generator()
        recipient = str(recipient)
        recipient = recipient.replace('+', '').replace(' ', '').replace('-', '')
        data = {"destination":recipient,"message": message}
        result = requests.post('https://api.smsglobal.com/v2/sms',data = data, headers={'Authorization':mac_value})
        return result
        
    except Exception as e:
       logging.error(e,exc_info=True)