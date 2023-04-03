import unittest
loader = unittest.TestLoader()
suite = loader.discover('.')
runner = unittest.runner.TextTestRunner(verbosity=3)
runner.run(suite)
