# -*- coding: utf-8 -*-
#!flask/bin/python
from app import app
app.debug = False

print "run  调用了两次需要修改"

app.run(host="0.0.0.0", port=8001)
