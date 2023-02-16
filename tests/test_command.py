from kci.command.address import power


def test_power():
    assert power(1) == 1
    assert power(2) == 4
