from setuptools import setup

setup(
    name='template-writer',
    version='0.1',
    py_modules=['tw'],
    install_requires=[
        'Click',
        'Jinja2',
        'pandas'
    ],
    entry_points='''
        [console_scripts]
        tw=tw:cli
    ''',
)