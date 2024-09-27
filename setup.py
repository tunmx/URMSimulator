from setuptools import setup, find_packages

setup(
    name='urm',
    version='1.0.1',
    packages=find_packages(include=['urm', 'urm.*']),
    description='Unlimited Register Machine (URM) Simulator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jingyu Yan',
    author_email='tunmxy@163.com',
    url='https://github.com/tunmx/URMSimulator',
    install_requires=[
        # Dependency list
    ],
    python_requires='>=3.7',
)
