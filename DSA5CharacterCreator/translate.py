def translate(what, lang="de"):
    de = dict(
        weight="Gewicht",
        title="Anrede",
        hairColor="Haarfarbe",
        height="Größe",
        culture="Kultur",
        birthDate="Geburtsdatum",
        family="Familie",
        eyeColor="Augenfarbe",
        birthLocation="Geburtsort",
        gender="Geschlecht",
        socialStatus="Sozialstatus"
    )
    langs = dict(
        de=de
    )
    return langs[lang][what]


tr = translate
