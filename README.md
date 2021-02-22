# bili_comment_del
 致敬永远的口羊二〇一六

# 简介

一个简单的Python程序

监听指定的评论区，自动删除评论

- [x] 视频评论区
- [ ] 动态、专栏评论区

使用轮子：

- [bilibili_api](https://github.com/Passkou/bilibili_api/)

# 使用

1.`sample_config.json`：认证信息，监听名单

```json
{
    "secrect": {
        "SESSDATA": "",
        "CSRF": ""
    },
    "listen": {
        "video": "avxxxxxxxx"
    }
}
```

获取 SESSDATA 和 CSRF 后填入`BiliVerift`

`video`内填写监听的视频的`av号

配置后运行`conment_del.py`即可