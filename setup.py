from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="trouve_ta_pompe",
    version="0.4",
    author="Guerard Robin, Maureen Metge, Nazir Youssouf",
    packages=["trouve_ta_pompe"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "trouve=trouve_ta_pompe.cli:main",
        ],
    },
)