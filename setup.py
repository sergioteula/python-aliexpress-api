import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-aliexpress-api',
    version='3.0.0',
    author='Sergio Abad',
    author_email='sergio.abad@bytelix.com',
    description='AliExpress API wrapper for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/sergioteula/python-aliexpress-api',
    packages=setuptools.find_packages(),
    install_requires=['setuptools'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
