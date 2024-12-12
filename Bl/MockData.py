from typing import Dict, List

class MockData:
    CINEMA_NAME: str = "MyCinema"
    MOVIES: Dict[str, Dict[str, List[str]]] = {
        "Avatar": {
            "Theater 1": ["10:00", "14:00"],
            "Theater 2": ["18:00"],
        },
        "Titanic": {
            "Theater 1": ["12:00", "16:00"],
            "Theater 2": ["20:00"],
        },
    }
    THEATERS: Dict[str, Dict[str, int]] = {
        "Theater 1": {"rows": 5, "cols": 5},
        "Theater 2": {"rows": 4, "cols": 6},
    }
