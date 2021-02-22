# coding: utf-8

import json
import time
from bilibili_api import utils, video, Verify, exceptions


def get_config():
    with open('./config.json', 'r', encoding='utf-8') as f:
        return json.load(f)
    return False


def get_comment_list(config: dict, verify: utils.Verify = None):
    vid = config['listen']['video'].replace('av', '')
    comments = []
    if vid.find('BV') >= 0:
        vid = utils.bvid2aid(vid)
    try:
        comments_g = video.get_comments_g(aid=vid, verify=verify)
    except (
        exceptions.BilibiliException,
        exceptions.NetworkException,
        exceptions.NoIdException,
        exceptions.NoPermissionException
    ) as exc:
        with open('./error.log', 'w+', encoding='utf-8') as err:
            err.write(
                '{time}\t\t {error}\n'.format(
                    time=time.strftime('%Y-%m-%d', time.localtime()),
                    error=exc
                )
            )
    else:
        for c in comments_g:
            comments.append({
                'rpid': c['rpid'],
                'aid': c['oid'],
                'mid': c['member']['mid'],
                'uname': c['member']['uname'],
                'content': c['content']['message'],
                'ctime': c['ctime']
            })
    return comments


def delete_comments(comments: list, verify: utils.Verify = None):
    with open('./comments/{}-.txt'.format(time.strftime('%Y-%m-%d', time.localtime())), 'a+', encoding='utf-8') as txt:
        for c in comments:
            txt.write(
                '{time}\t {mid}\t {uname}\t\t {content}\n'.format(
                    time=time.strftime(
                        '%Y-%m-%d %H:%M:%S',
                        time.localtime(c['ctime'])
                    ),
                    mid=c['mid'],
                    uname=c['uname'],
                    content=c['content']
                )
            )
            video.del_comment(aid=c['aid'], rpid=c['rpid'], verify=verify)
        return True
    return False


def run():
    config = get_config()
    if config:
        verify = Verify(
            sessdata=config['secrect']['SESSDATA'], csrf=config['secrect']['CSRF'])
        comments = get_comment_list(config, verify)
        if len(comments) == 0:
            return False
        delete_comments(comments, verify)
        return True
    else:
        with open('./error.log', 'w+', encoding='utf-8') as err:
            err.write(
                '{time}\t\t {error}\n'.format(
                    time=time.strftime('%Y-%m-%d', time.localtime()),
                    error='配置错误，请检查config'
                )
            )
    return False


def main():
    while True:
        print(
            time.strftime(
                '%Y-%m-%d %H:%M:%S',
                time.localtime()
            ),
            run()
        )
        time.sleep(11.4514)
    input()


if __name__ == "__main__":
    main()
