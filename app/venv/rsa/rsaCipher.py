# -*- coding: utf-8 -*-
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5


# # 伪随机数生成器
# random_generator = Random.new().read
# # rsa算法生成实例
# rsa =RSA.generate(1024, random_generator)
random_generator = Random.new().read

# rsa算法生成实例
rsa =RSA.generate(1024, random_generator)

def sendGhostPublicKey():
    with open('ghost-public.pem') as f:
        key = f.read()
        return key


#生成加密密钥
def masterKeyPair():
    # master的秘钥对的生成

    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)
    master_private_pem = rsa.exportKey()

    with open('app/venv/rsa/master-private.pem', 'w') as f:
        f.write(master_private_pem)

    master_public_pem = rsa.publickey().exportKey()
    with open('app/venv/rsa/master-public.pem', 'w') as f:
        f.write(master_public_pem)

    # with open('ghost-public.pem') as f:
    #     key = f.read()
    # print 'random~~~~~:',random_generator,'rsa~~~~~~```:',rsa,key


# 生成签名密钥
def ghostKeyPair():
    # ghost的秘钥对的生成

    # # 伪随机数生成器
    # random_generator = Random.new().read
    # # rsa算法生成实例
    # rsa = RSA.generate(1024, random_generator)

    rsa = RSA.generate(1024, random_generator)
    ghost_private_pem = rsa.exportKey()
    with open('app/venv/rsa/ghost-private.pem', 'w') as f:
        f.write(ghost_private_pem)

    ghost_public_pem = rsa.publickey().exportKey()
    with open('app/venv/rsa/ghost-public.pem', 'w') as f:
        f.write(ghost_public_pem)
    print ghost_public_pem

# Ghost使用Ghost的公钥对内容进行rsa 加密
def encryptionWithString(text):

    with open('app/venv/rsa/ghost-public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        cipher_text = base64.b64encode(cipher.encrypt(text))
        print '加密 :', cipher_text
        return cipher_text


# Ghost使用自己的私钥对内容进行rsa 解密
def decryptionWithString(cipher_text,random_generator):
    with open('app/venv/rsa/ghost-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        text = cipher.decrypt(base64.b64decode(cipher_text), random_generator)
        print '解密: ', text
        return text

# Master 使用自己的公钥对内容进行解签
def signatureWithString(text):
    with open('app/venv/rsa/master-private.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        digest.update(text)
        sign = signer.sign(digest)
        signature = base64.b64encode(sign)
        print '签名 :', signature
        return signature


 # Ghost使用自己的公钥对内容进行rsa 解密
def verificationSignature(message,signature):
    with open('app/venv/rsa/master-public.pem') as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        signer = Signature_pkcs1_v1_5.new(rsakey)
        verifier = Signature_pkcs1_v1_5.new(rsakey)
        digest = SHA.new()
        # Assumes the data is base64 encoded to begin with
        digest.update(message)
        is_verify = signer.verify(digest, base64.b64decode(signature))
        print '验签 :', is_verify
        return is_verify
