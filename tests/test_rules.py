from app.services.rules import normalize, present_terms, ratio_score, years_experience


def test_normalize_accents():
    assert normalize("Ingeniería y comunicación") == "ingenieria y comunicacion"


def test_present_terms_avoids_partial_words():
    assert present_terms("Trabajo con JavaScript, no Java.", {"java", "javascript"}) == {"java", "javascript"}


def test_years_experience_uses_largest_value():
    assert years_experience("2 años como analista y 5 años como líder") == 5


def test_ratio_score_is_bounded():
    assert ratio_score(8, 4, 60) == 60


def test_ratio_score_handles_no_requirements():
    assert ratio_score(0, 0, 10) == 10
