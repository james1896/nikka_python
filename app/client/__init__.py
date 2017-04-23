from flask import Blueprint
client = Blueprint("client",__name__)

client_v1_0 = Blueprint("client_v1_0",__name__)
client_v1_1 = Blueprint("client_v1_1",__name__)

from . import views
from . import views_v1_0
from . import views_v1_1