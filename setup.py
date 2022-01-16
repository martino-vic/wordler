from distutils.core import setup
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()

setup(
  name = 'wordler',
  packages = ['wordler'],
  version = '0.1.3',
  license='MIT',
  description = 'solves the wordle word puzzle',
  author = 'Viktor Martinović',
  author_email = 'viktormartin95@hotmail.com',
  url = 'https://github.com/martino-vic/wordler',
  download_url = 'https://github.com/martino-vic/wordler/archive/refs/tags/v0.1.tar.gz',
  keywords = ['wordle', 'puzzle', 'anagram'],
  install_requires=['anagram-solver'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10'
  ],
  long_description=read('README.rst')
)