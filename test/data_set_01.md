# ygo New！数据库 设计 v1

# users_admin
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_name      | varchar(32)   | not null unique                       |                  |
| password       | varchar(32)   | not null                              |                  |
| type           | int8          | not null                              | 类型             |

## users
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_name      | varchar(32)   | not null unique                       |                  |
| password       | varchar(32)   | not null                              |                  |
| question       | varchar(100)  | not null                              | 密码提示问题     |
| answer         | varchar(100)  | not null                              | 密码问题答案     |
| phone_number   | varchar(18)   | not null                              | 手机号           |
| timestamp      | int64         | not null                              | 注册时间         |

## users_ygo_ext
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_id        | int64         | not null                              | users.id         |
| status         | int64         | not null                              | 账号状态         |
| login_status   | int64         | not null                              | 登陆状态         |
| nick_name      | varchar(100)  | not null                              | 昵称             |
| sign           | varchar(100)  |                                       | 签名             |
| head_portrait  | varchar(64)   |                                       | 头像hash         |
| mark           | int32         | not null                              | 持有积分         |
| history_mark   | int32         | not null                              | 历史总积分       |
| level          | int32         | not null                              | 等级             |
| game_plays     | int32         | not null                              | 游戏场次         |
| win_game_plays | int32         | not null                              | 胜利场次         |

## users_login_history
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_id        | int64         | not null                              | users.id         |
| addr           | varchar(16)   | not null                              | 登陆地址         |
| timestamp      | int64         | not null                              | 登陆时间         |

## users_credit_history
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_id        | int64         | not null                              | users.id         |
| timestamp      | int64         | not null                              | 创建时间         |
| card_id        | varchar(32)   | not null                              | 充值卡号         |
| card_password  | int16         | not null                              | 充值密码         |
| money          | int16         | not null                              | 金额             |

## users_money
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| user_id        | int64         | not null                              | users.id         |
| history_money  | int32         | not null                              | 历史消费点数     |
| money          | int32         | not null                              | 持有点数         |
| mark_money     | int32         | not null                              | 积分兑换点数     |
| update_money   | int32         | not null                              | 更新点数         |

## users_item
| 字段                | 类型          | 约束                                  | 描述             |
| ------------------- | :-----------: | :-----------------------------------: | ---------------: |
| id                  | int64         | not null primary key identity(1,1)    |                  |
| user_id             | int64         | not null                              | users.id         |
| type                | int8          | not null                              | 类型             |
| cost_money          | int32         | not null                              | 每天变动点数     |
| cost_update_money   | int32         | not null                              | 每天变动更新点数 |

## users_friends
| 字段                | 类型          | 约束                                  | 描述             |
| ------------------- | :-----------: | :-----------------------------------: | ---------------: |
| id                  | int64         | not null primary key identity(1,1)    |                  |
| user_id             | int64         | not null                              | users.id         |
| friend_id           | int64         | not null                              | 好友id           |
| timestamp           | int64         | not null                              | 创建时间         |

## users_feedbacks
| 字段                | 类型          | 约束                                  | 描述             |
| ------------------- | :-----------: | :-----------------------------------: | ---------------: |
| id                  | int64         | not null primary key identity(1,1)    |                  |
| user_id             | int64         | not null                              | users.id         |
| message             | text          | not null                              | issue内容        |
| timestamp           | int64         | not null                              | 创建时间         |
| status              | int8          | not null                              | 状态             |
| read                | bool          | not null                              | 阅览状态         |

## update_package
| 字段                | 类型          | 约束                                  | 描述             |
| ------------------- | :-----------: | :-----------------------------------: | ---------------: |
| id                  | int64         | not null primary key identity(1,1)    |                  |
| version             | varchar(64)   | not null unique                       | 版本串           |
| version1            | int16         | not null                              | 主版本编号       |
| version2            | int16         | not null                              | 副版本编号       |
| version3            | int16         | not null                              | 测试版本号       |
| timestamp           | int64         | not null                              | 创建时间         |
| package_name        | varchar(64)   | not null                              | 存储名           |
| type                | int16         | not null                              | 类型             |

## credit_cards
| 字段           | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| timestamp      | int64         | not null                              | 创建时间         |
| timestamp2     | int64         | not null                              | 失效时间         |
| card_id        | varchar(32)   | not null unique                       | 充值卡号         |
| card_password  | int16         | not null                              | 充值密码         |
| money          | int16         | not null                              | 金额             |
| used           | bool          | not null                              | 是否已使用       |

## phone_verify_code
| 字段        	 | 类型          | 约束                                  | 描述             |
| -------------- | :-----------: | :-----------------------------------: | ---------------: |
| id             | int64         | not null primary key identity(1,1)    |                  |
| phone_number   | varchar(18)   | not null                              | 手机号           |
| verify_code    | varchar(4)    | not null                              | 验证码           |
| timestamp      | int64         | not null                              | 过期时间         |
| used           | bool          | not null                              | 是否已使用       |