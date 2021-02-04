# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Libpulsar(CMakePackage):
    """libpulsar is a C/C++ client library implementation of the Apache Pulsar
     protocol."""

    homepage = "https://github.com/apache/pulsar"
    url      = "https://github.com/apache/pulsar/archive/v2.7.0.tar.gz"

    maintainers = ['aahmed-se']

    version('2.7.0',
            sha256='5bf8e5115075e12c848a9e4474cd47067c3200f7ff13c45f624f7383287e8e5e')

    variant('python', default=False, description='Build the Python client')

    depends_on('zstd')
    depends_on('openssl')
    depends_on('snappy')
    depends_on('boost')
    depends_on('protobuf')
    depends_on('pkg-config')
    depends_on('openssl')
    depends_on('cmake@3.14:', type='build')

    extends('python'          , when='+python')

    depends_on('boost+python' , when='+python')
    depends_on('python'       , type=('build'), when='+python')
    depends_on('py-setuptools', type=('build'), when='+python')
    depends_on('py-wheel'     , type=('build'), when='+python')

    root_cmakelists_dir = 'pulsar-client-cpp'

    def cmake_args(self):
        args = ["-DBUILD_TESTS=OFF"]
        return args

    @run_after('build')
    def build_python_whl(self):
        if '+python' in self.spec:
            with working_dir(os.path.join(self.stage.source_path, 'pulsar-client-cpp/python')):
                python = self.spec['python'].command
                python('setup.py', 'bdist_wheel')
