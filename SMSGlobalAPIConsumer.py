#!/usr/bin/python

import SMSGlobalAPI
import logging
import sys


# Action : sends sms through Global service
# Parameter : recipient, message
def send_sms(recipient, message):
    
    response = SMSGlobalAPI.global_service_sms(recipient, message)
    if response.ok:
        logging.info("msg sent sucessfully to "+recipient+ " and the message sent is "+message )
    else:
        logging.error(response,exc_info=True)
        logging.error("msg sent unsucessfully to "+recipient+ " and the message sent is "+message,exc_info=True)

if __name__ == '__main__':
    send_sms(sys.argv[1] ,sys.argv[2])
