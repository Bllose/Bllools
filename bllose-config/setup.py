from setuptools import setup, find_packages

setup(
    name='bllose-config',
    version='0.1.0', 
    description='Configuration Management',
    author='Bllose',
    author_email='bllose2018@gmail.com',
    url='https://github.com/bllools',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.6'
)