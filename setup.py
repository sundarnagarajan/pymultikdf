'''
    Python wrapper around curve25519 by mehdi sotoodeh.
    The files under py25519/c  are from mehdi sotoodeh and are copied
    unchanged from https://github.com/msotoodeh/curve25519.

    The files under py25519/c are licensed under the MIT LICENSE (see
    license.txt file under py25519/c).

    All remaining files in this package are licensed under the GNU
    General Public License version 3 or (at your option) any later version.

    See the file LICENSE-GPLv3.txt for details of the GNU General Public
    License version 3.

    Copyright (C) 2016  Sundar Nagarajan

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
import sys
import os
from setuptools import setup, find_packages, Extension
from distutils.util import get_platform
# import setupext ONLY if you need triggers for installation steps
import setupext


os.chdir(os.path.dirname(sys.argv[0]) or ".")

'''
==============================================================================
PACKAGE DATA
==============================================================================
'''
# You _SHOULD_ set these
name = 'multikdf'
version = '0.01.25'   # oldver: open('ver.txt', 'r').read().splitlines()[0]
url = 'https://github.com/sundarnagarajan/pymultikdf'
download_url = '%s/tree/%s' % (url, version)
description = name
install_requires = [
    'cffi_utils',
]
packages = find_packages()
license = ('License :: OSI Approved :: '
           'GNU Lesser General Public License v3 or later (LGPLv3+)'
           )

# The following are optional
try:
    long_description = open('README.rst').read()
except:
    long_description = description
author = 'Sundar Nagarajan'
# author_email = ''
maintainer = author
# maintainer_email = author_email
classifiers = [
    'Development Status :: 4 - Beta',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: PyPy',
    'License :: OSI Approved :: MIT License',
    ('License :: OSI Approved :: '
     'GNU Lesser General Public License v3 or later (LGPLv3+)'
     )
]
zip_safe = True


'''
==============================================================================
C EXTENSION DETAILS
C source files are in a directory under the python module, so that the
C files are also installed with the python module
==============================================================================
'''
c_dir = 'c'
libname = 'libmultikdf'
c_src_files = [
    'scrypt/lib/crypto/crypto_scrypt.c',
    'scrypt/libcperciva/alg/sha256.c',
    'scrypt/lib/crypto/crypto_scrypt_smix.c',
    'scrypt/libcperciva/util/insecure_memzero.c',
    'scrypt/libcperciva/util/warnp.c',
    'py-bcrypt/bcrypt/bcrypt.c',
    'py-bcrypt/bcrypt/blowfish.c',
    'py-bcrypt/bcrypt/bcrypt_pbkdf.c',
    'py-bcrypt/bcrypt/sha2.c',
    'fastpbkdf2/fastpbkdf2.c',
]
libpath = os.path.join(name, libname)
c_src_list = [os.path.join(name, c_dir, x) for x in c_src_files]
ext_modules = [
    Extension(
        name=libpath,
        sources=c_src_list,
        include_dirs=[os.path.join(name, c_dir, x) for x in [
            'scrypt',
            'scrypt/libcperciva/alg',
            'scrypt/libcperciva/cpusupport',
            'scrypt/libcperciva/util',
            'py-bcrypt/bcrypt',
            'fastpbkdf2',
        ]],
        libraries=['crypto', ],
        extra_compile_args=['-std=c99',
                            '-DCONFIG_H_FILE=\"config_freebsd.h\"',
                            ],
    )
]


'''
==============================================================================
ADDITIONAL DATA FILES
---------------------
==============================================================================
'''

data_dirs = [
    'doc',
    c_dir,
    'build',
]


'''
==============================================================================
CUSTOM STEPS
==============================================================================
'''
build_c_dir = 'build/lib.%s-%s/%s/%s' % (
    get_platform(),
    '%d.%d' % sys.version_info[:2],
    name,
    c_dir
)
build_sh = os.path.join(name, 'build/build.sh')

setupext.config['build_ext']['pre']['cmdlist'] = [
    build_sh + ' ' + build_c_dir,
]

'''
==============================================================================
ADDITIONAL keyword args to setup() - shouldn't be required, normally
==============================================================================
'''
ADDL_KWARGS = dict(
    # To support custom step triggers
    cmdclass=setupext.get_cmdclass()
)


'''
==============================================================================
           DO NOT CHANGE ANYTHING BELOW THIS
==============================================================================
'''


def get_dirtree(topdir, dirlist=[]):
    '''
    topdir-->str: must be name of a dir under current working dir
    dirlist-->list of str: must all be names of dirs under topdir
    '''
    ret = []
    curdir = os.getcwd()
    if not os.path.isdir(topdir):
        return ret
    os.chdir(topdir)
    try:
        for dirname in dirlist:
            if not os.path.isdir(dirname):
                continue
            for (d, ds, fs) in os.walk(dirname):
                for f in fs:
                    ret += [os.path.join(d, f)]
        return ret
    except:
        return ret
    finally:
        os.chdir(curdir)

# Make some keywords MANDATORY
for k in [
    'name', 'version', 'description', 'license',
]:
    if k not in locals():
        raise Exception('Missing mandatory keyword: ' + k)

# keywords that are computed from variables
dirlist = locals().get('data_dirs', None)
if isinstance(dirlist, list):
    package_dir = {name: name}
    package_data = {name: get_dirtree(topdir=name, dirlist=dirlist)}

known_keywords = [
    'name', 'version', 'packages', 'description', 'license',
    'install_requires', 'requires', 'setup_requires',
    'ext_modules', 'package_dir', 'package_data',
    'zip_safe', 'classifiers', 'keywords',
    'long_description', 'url', 'download_url',
    'author', 'author_email', 'maintainer', 'maintainer_email',
]

kwdict = {}
for k in known_keywords:
    if k in locals():
        kwdict[k] = locals()[k]

# Additional keywords specified by user - shouldn't be required, normally
kwdict.update(ADDL_KWARGS)


setup(**kwdict)
