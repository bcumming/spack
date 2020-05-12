# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor: for simulating networks of multi-compartment neurons."""

    homepage = "https://arbor.readthedocs.io/"
    url      = "https://github.com/arbor-sim/arbor.git"
    git      = "https://github.com/arbor-sim/arbor.git"

    maintainers = ['bcumming', 'halfflat']

    version('master', branch='master', submodules=True)

    variant('mpi',    default=True, description='Enable MPI support.')
    variant('cuda',   default=False, description='Enable CUDA support.')
    variant('python', default=True,  description='Create Python module.')

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi',         when='+mpi')
    depends_on('python@3.6:', when='+python')
    depends_on('cuda@9.2:',   when='+cuda')

    # The only supported compilers for Arbor are GCC and Clang.
    conflicts('%gcc@:6.1')
    conflicts('%clang@:4.0')
    # Cray compiler v9.2 and later is Clang-based.
    conflicts('%cce@:9.2')
    # These compilers are not supported.
    conflicts('%intel')
    conflicts('%xl')
    conflicts('%pgi')

    extends('python')

    def cmake_args(self):
        spec = self.spec
        args = []

        if spec.satisfies('+mpi'):
            args.append('-DARB_WITH_MPI=on')

        if spec.satisfies('+cuda'):
            args.append('-DARB_GPU=cuda')

        if spec.satisfies('+python'):
            args.append('-DARB_WITH_PYTHON=on')

        return args

