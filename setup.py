# External Includes
import os
from setuptools import find_packages, setup

# Internal Includes
from algo_trade import __version__ as VERSION


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def load_requirements():
    return read("requirements.txt").splitlines()


setup(
    name="AlgoTrade",
    version=VERSION,
    author="Kyle McClintick",
    author_email="kyle.mcclintick@gmail.com",
    description="A set of toy python trading scripts to demonstrate fundamental metrics, concepts and pipelines",
    keywords="trading",
    url="https://github.com/kwmcclintick/trading_toys",
    packages=find_packages(exclude=["test*"]),
    long_description=(
        "A set of toy python trading scripts to demonstrate fundamental metrics, concepts and pipelines "
    ),
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Trading Industry",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Finance :: Trading",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    install_requires=load_requirements(),
)
