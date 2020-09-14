import setuptools
from offline_115 import __version__ as offline_115_version

with open('Readme.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='Offline-115',
    version=offline_115_version,
    author='owtotwo',
    author_email='owtotwo@163.com',
    description='115网盘添加离线下载任务命令行工具',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/owtotwo/Offline-115',
    py_modules=['offline_115'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'offl115 = offline_115:main',
            'offline115 = offline_115:main',
        ],
    },
)
