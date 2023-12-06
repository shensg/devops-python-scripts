#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'shensg'

"""
webhook=机器人token
# 状态图
# 红色：img_v3_025s_6be37f73-896f-4b0f-950f-533decfeff9g
# 绿色：img_v3_025s_bdc4954d-e00b-4d4f-9b01-0d1eaf3d0ddg
content="**${title}**
==========
发布项目名称：${CI_PROJECT_NAME}
构建耗时：${use_time}
提交人：${GITLAB_USER_NAME}
构建编号：${CI_PIPELINE_ID}
提交信息：${CI_COMMIT_MESSAGE}
构建分支：${CI_COMMIT_REF_NAME}
构建状态：${1}...${CI_JOB_STATUS}
[查看流水线详情](${CI_PROJECT_URL}/pipelines/${CI_PIPELINE_ID})"

python notice.py "$content"

"""

import sys
import requests
import json

def notice(image, content, webhook):
    # 告警信息
    card = json.dumps({
        "config": {
            "wide_screen_mode": True
        },
        "elements": [{
            "alt": {
                "content": "",
                "tag": "plain_text"
            },
            "img_key": image,
            "tag": "img"
        },
            {
                "tag": "div",
                "text": {
                    "content": content,
                    "tag": "lark_md"
                }
            }]
    })
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/" + webhook
    body = json.dumps({"msg_type": "interactive", "card": card})
    headers = {"Content-Type": "application/json"}
    res = requests.post(url=url, data=body, headers=headers)
    print(res.text)


if __name__ == '__main__':
    notice(image=sys.argv[1], content=sys.argv[2], webhook=sys.argv[3])
