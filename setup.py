from setuptools import setup


setup(
    name="trouve_ta_pompe",
    version="0.1",
    author="Guerard Robin, Maureen Metge, Nazir Youssouf",
    packages=["trouve_ta_pompe"],
    entry_points={
        "console_scripts": [
            "trouve=trouve_ta_pompe.cli:main",
        ],
    },
)