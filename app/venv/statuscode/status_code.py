# -*- coding: utf-8 -*-


statusCode              = 'statusCode'

trueCode                = 1001
http_type_post          = 1010
http_type_get           = 1011




# 1005      参数错误
parameterError          = 2005
parameter_none          = 2006

# 请求过来的key值错误
parameter_key_wrong     = 2006

# 1001      注册用户名重复
registeUsernameRepeat   = 2001



# 通过value得到的 rsa加密数据异常
valueRSAIsWrong         = 3000

# 登录请求返回为空
login_return_null       = 4000

# 注册返回失败
register_return_null    = 4001


# 意见反馈插入数据库失败
query_feedback_failure  = 700

query_userinfo_failure  = 701

# 订单
query_findorder_failure  = 702
query_findorder_id_null  = 703


# 更新积分

query_points_update_failure = 705
query_points_update_error = 706
query_points_select_success = 707
query_points_select_failure = 708
query_update_points_parameter_error = 709

# 积分转赠

# 转赠发起人查询失败
query_points_transform_sponsor_failuret = 710
# 转赠接收人用户名查询失败
query_points_transform_received_failuret = 711
query_points_transform_success = 712
query_points_transform_failuret = 713


