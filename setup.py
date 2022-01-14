from distutils.core import setup

setup(
  name = 'wordler',
  packages = ['wordler'],
  version = '0.1',
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
    'Programming Language :: Python :: 3'
  ],
)