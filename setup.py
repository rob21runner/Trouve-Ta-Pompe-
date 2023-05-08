from setuptools import setup


with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    print(requirements)


setup(
    name="trouve_ta_pompe",
    version="0.6.4",
    author="Guerard Robin, Maureen Metge, Nazir Youssouf",
    packages=["trouve_ta_pompe"],
    entry_points={
        "console_scripts": [
            "trouve=trouve_ta_pompe.cli:main",
        ],
    },
)