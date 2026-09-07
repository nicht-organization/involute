import os
import subprocess
from setuptools import setup
from setuptools.command.build_py import build_py

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class BuildCSharedLib(build_py):
    def run(self):
        c_sources = [
            os.path.join(BASE_DIR, "src/core/register.c"),
            os.path.join(BASE_DIR, "src/math/diophantine.c"),
            os.path.join(BASE_DIR, "src/math/radical.c"),
            os.path.join(BASE_DIR, "src/stream/mmap_stream.c"),
        ]
        include_dir = os.path.join(BASE_DIR, "include")
        
        # Ensure target destination folder exists inside the temporary build path
        pkg_dir = os.path.join(BASE_DIR, "python/involute")
        os.makedirs(pkg_dir, exist_ok=True)
        out_so = os.path.join(pkg_dir, "libinvolute.so")

        if all(os.path.exists(src) for src in c_sources):
            cmd = [
                "gcc",
                "-shared",
                "-fPIC",
                "-O3",
                "-fopenmp",
                f"-I{include_dir}",
                *c_sources,
                "-lm",
                "-o",
                out_so
            ]
            print(f"Building C shared library: {' '.join(cmd)}")
            subprocess.check_call(cmd)

        super().run()

setup(
    cmdclass={"build_py": BuildCSharedLib},
)
