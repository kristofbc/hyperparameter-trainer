from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='hyperparameter-trainer',
    version='1.0.0',
    description='Try different hyperparameters for a neural network, easily.',
    long_description=long_description,
    url='https://github.jp.honda-ri.com/kcharbonneau/chainer-hyperparameter-trainer',
    license='MIT',
    author='Kristof Boucher Charbonneau',
    author_email='k.charbonneau@jp.honda-ri.com',
    packages=['trainer'],
    entry_points={ },
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ],
)
