# -*- coding: utf-8 -*-
from apns import APNs, Frame, Payload




# def sendPushNotification(token,message,sound,badge):
#     # Send a notification
#     # token_hex = '0383c581d045e896912f621f43216bd2aa11456ab01ff32185addf190ea10af2'
#     # payload = Payload(alert="Hello World!", sound="default", badge=1)
#     # apns.gateway_server.send_notification(token_hex, payload)
#     apns = APNs(use_sandbox=True, cert_file='apns-dev-cert.pem', key_file='apns-dev-key.pem')
#     token_hex = token
#     payload = Payload(alert=message, sound=sound, badge=badge)
#     apns.gateway_server.send_notification(token_hex, payload)


#需要创建无密码的证书 实验
def sendPushNotification():
    # Send a notification
    apns = APNs(use_sandbox=True, cert_file='apns-dev-cert.pem', key_file='apns-dev-key.pem')
    token_hex = '0383c581d045e896912f621f43216bd2aa11456ab01ff32185addf190ea10af2'
    payload = Payload(alert="Hello World!", sound="default", badge=1)
    apns.gateway_server.send_notification(token_hex, payload)






