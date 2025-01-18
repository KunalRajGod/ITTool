from setuptools import setup, find_packages

setup(
    name="pc_repair_tool",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'PyQt6>=6.8.0',
        'psutil>=6.1.1',
        'bcrypt>=4.2.1',
        'speedtest-cli>=2.1.3',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive PC and Mac repair tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords="pc repair, maintenance, system tools",
    url="https://github.com/yourusername/pc_repair_tool",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        'console_scripts': [
            'pc_repair=main:main',
        ],
    },
)