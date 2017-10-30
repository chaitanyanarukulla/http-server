from setuptools import setup

setup(
    name='http-server',
    description='Build an echo server.',
    package_dir={'': 'src'},
    author='Chai Nareulla & Darren Haynes',
    author_email='dummmy-address@zoho.com',
    py_modules=[],
    install_requires=['gevent'],
    extras_require={
        'testing': ['pytest', 'pytest-cov', 'pytest-watch', 'tox'],
        'development': ['ipython']
    },
    entry_points={
        # 'console_scripts': {
        # 'http-server=http-server:main'
        # }
    }
)
