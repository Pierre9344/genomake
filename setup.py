from setuptools import setup, find_packages

setup(
    name='genomake',
    packages=find_packages(),
    include_package_data=True,  # Ensures data files are included
    package_data={
        'genomake': ['pipelines/chromake/Snakefile'],  # Specify the Snakefile location here
    },
    # other configurations...
)
