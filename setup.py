from setuptools import setup, find_packages


setup(name='agent.http',
      version='0.3.1',
      description='Rackspace Monitoring agent.plugin HTTP check',
      author='Vic Watkins',
      author_email='vic.watkins@rackspace.com',
      url='https://github.com/vickleford/agent.http',
      install_requires=['requests', 'argparse', 'logging'],
      packages=find_packages(),
      py_modules=['agent_http'],
      entry_points = { 'console_scripts': [
        'agent.http = agent_http:spawn'
      ] }
     )