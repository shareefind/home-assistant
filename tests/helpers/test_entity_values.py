"""Test the entity values helper."""
from homeassistant.helpers.entity_values import EntityValues as EV

ent = 'test.test'


def test_override_single_value():
    """Test values with exact match."""
    store = EV({ent: {'key': 'value'}})
    assert store.get(ent) == {'key': 'value'}
    assert len(store._cache) == 1
    assert store.get(ent) == {'key': 'value'}
    assert len(store._cache) == 1


def test_override_by_domain():
    """Test values with domain match."""
    store = EV(domain={'test': {'key': 'value'}})
    assert store.get(ent) == {'key': 'value'}


def test_override_by_glob():
    """Test values with glob match."""
    store = EV(glob={'test.?e*': {'key': 'value'}})
    assert store.get(ent) == {'key': 'value'}


def test_domain_overrules_glob():
    """Test domain overrules glob match."""
    store = EV(
        domain={'test': {'key': 'domain'}},
        glob={'test.?e*': {'key': 'glob'}})
    assert store.get(ent) == {'key': 'domain'}


def test_exact_overrules_domain():
    """Test exact overrules domain match."""
    store = EV(
        exact={'test.test': {'key': 'exact'}},
        domain={'test': {'key': 'domain'}},
        glob={'test.?e*': {'key': 'glob'}})
    assert store.get(ent) == {'key': 'exact'}


def test_merging_values():
    """Test merging glob, domain and exact configs."""
    store = EV(
        exact={'test.test': {'exact_key': 'exact'}},
        domain={'test': {'domain_key': 'domain'}},
        glob={'test.?e*': {'glob_key': 'glob'}})
    assert store.get(ent) == {
        'exact_key': 'exact',
        'domain_key': 'domain',
        'glob_key': 'glob',
    }
