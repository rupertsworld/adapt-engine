from api.engine import theory

def test_scale_generation():
    scale = theory.get_scale("C", "major")
    valid_notes = [60, 64, 74, 91]
    assert all(note in scale for note in valid_notes)