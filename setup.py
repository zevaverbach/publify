import pathlib as pl
from setuptools import setup

setup(
    name="publify",
    version="0.1.5",
    description="A CLI for publishing sites to Netlify and assigning custom domains to them.",
    author="Zev Averbach",
    author_email="zev@averba.ch",
    description_file="README.md",
    long_description=pl.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=["publify"],
    include_package_data=True,
    install_requires=["requests"],
    python_requires=">=3.10",  # only because we're using | instead of typing.Union; otherwise >= 3.9
    url="https://github.com/zevaverbach/publify",
    entry_points={"console_scripts": ["pub=publify.publify:main"]},
)
