import pkg_resources


# Load plugins tests
for entry in pkg_resources.iter_entry_points('pygal.test.test_maps'):
    module = entry.load()
    for k, v in module.__dict__.items():
        if k.startswith('test_'):
            globals()['test_maps_' + entry.name + '_' + k[5:]] = v
