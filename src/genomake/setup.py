from setuptools import setup, find_packages

setup(
    name="genomake",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        # Your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'genomake = genomake.cli:main',  # This will point to your CLI entry point
        ],
    },
)
