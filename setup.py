import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py

class BuildInvoluteCFFI(build_py):
    def run(self):
        c_source = os.path.join("src", "involute_wrapper.c")
        output_so = os.path.join("python", "involute", "libinvolute.so")
        include_dir = "include"

        compile_cmd = [
            "gcc",
            "-shared",
            "-fPIC",
            "-O3",
            "-lm",  # Link math library for pow()
            f"-I{include_dir}",
            c_source,
            "-o",
            output_so,
        ]
        print(f"Building C shared library: {' '.join(compile_cmd)}")
        subprocess.check_call(compile_cmd)
        super().run()

setup(
    name="involute",
    version="0.1.0",
    packages=find_packages(where="python"),
    package_dir={"": "python"},
    package_data={"involute": ["libinvolute.so"]},
    cmdclass={"build_py": BuildInvoluteCFFI},
)