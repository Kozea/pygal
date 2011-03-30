import samples

def pytest_generate_tests(metafunc):
	if "sample" in metafunc.funcargnames:
		for name, chart in samples.generate_samples():
			metafunc.addcall(funcargs=dict(sample=chart))

def test_sample(sample):
	res = sample.burn()
