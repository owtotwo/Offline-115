# Offline 115 (115 离线下载 python 命令行工具)

`author: owtotwo`

*可配合[extract_115_cookies_ext](https://github.com/owtotwo/extract_115_cookies_ext)项目使用*

```
usage: offl115 [-h] [-c cookies] [-t torrent [torrent ...]] [-m magnet [magnet ...]] [--check] [-v]

115离线下载命令行工具（用于添加115离线下载任务）

optional arguments:
  -h, --help            show this help message and exit
  -c cookies, --cookies cookies
                        本地115的cookies文件路径（仅支持分号间隔的cookies字符串为文本内容）
                        若无此值，则根据环境变量`OFFLINE_115_COOKIES_PATH`查找
                        若无环境变量，则根据默认cookies路径`C:\Users\AT\.115.cookies`查找
  -t torrent [torrent ...], --torrent torrent [torrent ...]
                        本地种子文件
  -m magnet [magnet ...], --magnet magnet [magnet ...]
                        磁力链接（最多15个）
  --check               检查本地cookies是否能正常登陆115
  -v, --version         显示此命令行当前版本
```


## Requirements
- Windows 10
- Python3.7+
- pip
- pypi
  + bencode.py == 4.0.0
  + requests == 2.24.0


## Before Installation
Install [extract_115_cookies_ext](https://github.com/owtotwo/extract_115_cookies_ext/releases) in 115 browser, Login and Save the 115 cookies to file 'C:\Users\<You>\.115.cookies'. (Make sure the prefix dot in `.115.cookies`)

OR, Login your 115 and Save the cookies to file 'C:\Users\<You>\.115.cookies' in format 'Semicolon separated name=value pairs' by [EditThisCookie](http://www.editthiscookie.com/).


## Install Release Binary and Run on Win10
Get the 115 cookies file as above at first.

Then,

1. Download the latest version zip file in [release](https://github.com/owtotwo/Offline-115/releases)
2. Extract zip file to your Win10 PC (e.g.: C:\Users\<You>\AppData\Local\Offline-115)
3. Add the folder path you extracted in step 2 to PATH (the Windows Environment Variable)
4. Open Powershell or CMD, run `offl115 --check` and `offl115 -m "magnet:?xt=urn:btih:<Your-magnet-url>"`


## Install by pip and Run on Win10
Get the 115 cookies file as above at first.

Then,

```
$ pip install Offline-115
$ offl115 -h
$ offl115 --check (Make sure it prints 'The 115 cookies are Ok!')
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```


## Install from source code and Run on Win10
(* Need [Git for Windows](https://git-scm.com/download/win))

Get the 115 cookies file as above at first.

Then,

```
$ git clone https://github.com/owtotwo/Offline-115.git
$ cd Offline-115
$ py -3 setup.py install
$ offl115 -h
$ offl115 --check (Make sure it prints 'The 115 cookies are Ok!')
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```

OR, just run the script:

```
$ git clone https://github.com/owtotwo/Offline-115.git
$ cd Offline-115
$ py -3 offline_115.py -h
$ py -3 offline_115.py --check (Make sure it prints 'The 115 cookies are Ok!')
$ py -3 offline_115.py -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```


## Usage

### 设定Cookies (在115浏览器中登录115后获取)
- 请在115浏览器登录后，推荐使用 [EditThisCookie](http://www.editthiscookie.com/) 插件导出 cookies 到 `{HOMEPATH}/.115.cookies` 即
可正常使用。
- Cookies 只支持分号分隔的格式(Semicolon separated name=value pairs)，如`a=1;b=2;c=3;`。
- 脚本对于115cookies路径会根据以下顺序获取：
  1. 命令行参数中-c/--cookies指定的cookies文件路径
  2. 环境变量中 `OFFLINE_115_COOKIES_PATH` 变量所指定的路径
  3. 默认路径 `{HOMEPATH}/.115.cookies` 

### Help (显示命令行使用方法)
``` bash
$ offl115 -h
```

### Check cookies (检查本地115cookies文件是否合法)

Run with default cookies path:
``` bash
$ offl115 --check
115 cookies file path is C:\Users\<You>\.115.cookies ...
The 115 cookies are Ok!
```

Run in CMD:
``` cmd
$ set OFFLINE_115_COOKIES_PATH=C:\Users\<You>\Documents\115.cookies && offl115 --check
Environment Variable `OFFLINE_115_COOKIES_PATH` Found!
115 cookies file path is C:\Users\<You>\Documents\115.cookies ...
The 115 cookies are Ok!
```

Run with option `-c` or `--cookies`:
``` bash
$ offl115 --check -c "C:\Your\New\Path\cookies.txt"
115 cookies file path is C:\Your\New\Path\cookies.txt ...
The 115 cookies are Ok!
```

### Add torrent (单个本地种子文件)
``` bash
$ offl115 -t "C:\Users\<You>\Desktop\abc.torrent"
```

### Add magnet (单个磁力链接)
``` bash
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```

### Add magnet (用其他路径的115cookies文件添加单个磁力链接)
``` bash
$ offl115 -c "C:\Your\New\Path\cookies.txt" -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```

### Add multiple torrents (多个本地种子文件)
``` bash
$ offl115 -t "C:\Users\<You>\Desktop\abc.torrent" "C:\Users\<You>\Desktop\def.torrent"
```

### Add multiple magnets (多个磁力链接)
``` bash
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a" "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88b"
```

### Help (显示命令行工具当前版本)
``` bash
$ offl115 -v
```

## Related Repo
*[coolzilj/lixian-115](https://github.com/coolzilj/lixian-115)*


## License
[LGPLv3](./License) © [owtotwo](https://github.com/owtotwo)
