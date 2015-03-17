from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open  # To use a consistent encoding
from os import path


# Get the long description from the relevant file
setup(
    name='remns',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.0.dev4',

    description='An elegant Python blogging engine.',
    scripts=['bin/remns'],


    # The project's main homepage.
    url='https://github.com/vchynarov/remns',

    # Author details
    author='Viktor Chynarov',
    author_email='viktor.chynarov@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
    #    'Programming Language :: Python :: 2',
    #    'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    #    'Programming Language :: Python :: 3',
    #    'Programming Language :: Python :: 3.2',
    #    'Programming Language :: Python :: 3.3',
    #    'Programming Language :: Python :: 3.4',
    ],

    # What does your project relate to?
    keywords='blog sqlalchemy werkzeug engine web framework',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=['remns'],

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        # 'Jinja2',
        # 'SQLALchemy',
        # 'Werkzeug',
        # 'PyYAML',
        # 'MarkupSafe',
        # 'markdown2',
        # 'Pygments'
    ],

    # List additional groups of dependencies here (e.g. development dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['gunicorn', 'psycopg2'],
        'test': ['nose']
    },

    package_data={
        'remns': [
            'dist/static/admin/utils.js',
            'dist/static/admin/epiceditor/preview/github.css',
            'dist/static/admin/epiceditor/preview/bartik.css',
            'dist/static/admin/epiceditor/preview/preview-dark.css',
            'dist/static/admin/epiceditor/base/epiceditor.css',
            'dist/static/admin/epiceditor/editor/epic-dark.css',
            'dist/static/admin/epiceditor/editor/epic-light.css',
            'dist/static/admin/admin.js',
            'dist/static/admin/admin.css',
            'dist/templates/admin/edit_view.html',
            'dist/templates/admin/base.html',
            'dist/templates/admin/all_posts.html',
            'dist/templates/admin/login.html'
        ]
    }
)
