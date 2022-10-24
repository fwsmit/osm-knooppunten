import unittest
import tests.analyze
import tests.parser
import tests.helper

# initialize the test suite
loader = unittest.TestLoader()
suite  = unittest.TestSuite()

# add tests to the test suite
suite.addTests(loader.loadTestsFromModule(tests.analyze))
suite.addTests(loader.loadTestsFromModule(tests.parser))
suite.addTests(loader.loadTestsFromModule(tests.helper))

# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)

