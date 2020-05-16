# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arbor(CMakePackage, CudaPackage):
    """Arbor: for simulating networks of multi-compartment neurons."""

    homepage = 'https://arbor.readthedocs.io/'
    url      = 'https://github.com/arbor-sim/arbor.git'
    git      = 'https://github.com/arbor-sim/arbor.git'

    maintainers = ['bcumming', 'halfflat']

    version('master', branch='master', submodules=True)
    version('0.3',    tag='v0.3',      submodules=True)

    variant('mpi', default=True,
            description='Enable MPI support.')
    variant('vectorize', default=True,
            description=f'Enable vectorization: requires that the target '
            f'architecture supports one of AVX, AVX2, AVX512 or Neon '
            f'instrinsics.')
    variant('python', default=True,
            description='Create Python module.')
    variant('vec', default=False,
            description='Use vector intrinsics, which must be available for '
            f'target architeture.')
    variant('gpu', default='none',
            description='Enable GPU support.',
            # Wait for hip-clang compiler to be more robust before
            # explicitly supporting.
            values=('none', 'cuda'),
            multi=False)

    depends_on('cmake@3.12:', type='build')
    depends_on('mpi',         when='+mpi')
    depends_on('py-mpi4py',   when='+mpi+python', type=('build', 'link', 'run'))
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

        args.append('-DARB_ARCH={}'.format(spec.target))
        # Enable MPI support
        if spec.satisfies('+mpi'):
            args.append('-DARB_WITH_MPI=on')

        # Enable Vectorization
        if spec.satisfies('+vec'):
            args.append('-DARB_VECTORIZE=on')

        # GPU support
        gpu = spec.variants['gpu'].value
        if spec.version > Version('0.3'):
            # Later versions of Arbor enable cuda, clang-cuda and hip, enabled
            # in CMake via a multi-valued ARB_GPU option.

            # Enable clang-cuda if compiling with Clang or Cray cce
            if gpu == 'cuda':
                if spec.satisfies('%cce') or spec.satisfies('%clang'):
                    args.append('-DARB_GPU=clang-cuda')
                else:
                    args.append('-DARB_GPU=cuda')
        else:
            # v:0.3 of Arbor supported only CUDA, which was enabled in CMake
            # via a boolean ARB_WITH_GPU option.
            if gpu == 'cuda':
                args.append('-DARB_WITH_GPU=on')

        # Python support
        if spec.satisfies('+python'):
            args.append('-DARB_WITH_PYTHON=on')

        return args
