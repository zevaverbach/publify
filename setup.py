from setuptools import setup

setup(
    name="publify",
    version="0.1.0",
    description="A CLI for publishing sites to Netlify and assigning custom domains to them.",
    author="Zev Averbach",
    author_email="zev@averba.ch",
    license="MIT",
    packages=["publify"],
    install_requires=["python-dotenv", "requests"],
    url="https://github.com/zevaverbach/publify",
    entry_points={"console_scripts": ["pub = publify.publify:main"]},
)
