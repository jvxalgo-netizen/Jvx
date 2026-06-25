from setuptools import setup, find_packages

setup(
    name="pmClient",
    version="0.1.0",
    author="Hitesh Vidhani",
    description="Paytm Money API client package",
    packages=find_packages(include=["pmClient", "pmClient.*"]),
    install_requires=[
        "requests>=2.28.0",
        "httpx~=0.23.3",
        "websocket-client~=1.5.0",
    ],
    python_requires=">=3.10",
    license="MIT",
)
