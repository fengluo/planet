from setuptools import setup, find_packages
setup(
    name='postflow',
    version='0.1.1',
    author='Shawn Xie',
    author_email='fengluo17@gmail.com',
    url="https://github.com/TryPostFlow/PostFlow",
    license="Apache Licence 2.0",
    long_description="""
    A simple, powerful publishing platform
    """,
    packages=find_packages(exclude=['tests*']),
    zip_safe=False,
    include_package_data=True,
    entry_points='''
        [console_scripts]
        postflow=postflow.commands:postflow
    ''',
    install_requires=[
        'feedparser==5.2.1', 'Flask==0.12.3', 'Flask-Storage==0.1.1',
        'Flask-Mail==0.9.1', 'Flask-OAuthlib==0.9.3', 'Flask-Principal==0.4.0',
        'Flask-Alembic==2.0.1', 'Flask-SQLAlchemy==2.1',
        'Flask-Themes2==0.1.4', 'SQLAlchemy-Utils==0.32.12', 'gevent==1.1.1',
        'gunicorn==19.6.0', 'jieba==0.38', 'Jinja2==2.11.3',
        'marshmallow==2.16.3', 'mistune==0.7.1', 'nose==1.3.7',
        'pypinyin==0.16.1', 'python-dateutil==2.6.0', 'simplejson==3.10.0',
        'Unidecode==0.4.20', 'raven==6.0.0'
    ])
