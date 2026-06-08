from types import SimpleNamespace

from changeme import core


def build_config(**overrides):
    config = {
        'all': False,
        'category': None,
        'contributors': False,
        'dump': False,
        'name': None,
        'protocols': 'telnet',
        'target': '127.0.0.1',
        'validate': False,
    }
    config.update(overrides)
    return SimpleNamespace(**config)


def test_load_creds_skips_unrequested_protocol_validation(caplog):
    creds = core.load_creds(build_config())

    assert creds
    assert {cred['protocol'] for cred in creds} == {'telnet'}
    assert 'Validation Error' not in caplog.text


def test_load_creds_uses_protocol_from_target_url():
    creds = core.load_creds(build_config(protocols='http', target='telnet://127.0.0.1'))

    assert creds
    assert {cred['protocol'] for cred in creds} == {'telnet'}
