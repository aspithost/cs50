from um import count


def test_count():
    assert count("yum dum gum umm") == 0
    assert count("um test um um yum yum") == 3
    assert count("um Um UM") == 3
