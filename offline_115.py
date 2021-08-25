import argparse
import base64
import hashlib
import sys
import traceback
from collections import OrderedDict
from json.decoder import JSONDecodeError
from os import environ
from pathlib import Path
from typing import Dict, Final, List, Optional, OrderedDict, Sequence, Tuple, Union

import bencodepy
import requests
import requests.utils
from requests.cookies import RequestsCookieJar

__author__: Final[str] = 'owtotwo'
__copyright__: Final[str] = 'Copyright 2020 owtotwo'
__credits__: Final[Sequence[str]] = ['owtotwo']
__license__: Final[str] = 'LGPLv3'
__version__: Final[str] = '0.1.7'
__maintainer__: Final[str] = 'owtotwo'
__email__: Final[str] = 'owtotwo@163.com'
__status__: Final[str] = 'Experimental'

ENV_115_COOKIES_KEY: Final[str] = 'OFFLINE_115_COOKIES_PATH'
DEFAULT_COOKIES_FILE_PATH: Final[Path] = Path.home() / '.115.cookies'


class Lixian115:
    DEFAULT_COMMON_HEADERS: Final[Dict[str, str]] = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://115.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36 115Browser/9.1.1',
        'Referer': 'https://115.com/?cid=0&offset=0&mode=wangpan',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
    }
    COOKIES_SHOULD_HAVE_KEYS: Final[Sequence[str]] = ('UID', 'CID', 'SEID')

    class CookiesFileNotFound(Exception):
        def __init__(self, msg='找不到存放115cookies的文件', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    class CookiesNotVaild(Exception):
        def __init__(self, msg=f'115cookies文件不合法（分号间隔，且要有UID,CID,SEID字段）', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    class AddTasksError(Exception):
        def __init__(self, msg='添加任务出错', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    class GetUidError(Exception):
        def __init__(self, msg='获取uid时出错', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    class GetSignAndTimeError(Exception):
        def __init__(self, msg='获取sign和time值时出错', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    class LoginWithCookiesError(Exception):
        def __init__(self, msg='使用cookies检查登录状态出错（理应已登录）', *args, **kwargs) -> None:
            super().__init__(msg, *args, **kwargs)

    def __init__(self, cookies_path: Path=None) -> None:
        self.cookies_path: Path = cookies_path or DEFAULT_COOKIES_FILE_PATH
        if not self.cookies_path.is_file():
            raise self.CookiesFileNotFound
        self.session: requests.Session = requests.session()
        try:
            self.session.cookies = self.get_cookie_jar_from_file()
        except Exception as e:
            raise self.CookiesNotVaild from e
        if not self.is_cookies_valid():
            raise self.CookiesNotVaild(f'115的Cookies必须包含UID,CID,SEID字段')
        self.session.headers.update(self.DEFAULT_COMMON_HEADERS)
        self._is_login: Optional[bool] = None
        self._uid: Optional[int] = None

    # return the number of successful added tasks
    def add_tasks(self, url_or_urls: Union[str, Sequence[str]]) -> int:
        if not self.is_login():
            raise self.AddTasksError from self.LoginWithCookiesError()
        try:
            sign, time = self.get_sign_and_time()
            uid = self.get_uid()
        except Exception as e:
            raise self.AddTasksError from e
        form_data = {
            'savepath': '',
            'wp_path_id': '',
            'uid': uid,
            'sign': sign,
            'time': time,
        }
        success_tasks_count = 0
        if (isinstance(url_or_urls, tuple) or isinstance(url_or_urls, list)) and len(url_or_urls) == 1:
            url_or_urls = url_or_urls[0]
        if isinstance(url_or_urls, str):
            url: str = url_or_urls
            form_data.update({'url': url})
            print(f'Add one 115 offline task...')
            self.session.headers.update({'Host': '115.com'})
            res = self.session.post('https://115.com/web/lixian/?ct=lixian&ac=add_task_url', data=form_data)
            try:
                result = res.json()
            except JSONDecodeError as e:
                raise self.AddTasksError from e
            if result['state'] != True:
                raise self.AddTasksError(msg=f'添加单个离线任务失败: error_msg为 `{result["error_msg"]}`, state is `{result["state"]}`.')
            try:
                print(f'Succeed to Add offline task `{result["name"]}`.')
            except KeyError:
                print(f'Succeed to Add offline task.')
            success_tasks_count += 1
        else:
            urls: Sequence[str] = url_or_urls
            form_data.update({f'url[{i}]': url for i, url in enumerate(urls)})
            print(f'Add multiple 115 offline tasks...')
            self.session.headers.update({'Host': '115.com'})
            res = self.session.post('https://115.com/web/lixian/?ct=lixian&ac=add_task_urls', data=form_data) # add_task_urls instead of add_task_url
            try:
                resjson = res.json()
            except JSONDecodeError as e:
                raise self.AddTasksError from e
            if resjson['state'] != True:
                raise self.AddTasksError(msg=f'添加多个离线任务失败，返回state为{resjson["state"]}')
            results = resjson['result']
            for i, result in enumerate(results):
                if result['state'] == True:
                    try:
                        print(f'{i+1}. Succeed to Add offline task `{result["name"]}`.')
                    except KeyError:
                        print(f'{i+1}. Succeed to Add offline task.')
                    success_tasks_count += 1
                else:
                    print(f'{i+1}. Failed to Add one of offline tasks: error_msg is `{result["error_msg"]}`, url is `{result["url"]}`.')
        return success_tasks_count

    # return 115 uid
    def get_uid(self) -> int:
        if not self.is_login():
            raise self.GetUidError from self.LoginWithCookiesError()
        if self._uid is not None:
            return self._uid
        self.session.headers.update({'Host': 'my.115.com'})
        res = self.session.get('https://my.115.com/?ct=ajax&ac=get_user_aq')
        try:
            result = res.json()
        except JSONDecodeError as e:
            raise self.GetUidError from e
        if result['state'] != True or not result['data'] or not result['data']['uid']:
            raise self.GetUidError
        self._uid = result['data']['uid']
        assert (self._uid is not None)
        return self._uid

    # return (sign, time)
    def get_sign_and_time(self) -> Tuple[str, int]:
        if not self.is_login():
            raise self.GetSignAndTimeError from self.LoginWithCookiesError()
        self.session.headers.update({'Host': '115.com'})
        res = self.session.get('https://115.com/?ct=offline&ac=space')
        try:
            result = res.json()
        except JSONDecodeError as e:
            raise self.GetSignAndTimeError from e
        if result['state'] != True or not result['sign'] or not result['time']:
            raise self.GetSignAndTimeError
        return result['sign'], result['time']

    # return if is logined
    def is_login(self) -> bool:
        if self._is_login is not None:
            return self._is_login
        self.session.headers.update({'Host': 'my.115.com'})
        res = self.session.get('https://my.115.com/?ct=guide&ac=status')
        try:
            result = res.json()
        except JSONDecodeError as e:
            self._is_login = False
        else:
            self._is_login = result['state'] == True
        assert (self._is_login is not None)
        return self._is_login

    # 从cookies_path指向的文件中读取115cookies
    def get_cookie_jar_from_file(self) -> RequestsCookieJar:
        text = self.cookies_path.read_text(encoding='utf-8')
        lines: List[str] = []
        for line in text.split('\n'):
            if line.strip() == '' or line.strip().startswith('//'):
                continue
            lines.append(line)
        cookie_semicolon_string = ' '.join(lines)
        cookie_jar = self.get_cookie_jar_from_semicolon_string(cookie_semicolon_string)
        return cookie_jar

    # cookie必须包含某些字段
    def is_cookies_valid(self) -> bool:
        return all(k in self.session.cookies.iterkeys() for k in self.COOKIES_SHOULD_HAVE_KEYS)

    # 从 A=123;B=456; 类似格式的字符串中提取出cookie-jar
    @staticmethod
    def get_cookie_jar_from_semicolon_string(semi_string: str) -> RequestsCookieJar:
        cookie_dict = {}
        for kv_str in semi_string.split(';'):
            if '=' in kv_str:
                k, v = kv_str.strip().split('=')
                cookie_dict[k.strip()] = v.strip()
        cookie_jar = requests.utils.cookiejar_from_dict(cookie_dict)
        return cookie_jar


class Torrent2MagnetError(Exception):
    def __init__(self, msg='种子文件转磁力链接出错', *args, **kwargs) -> None:
        super().__init__(msg, *args, **kwargs)


# Convert torrent file to magnet url
# Inspired by: https://github.com/DanySK/torrent2magnet
def get_magnet_from_torrent_file(torrent_file: Path) -> str:
    try:
        decoded_result = bencodepy.bread(torrent_file)
    except bencodepy.BencodeDecodeError as e:
        raise Torrent2MagnetError from e
    if not isinstance(decoded_result, OrderedDict):
        raise Torrent2MagnetError(msg=f'种子文件转磁力链接出错: 期望bencodepy.bread解析出来的结果是OrderedDict，结果却是{type(decoded_result).__name__}')
    meta: OrderedDict = decoded_result
    hashcontents: bytes = bencodepy.encode(meta[b'info'])
    digest: bytes = hashlib.sha1(hashcontents).digest()
    b32hash: str = base64.b32encode(digest).decode()
    dn = meta[b'info'][b'name'].decode()
    tr = meta[b'announce'].decode()
    xl = str(meta[b'info'][b'length'])
    return f'magnet:?xt=urn:btih:{b32hash}&dn={dn}&tr={tr}&xl={xl}'


# For argparse
def get_file_path(path_string) -> Path:
    p = Path(path_string)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f'{path_string} is not a valid path for an existed file.')
    return p


# For argparse
def get_folder_path(path_string) -> Path:
    p = Path(path_string)
    if not p.is_dir():
        raise argparse.ArgumentTypeError(f'{path_string} is not a valid path for an existed folder.')
    return p


# For argparse
def get_torrent_file_path(path_string) -> Path:
    p = Path(path_string)
    if not p.is_file() or not p.suffix == '.torrent':
        raise argparse.ArgumentTypeError(f'{path_string} is not a valid torrent file path.')
    return p


# return string like '[aaa] -> [bbb] -> [ccc]'
def format_exception_chain(e: BaseException) -> str:
    # recursive function, get exception chain from __cause__
    def get_exception_chain(e: BaseException) -> List[BaseException]:
        return [e] if e.__cause__ is None else [e] + get_exception_chain(e.__cause__)

    # use Exception class name as string if no message in Exception object
    e2s = lambda e: str(e) or e.__class__.__name__
    return ''.join(f'[{e2s(exc)}]' if i == 0 else f' -> [{e2s(exc)}]' for i, exc in enumerate(reversed(get_exception_chain(e))))


# 命令行入口
def main() -> int:
    parser = argparse.ArgumentParser(description='115离线下载命令行工具（用于添加115离线下载任务）', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c',
                        '--cookies',
                        metavar='cookies',
                        type=get_file_path,
                        default=None,
                        help=f'本地115的cookies文件路径（仅支持分号间隔的cookies字符串为文本内容）\n' \
                            f'若无此值，则根据环境变量`{ENV_115_COOKIES_KEY}`查找\n' \
                            f'若无环境变量，则根据默认cookies路径`{DEFAULT_COOKIES_FILE_PATH}`查找')
    parser.add_argument('-t', '--torrent', metavar='torrent', type=get_torrent_file_path, nargs='+', help='本地种子文件')
    parser.add_argument('-m', '--magnet', metavar='magnet', type=str, nargs='+', help='磁力链接（最多15个）')
    parser.add_argument('--check', metavar='check_cookies', action='store_const', const=True, default=False, help='检查本地cookies是否能正常登陆115')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}', help='显示此命令行当前版本')
    args: argparse.Namespace = parser.parse_args()
    env_cookies_path: Optional[str] = environ.get(ENV_115_COOKIES_KEY)
    if not args.check and not args.magnet and not args.torrent:
        parser.print_help()
        return 0
    if args.cookies is not None:
        cookies_path: Path = args.cookies
    elif env_cookies_path is not None:
        cookies_path: Path = Path(env_cookies_path)
        print(f'Environment Variable `{ENV_115_COOKIES_KEY}` Found!')
    else:
        cookies_path: Path = DEFAULT_COOKIES_FILE_PATH
    print(f'115 cookies file path is {cookies_path} ...')
    if args.check == True:
        check_result: bool = False
        try:
            lx: Lixian115 = Lixian115(cookies_path=cookies_path)
            check_result = lx.is_login()
        except Lixian115.CookiesFileNotFound as e:
            print(f'115的cookies文件找不到: {format_exception_chain(e)}，可能需要创建 {DEFAULT_COOKIES_FILE_PATH} 文件并填入cookies内容')
        except Lixian115.CookiesNotVaild as e:
            print(f'115的cookies文件不合规范: {format_exception_chain(e)}')
        except Exception as e:
            print(f'检查115cookies文件时因未知原因出错: {format_exception_chain(e)}')
        if check_result == True:
            print(f'The 115 cookies are Ok!')
            return 0
        else:
            print(f'There is something wrong with the 115 cookies.')
            return 1
    urls: List[str] = []
    if args.magnet and len(args.magnet) > 0:
        urls.extend(args.magnet)
    if args.torrent and len(args.torrent) > 0:
        try:
            urls.extend(get_magnet_from_torrent_file(t) for t in args.torrent)
        except Torrent2MagnetError as e:
            print(format_exception_chain(e))
        except Exception as e:
            print(f'未知原因出错: {format_exception_chain(e)}')
            traceback.print_exc(chain=True)
    if len(urls) == 0:
        print(f'没有有效的磁力链接')
        return 1
    # 只取前面15个磁力链接
    if len(urls) > 15:
        print(f'多于15个磁力链接，仅提交前15个')
        urls = urls[:15]
    try:
        lx: Lixian115 = Lixian115(cookies_path=cookies_path)
        lx.add_tasks(urls)
    except Lixian115.CookiesFileNotFound as e:
        print(f'115的cookies文件找不到: {format_exception_chain(e)}')
    except Lixian115.CookiesNotVaild as e:
        print(f'115的cookies文件不合规范: {format_exception_chain(e)}')
    except Lixian115.AddTasksError as e:
        print(f'添加离线任务出错: {format_exception_chain(e)}')
    except Lixian115.GetUidError as e:
        print(f'获取115的UID出错: {format_exception_chain(e)}')
    except Lixian115.GetSignAndTimeError as e:
        print(f'获取115的sign与time值出错: {format_exception_chain(e)}')
    except Lixian115.LoginWithCookiesError as e:
        print(f'提供的115cookies不能成功登录: {format_exception_chain(e)}')
    except Exception as e:
        print(f'未知原因出错: {format_exception_chain(e)}')
        traceback.print_exc(chain=True)
    else:
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
