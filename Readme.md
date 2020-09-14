# Offline 115 (115 离线下载 python 命令行工具)

`author: owtotwo`

```
usage: offl115 [-h] [-c cookies] [-t torrent [torrent ...]] [-m magnet [magnet ...]] [--check] [-v]

115离线下载命令行工具（用于添加115离线下载任务）

optional arguments:
  -h, --help            show this help message and exit
  -c cookies, --cookies cookies
                        本地115的cookies文件（仅支持分号间隔的cookies字符串为文本内容）
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


## Install and Run on Win10
```
$ pip install Offline-115
$ (Login your 115 and Save the cookies to file 'C:\Users\<You>\.115.cookies' in format 'Semicolon separated name=value pairs' by EditThisCookie)
$ offl115 -h
$ offl115 --check (Make sure it prints 'The 115 cookies are Ok!')
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```


## Install from source code and Run on Win10
(* Need [Git for Windows](https://git-scm.com/download/win))

```
$ (Login your 115 and Save the cookies to file 'C:\Users\<You>\.115.cookies' in format 'Semicolon separated name=value pairs' by EditThisCookie)
$ git clone https://github.com/owtotwo/Offline-115.git
$ cd Offline-115
$ py -3 setup.py install
$ offl115 -h
$ offl115 --check (Make sure it prints 'The 115 cookies are Ok!')
$ offl115 -m "magnet:?xt=urn:btih:c12fe1c06bba254a9dc9f519b335aa7c1367a88a"
```


## Usage

### Login (登录)
请在115浏览器登录后，推荐使用 [EditThisCookie](http://www.editthiscookie.com/) 插件导出 cookies 到 `{HOMEPATH}/.115.cookies` 即
可正常使用。cookies 只支持分号分隔的格式(Semicolon separated name=value pairs)，如`a=1;b=2;c=3;`。

### Help (显示命令行使用方法)
``` bash
$ offl115 -h
```

### Check cookies (检查本地115cookies文件是否合法)
``` bash
$ offl115 --check
115 cookies file path is C:\Users\<You>\.115.cookies ...
The 115 cookies are Ok!

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
