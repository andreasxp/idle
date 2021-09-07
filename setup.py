"""Install script for leprechaun."""
from setuptools import setup, find_packages

install_requires = [
    "PyGObject; platform_system=='Linux'",
    "pywin32; platform_system=='Windows'"
]

setup(
    name="idle",
    version="0.1.0",
    description="Detect system idle time",
    license="MIT",
    author="Andrey Zhukov",
    url="https://github.com/andreasxp/idle",
    install_requires=install_requires,
    packages=find_packages(include=[
        "idle",
        "idle.*"
    ])
)
