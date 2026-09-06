import os
import subprocess
from setuptools import setup
from setuptools.command.build_py import build_py


class BuildInvoluteCFFI(build_py):
    """Custom build step to compile the C shared library before packaging Python modules."""

    def run(self):
        c_source = os.path.join("src", "involute_wrapper.c")
        output_so = os.path.join("python", "involute", "libinvolute.so")
        include_dir = "include"

        compile_cmd = [
            "gcc",
            "-shared",
            "-fPIC",
            "-O3",
            "-march=native",
            "-flto",
            "-fopenmp",
            f"-I{include_dir}",
            c_source,
            "-lm",
            "-o",
            output_so,
        ]

        print(f"Building C shared library (Prod + OpenMP): {' '.join(compile_cmd)}")
        subprocess.check_call(compile_cmd)

        super().run()


setup(
    cmdclass={"build_py": BuildInvoluteCFFI},
)
