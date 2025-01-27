from setuptools import setup, find_packages

setup(
    name="bllose-market",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 依赖包列表
    ],
    author="Bllose",
    author_email="bllose2018@gmail.com",
    description="A short description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/bllose/bllools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
