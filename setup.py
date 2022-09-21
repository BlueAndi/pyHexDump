""" Tool setup """

# MIT License
#
# Copyright (c) 2022 Andreas Merkle (web@blue-andi.de)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

################################################################################
# Imports
################################################################################
import setuptools

################################################################################
# Variables
################################################################################

README_FILE_NAME = "README.md"
LONG_DESCRIPTION = ""

################################################################################
# Classes
################################################################################

################################################################################
# Functions
################################################################################

################################################################################
# Main
################################################################################

# Use the README as long description
with open(README_FILE_NAME, "r", encoding="utf-8") as fh:
    LONG_DESCRIPTION = fh.read()

# Get __version__, __author__ and __email__
exec(open("src/pyHexDump/version.py", encoding="utf-8").read()) # pylint: disable=exec-used

setuptools.setup(
    name="pyHexDump",
    version=__version__, # type: ignore[reportUndefinedVariable] # pylint: disable=undefined-variable
    author=__author__, # type: ignore[reportUndefinedVariable] # pylint: disable=undefined-variable
    author_email=__email__, # type: ignore[reportUndefinedVariable] # pylint: disable=undefined-variable
    description="Hex dump with report functionality",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/BlueAndi/pyHexDump",
    project_urls={
        "Bug Tracker": "https://github.com/BlueAndi/pyHexDump/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"pyHexDump": "src/pyHexDump"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    include_package_data=True,
    install_requires=[
        "intelhex==2.3.0",
        "Mako==1.2.2"
    ],
    entry_points={"console_scripts": [
        "pyHexDump = pyHexDump.__main__:main",
    ]}
)
