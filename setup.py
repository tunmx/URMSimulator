from setuptools import setup, find_packages

setup(
    name='urm',
    version='1.1.0',
    packages=find_packages(include=['urm', 'urm.*']),
    include_package_data=True,
    description='Unlimited Register Machine (URM) Simulator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jingyu Yan',
    author_email='tunmxy@163.com',
    url='https://github.com/tunmx/URMSimulator',
    install_requires=[
        'fastapi',
        'uvicorn',
        'click',
    ],
    python_requires='>=3.7',
    zip_safe=False,
    entry_points="""
        [console_scripts]
        urm=urm.gui.cli:cli
    """,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)