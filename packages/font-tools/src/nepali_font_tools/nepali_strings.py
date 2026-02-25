"""Curated Nepali strings for QA and specimens."""

from __future__ import annotations

TEST_STRINGS: dict[str, list[str]] = {
    "basic": [
        "क ख ग घ ङ",
        "च छ ज झ ञ",
        "ट ठ ड ढ ण",
        "त थ द ध न",
        "प फ ब भ म",
        "य र ल व श ष स ह",
    ],
    "conjuncts": [
        "क्ष ज्ञ त्र श्र द्ध ट्ट ण्ड क्त क्र स्त न्त",
        "स्त्र न्त्र ङ्क्ष क्ष्म र्त्स्न्य",
    ],
    "matras": [
        "का कि की कु कू कृ के कै को कौ कं कः कँ",
        "टा टि टी टु टू टृ टे टै टो टौ",
    ],
    "numerals": [
        "० १ २ ३ ४ ५ ६ ७ ८ ९",
    ],
    "mixed": [
        "Nepal को राजधानी Kathmandu हो।",
        "Version 2.0 मा नयाँ features छन्।",
    ],
}

PANGRAMS: list[str] = [
    "ऋषिले कँचन मुनिको धूम्रपान त्यागी सफा खाना खाए।",
    "छिटो भूरो स्यालले अल्छी कुकुरमाथि हाम फाल्यो।",
]
