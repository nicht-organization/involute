import os
import subprocess
from setuptools import setup
from setuptools.command.build_py import build_py


class BuildInvoluteCFFI(build_py):
    """Custom build step to compile the C shared library across modular subdirectories."""

    def run(self):
        output_dir = os.path.join("python", "involute")
        output_so = os.path.join(output_dir, "libinvolute.so")
        include_dir = "include"

        os.makedirs(output_dir, exist_ok=True)

        c_sources = [
            os.path.join("src", "core", "register.c"),
            os.path.join("src", "math", "diophantine.c"),
            os.path.join("src", "math", "radical.c"),
            os.path.join("src", "stream", "mmap_stream.c"),
        ]

        compile_cmd = [
            "gcc",
            "-shared",
            "-fPIC",
            "-O3",
            "-march=native",
            "-flto",
            "-fopenmp",
            f"-I{include_dir}",
            *c_sources,
            "-lm",
            "-o",
            output_so,
        ]

        print(f"Building C shared library: {' '.join(compile_cmd)}")
        subprocess.check_call(compile_cmd)
        super().run()


setup(
    cmdclass={"build_py": BuildInvoluteCFFI},
)
