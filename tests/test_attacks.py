from red_teaming.attacks import attacks_by_category, build_attack_library
from red_teaming.models import AttackCategory

def test_library_is_deterministic_and_unique():
    a, b = build_attack_library(), build_attack_library()
    assert [c.id for c in a] == [c.id for c in b]
    assert len({c.id for c in a}) == len(a) == 21

def test_all_categories_present():
    cats = {c.category for c in build_attack_library()}
    assert cats == set(AttackCategory)

def test_by_category_partitions_library():
    grouped = attacks_by_category(build_attack_library())
    assert sum(len(v) for v in grouped.values()) == 21
    assert len(grouped[AttackCategory.PROMPT_INJECTION]) == 5
