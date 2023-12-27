from setuptools import setup, find_packages

setup(
    name='lets_type',
    version='1.0.19',
    author='Naman Sharma',
    author_email='namansharma18899@gmail.com',
    description='A small, cool & performant typing app.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/namansharma18899/lets-type',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.7',
    include_package_data=True,
install_requires= [
    'urllib3'
]
)

