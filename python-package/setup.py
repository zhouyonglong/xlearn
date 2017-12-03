# coding: utf-8
"""Setup xlearn package."""
from __future__ import absolute_import

import os
import subprocess
import shutil
import sys

from setuptools import find_packages
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.sdist import sdist

sys.path.insert(0, '.')

CURRENT_DIR = os.path.dirname(__file__)

def silent_call(cmd, raise_error=False, error_msg=''):
    try:
        with open(os.devnull, 'w') as shut_up:
            subprocess.check_output(cmd, stderr=shut_up)
            return 0
    except Exception:
        if raise_error:
            raise Exception(error_msg);
        return 1

def compile_cpp():
    
    build_path = os.path.join(CURRENT_DIR, 'build_cpp')
    if os.path.isdir(build_path):
        shutil.rmtree(build_path)
    os.makedirs(build_path)
    old_working_dir = os.getcwd()
    print(old_working_dir)
    os.chdir(build_path)
    print(os.listdir(old_working_dir))

    src_path = '../compile'
    cmake_cmd = ['cmake', src_path]
    if not os.path.isdir(src_path):
        print('current path: {}'.format(os.getcwd()))
        raise Exception('{} not exists'.format(src_path))
    if os.name == "nt":
        # Windows
        pass
    else:
        # Linux, Darwin (OS X), etc.
        silent_call(cmake_cmd, raise_error=True, error_msg='Please install CMake first')
        silent_call(["make", "-j4"], raise_error=True, 
                error_msg='An error has occurred while building xlearn library file')
        shutil.copy('lib/libxlearn.so', '../xlearn/')

    os.chdir(old_working_dir)
    

class CustomInstall(install):
    
    def run(self):

        compile_cpp();
        install.run(self)

class CustomSdist(sdist):
    
    def run(self):
        src_list = ['demo', 'gtest', 'scripts', 'src']
        for src in src_list:
            dst = 'compile/{}'.format(src)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            shutil.copytree('../{}'.format(src), dst)
        shutil.copy('../CMakeLists.txt', 'compile')
        # create empty python-package for cmake
        os.makedirs('compile/python-package')
        open('compile/python-package/CMakeLists.txt', 'w')
        sdist.run(self)


if __name__ == "__main__":
    libpath_py = os.path.join(CURRENT_DIR, 'xlearn/libpath.py')
    libpath = {'__file__': libpath_py}
    exec(compile(open(libpath_py, "rb").read(), libpath_py, 'exec'), libpath, libpath)
    
    # LIB_PATH = [os.path.relpath(libfile, CURRENT_DIR) for libfile in libpath['find_lib_path']()]
    # print("Install libxlearn from: %s" % LIB_PATH)
    
    setup(name='xlearnk',
          version=open(os.path.join(CURRENT_DIR, 'xlearn/VERSION')).read().strip(),
          description="xLearn Python Package",
          maintainer='Chao Ma',
          maintainer_email='mctt90@gmail.com',
          zip_safe=False,
          cmdclass={
              'install': CustomInstall,
              'sdist': CustomSdist,
          },
          packages=find_packages(),
          # this will use MANIFEST.in during install where we specify additional files,
          # this is the golden line
          include_package_data=True,
          # move data to MANIFEST.in
          # data_files=[('xlearn', LIB_PATH)],
          license='Apache-2.0',
          classifiers=['License :: OSI Approved :: Apache Software License'],
          url='https://github.com/aksnzhy/xlearn')
