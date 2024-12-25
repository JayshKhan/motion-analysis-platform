from setuptools import setup, find_packages

setup(
    name="motion_analysis_platform",  # Replace with your project name
    version="0.1.0",
    packages=find_packages(where="src"),  # Tell setuptools to find packages in src
    package_dir={"": "src"},  # Map the root package to the src directory
    install_requires=[
        "pygame>=2.6.1",  # Add other dependencies here
    ],
)
