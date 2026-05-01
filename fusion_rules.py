
from itertools import combinations #generate all combinations of symbols

FUSION_RULES = {

    # 5 SYMBOL COMBINATIONS

    frozenset(["ank", "eye", "feather", "scale", "pot"]):
        "the complete rite of Ma'at: life weighed against truth, the offering witnessed "
        "and protected by the divine eye, culminating in eternal judgment and sacred nourishment",

    frozenset(["ank", "boat", "star", "water", "feather"]):
        "the full solar journey of the soul: life carried across the celestial ocean beneath "
        "the guiding stars, judged by Ma'at's feather, ascending to eternal solar existence",

    frozenset(["beetle", "ank", "star", "water", "sunrise"]):
        "Khepri's total resurrection cycle: the scarab pushes the sun from primordial waters "
        "beneath the stars at dawn, life is reborn, and the soul ascends to its imperishable stellar home",

    frozenset(["ank", "eye", "feather", "grain", "water"]):
        "Osiris fully manifest: everlasting life nourished by grain and the sacred Nile, protected "
        "by the divine eye and weighed by truth's feather in the eternal cycle of resurrection",

    frozenset(["cobra_kai", "ank", "eye", "feather", "scale"]):
        "total divine sovereignty over judgment: the royal uraeus guards eternal life as Horus's eye "
        "witnesses the heart weighed by Ma'at's feather upon the scales of cosmic truth",

    frozenset(["boat", "ank", "star", "water", "triangle"]):
        "the soul's complete passage to the pyramid of stars: the barque sails the celestial waters "
        "bearing the ankh, guided by the imperishable stars toward the triangular gateway of eternity",

    frozenset(["ank", "feather", "eye", "scale", "dog"]):
        "the hall of two truths fully assembled: Anubis presides as eternal life stands before the "
        "scale, truth's feather descends, and the divine eye bears witness to every judgment",

    frozenset(["grain", "water", "ank", "sunrise", "egg"]):
        "primordial creation in full bloom: the sun rises from the Nile's waters as the primordial "
        "egg opens to germinate the grain of life — the complete act of divine genesis at dawn",

    frozenset(["snake", "ank", "star", "water", "feather"]):
        "the night cycle of cosmic regeneration: the serpent of the underworld traverses the "
        "stellar waters, renewing the gift of life through sacred nocturnal rites weighed by truth",

    frozenset(["ank", "eye", "cobra_kai", "triangle", "feather"]):
        "the divine triad of protection over the pyramid: eternal life guarded by the uraeus, "
        "witnessed by the eye of Horus, and sanctioned by Ma'at's feather atop the sacred triangle",

    frozenset(["beetle", "sunrise", "water", "egg", "ank"]):
        "the dawn of creation: Khepri rises from the primordial waters at sunrise as the cosmic "
        "egg cracks open, pouring the first breath of life — the ankh seals the eternal covenant",

    frozenset(["bird", "ank", "star", "feather", "water"]):
        "the ba soul's complete celestial passage: the spirit bird soars over sacred waters toward "
        "the imperishable stars, carrying the ankh and weighed worthy by Ma'at's feather",

    frozenset(["dog", "scale", "feather", "ank", "eye"]):
        "the weighing ceremony complete: Anubis steadies the scales, Ma'at's feather descends, "
        "the eye of Horus witnesses, and the soul bearing the ankh is declared worthy of eternal life",

    frozenset(["cobra_kai", "ank", "eye", "sunrise", "water"]):
        "the solar pharaoh's dominion at dawn: the uraeus rears as Ra rises from the sacred Nile, "
        "the eye watches all that is reborn, and the ankh seals the eternal life of the living god",

    frozenset(["grain", "water", "boat", "ank", "star"]):
        "the Osirian flood voyage: grain-laden waters carry the sacred barque bearing the ankh "
        "toward the imperishable stars — the full Nile cycle as a journey to eternal abundance",

    frozenset(["egg", "snake", "water", "sunrise", "ank"]):
        "creation from the primordial deep: the cosmic egg rests upon the waters, the serpent "
        "encircles it, and at sunrise the ankh of life bursts forth — the first sacred morning",

    frozenset(["person", "ank", "feather", "scale", "eye"]):
        "the mortal soul before the divine tribunal: a person stands bearing the ankh as the "
        "feather of Ma'at descends upon the scale and the all-seeing eye renders its verdict",

    frozenset(["triangle", "star", "ank", "sunrise", "boat"]):
        "the pyramid as a cosmic machine of rebirth: its apex aligned with the stars receives "
        "the ascending soul carried in the barque at sunrise, the ankh confirming eternal life",

    frozenset(["bird", "egg", "moon", "table", "arms_up"]):
        "the ba soul glorified at the altar of creation: worshippers raise their arms in the "
        "gesture of divine praise as the bird of the spirit hovers above the sacred offering "
        "table beside the primordial egg, while the moon of Thoth bears witness to the rite",

    frozenset(["cobra_kai", "mace", "ank", "eye", "feather"]):
        "the pharaoh's divine authority over life and judgment: the uraeus and mace proclaim "
        "royal power, the ankh grants life, and the eye with Ma'at's feather ensure all is just",

    # =========================================================================
    # 4-SYMBOL COMBINATIONS
    # =========================================================================

    frozenset(["ank", "eye", "feather", "scale"]):
        "the weighing of the heart ceremony: life, divine sight, Ma'at's feather, and the "
        "scales of justice unite in the supreme moment of judgment in the hall of two truths",

    frozenset(["ank", "boat", "star", "water"]):
        "the journey of the soul across the celestial Nile: life is carried upon sacred waters "
        "toward the imperishable stars in the eternal voyage of the deceased",

    frozenset(["beetle", "sunrise", "ank", "water"]):
        "Khepri's dawn rebirth from the primordial waters: the scarab rolls the sun into the sky "
        "at sunrise, reanimating life and declaring the triumph of light and resurrection over darkness",

    frozenset(["ank", "eye", "feather", "grain"]):
        "Osiris resurrected and nourished: eternal life stands witnessed by the divine eye, "
        "measured by truth's feather, and sustained by the grain of the resurrected grain god",

    frozenset(["cobra_kai", "ank", "eye", "feather"]):
        "the complete divine protection of life: the ankh grants immortality, the uraeus "
        "strikes down enemies, the eye watches over the soul, and Ma'at ensures perfect truth",

    frozenset(["grain", "water", "ank", "sunrise"]):
        "the full cycle of agricultural resurrection: the sun's rays, the Nile's water, and "
        "the grain of Osiris together sustain and perpetually renew the gift of eternal life",

    frozenset(["eye", "feather", "scale", "pot"]):
        "divine judgment accompanied by sacred offering: all deeds are seen, truth is weighed, "
        "and nourishment is given — the complete moral economy of the Egyptian afterlife",

    frozenset(["ank", "snake", "feather", "star"]):
        "nocturnal regeneration judged by truth: the serpent of the night renews life beneath "
        "the imperishable stars as Ma'at's feather confirms the worthiness of the soul",

    frozenset(["boat", "water", "triangle", "star"]):
        "the barque navigating the celestial Nile toward the pyramid of stars: the sacred vessel "
        "crosses the divine waters, the triangular summit pointing the soul toward eternity",

    frozenset(["bird", "egg", "moon", "arms_up"]):
        "the ba soul celebrated at the moment of creation: the bird of the spirit soars beneath "
        "the sacred lunar sky while worshippers raise their arms in ecstatic praise beside the "
        "primordial egg — the soul is declared coeval with the first divine act of existence",

    frozenset(["bird", "egg", "moon", "table"]):
        "the ba soul's nocturnal offering rite: the bird of the spirit descends to the sacred "
        "altar by moonlight while the primordial egg declares the scene a rite of cosmic "
        "rebirth — the moon of Thoth oversees this mystery of soul, nourishment, and renewal",

    frozenset(["bird", "arms_up", "table", "egg"]):
        "devout worship of the creative soul: arms raised to heaven in the ka gesture of praise "
        "before the sacred altar, the ba bird honoured above the primordial egg of creation",

    frozenset(["ank", "eye", "cobra_kai", "triangle"]):
        "the pyramid under divine protection: the ankh of life, the all-seeing eye, and the "
        "royal uraeus converge to guard the triangular gateway of royal resurrection",

    frozenset(["grain", "water", "boat", "ank"]):
        "the Osirian flood barque: grain-laden waters carry the sacred vessel bearing the ankh "
        "— the Nile flood as the living body of Osiris delivering abundance and eternal life",

    frozenset(["dog", "scale", "feather", "ank"]):
        "Anubis presides over the weighing of the heart: the divine jackal steadies the scale "
        "as Ma'at's feather tests the soul, and the ankh awaits the one found truly worthy",

    frozenset(["triangle", "star", "ank", "sunrise"]):
        "the pyramid aligned with the imperishable stars at dawn: the triangular tomb channels "
        "the first light of Ra, and the soul bearing the ankh ascends to eternal stellar life",

    frozenset(["beetle", "egg", "water", "sunrise"]):
        "Khepri born from the cosmic egg at dawn: the scarab of self-creation rises from the "
        "primordial waters as the sun breaks over the horizon, the world's first morning",

    frozenset(["cobra_kai", "mace", "ank", "eye"]):
        "the warrior-king's divine mandate: the uraeus and mace proclaim royal power in battle, "
        "while the ankh and the all-seeing eye confirm that sovereignty flows from the gods",

    frozenset(["person", "ank", "feather", "scale"]):
        "the mortal soul at the moment of judgment: a person stands bearing the ankh of life "
        "as Ma'at's feather is placed upon the scale to determine their eternal destiny",

    frozenset(["egg", "snake", "water", "sunrise"]):
        "the primal dawn of creation: the cosmic egg rests upon the primordial waters, the "
        "serpent encircles it in protection, and at sunrise the first life bursts into being",

    frozenset(["bird", "ank", "star", "feather"]):
        "the ba soul's judgment and ascension: the spirit bird carries the ankh as it rises "
        "toward the imperishable stars, found worthy by the feather of Ma'at in its flight",

    frozenset(["table", "pot", "grain", "water"]):
        "the full offering rite of abundance: the altar is laden with the sacred vessel, "
        "grain of Osiris, and Nile water — the complete ritual banquet laid before the gods",

    frozenset(["sunrise", "water", "ank", "star"]):
        "the eternal return of the sun over the sacred Nile: Ra rises from the waters at dawn, "
        "the stars fade into the light, and the ankh confirms that life is reborn each morning",

    frozenset(["mansion", "ank", "eye", "feather"]):
        "the divine temple of truth and eternal life: the god's sacred dwelling is protected "
        "by the eye of Horus, the ankh of immortality, and the feather of Ma'at's perfect justice",

    frozenset(["triangle", "ank", "star", "feather"]):
        "the pyramid as the seat of stellar judgment: its apex points to the stars where the "
        "feather of Ma'at awaits the soul bearing the ankh, ascending to eternal celestial life",

    frozenset(["snake", "water", "egg", "moon"]):
        "the nocturnal mystery of creation: the serpent moves through the dark waters beneath "
        "the moon's sacred light, encircling the cosmic egg — the world renewed in silence",

    frozenset(["arms_up", "table", "pot", "grain"]):
        "the complete offering ceremony: arms raised in the ka gesture of divine praise before "
        "the altar laden with the ritual vessel and grain — the fullness of devotion made manifest",

    frozenset(["cobra_kai", "sunrise", "ank", "water"]):
        "the solar pharaoh at dawn: the uraeus rears as Ra rises from the sacred Nile and the "
        "ankh confirms that the living god's power is renewed with each sacred morning",

    frozenset(["person", "arms_up", "table", "feather"]):
        "the worshipper's offering found worthy by truth: a person raises their arms in praise "
        "at the sacred altar, and Ma'at's feather confirms the purity of their devotion",

    frozenset(["bird", "moon", "star", "water"]):
        "the ba soul's nocturnal voyage over the sacred waters: the spirit bird flies by moonlight "
        "guided by the imperishable stars across the dark celestial Nile of the underworld",

    frozenset(["mace", "cobra_kai", "triangle", "ank"]):
        "the pharaoh's total dominion over death: the royal mace and uraeus proclaim sovereign "
        "power, the pyramid receives the deceased king, and the ankh seals his eternal life",

    frozenset(["grain", "egg", "water", "sunrise"]):
        "the complete act of divine nourishment at creation: at dawn the waters recede to reveal "
        "the egg and the grain, all born from the sun's first light upon the fertile Nile flood",

    frozenset(["hook", "whip", "ank", "feather"]):
        "the crook and flail of Osiris united with truth: the shepherd's hook and the royal "
        "flail proclaim divine authority, the ankh grants life, and the feather measures all deeds",

    frozenset(["spiral", "water", "star", "ank"]):
        "the eternal cycle of the cosmos: the spiral of infinite time, the cosmic waters, and "
        "the imperishable stars converge as the ankh confirms that life spirals on without end",

    frozenset(["drop", "water", "ank", "eye"]):
        "the tears of Isis and the gift of the Nile: the sacred drop falls into the divine "
        "waters, the ankh rises from the flood, and the eye of Horus watches over all who are "
        "purified and renewed by the sacred inundation",

    frozenset(["fathead_plant", "water", "ank", "sunrise"]):
        "the lotus rising from the waters at dawn: the sacred plant of rebirth emerges from "
        "the Nile as Ra rises, the ankh of life confirming that beauty and existence are reborn "
        "together at the first light of each new sacred morning",

    frozenset(["horns", "ank", "feather", "eye"]):
        "Hathor crowned with the horns of divine power: the goddess's authority is sealed by "
        "the ankh of eternal life, observed by the divine eye, and balanced by the feather of truth",

    frozenset(["mansion", "tower", "ank", "eye"]):
        "the sacred precinct of the divine temple: the great pylon gateway opens to the god's "
        "mansion, the ankh of life presides within, and the eye of Horus guards every threshold",

    # =========================================================================
    # 3-SYMBOL COMBINATIONS
    # =========================================================================

    frozenset(["ank", "pot", "eye"]):
        "sacred ritual protected by divine power: life is nourished through ritual offering "
        "while the all-seeing eye of Horus guards the ceremony from all that is impure",

    frozenset(["ank", "eye", "feather"]):
        "life, truth, and divine sight in harmony: the soul carries the ankh of immortality, "
        "acts with the truth of Ma'at's feather, and is watched over by the eye of Horus",

    frozenset(["ank", "eye", "beetle"]):
        "the life-bearing eye of resurrection: the ankh and the eye of Horus unite with "
        "Khepri's scarab power, declaring a protected rebirth in which life is renewed and "
        "guided by divine sight",

    frozenset(["eye", "beetle", "sunrise"]):
        "the witnessed dawn rebirth: the eye beholds Khepri at sunrise as the scarab rolls "
        "the solar disk into day, making renewal visible, protected, and ritually affirmed",

    frozenset(["ank", "eye", "beetle", "sunrise"]):
        "the complete solar revival of life: at dawn the scarab manifests rebirth, the eye "
        "watches over the transformation, and the ankh seals the scene as enduring immortal life",

    frozenset(["boat", "ank", "sunrise"]):
        "journey to eternal life with the rising sun: the sacred barque carries the soul across "
        "the celestial waters, guided by Ra's dawn light into immortality beyond the horizon",

    frozenset(["beetle", "sunrise", "ank"]):
        "Khepri's resurrection at dawn: the scarab god rolls the sun into the sky at sunrise, "
        "and life is reborn — the eternal cycle of death defeated and existence renewed",

    frozenset(["ank", "feather", "scale"]):
        "the weighing of the heart: eternal life hangs in balance as the feather of Ma'at "
        "is placed opposite the heart on the divine scales of judgment",

    frozenset(["eye", "cobra_kai", "feather"]):
        "divine vigilance and royal justice: the all-seeing eye, the striking uraeus, and the "
        "feather of Ma'at combine to ensure that no evil escapes sight, strike, or divine truth",

    frozenset(["grain", "water", "ank"]):
        "the trinity of sustenance and life: Nile waters feed the grain of Osiris whose "
        "resurrection perpetually renews the gift of eternal life for all living things",

    frozenset(["eye", "ank", "triangle"]):
        "the all-seeing pyramid of eternal life: the eye of Horus watches from the apex of "
        "the sacred triangle, and the ankh confirms that the pyramid grants immortality",

    frozenset(["boat", "water", "star"]):
        "the night voyage of the dead: the barque sails the dark underworld waters navigating "
        "by the light of the imperishable stars toward the realm of the blessed dead",

    frozenset(["star", "ank", "sunrise"]):
        "the stellar and solar union of immortality: Ra's rising sun and the imperishable stars "
        "together guarantee that the bearer of the ankh shall never truly die",

    frozenset(["feather", "scale", "eye"]):
        "the judgment of souls fully witnessed: Ma'at's feather rests on the scale of "
        "perfect justice while the divine eye records each soul's moral truth without mercy",

    frozenset(["cobra_kai", "feather", "ank"]):
        "the royal path to immortality: the uraeus guards the bearer, Ma'at's feather "
        "confirms purity, and the ankh seals the covenant of eternal life with the gods",

    frozenset(["triangle", "sunrise", "ank"]):
        "the pyramid's solar promise: the triangular form channels the sun's resurrection "
        "power at dawn to guarantee the ankh-bearer's eternal survival beyond death",

    frozenset(["dog", "ank", "scale"]):
        "Anubis presides over judgment: the divine jackal weighs the heart on the scales "
        "of Ma'at to determine whether the soul shall receive the gift of eternal life",

    frozenset(["snake", "egg", "sunrise"]):
        "primordial creation through serpentine power: the cosmic serpent encircles the "
        "primordial egg from which the sun is born at dawn — the first moment of divine creation",

    frozenset(["grain", "water", "sunrise"]):
        "the annual Nile flood blessing: Ra's sun warms the flood waters that deposit the "
        "fertile silt from which the sacred grain of Osiris rises to feed all of Egypt",

    frozenset(["eye", "pot", "feather"]):
        "the divine offering seen and judged: ritual libations are poured before the divine "
        "eye that oversees all, and Ma'at's feather confirms the purity of the intent",

    frozenset(["ank", "star", "triangle"]):
        "the pyramid pointing to stellar immortality: the triangular sacred form aligns with "
        "the circumpolar stars, and the ankh confirms the soul's eternal celestial destination",

    frozenset(["boat", "star", "sunrise"]):
        "Ra's celestial navigation from night to dawn: the solar barque steers by the fixed "
        "stars across the sky ocean, completing the full circuit from darkness into sacred light",

    frozenset(["cross", "circle", "ank"]):
        "sacred geometry of eternal life: the cross marks the four quarters of creation, "
        "the circle completes the solar whole, and the ankh unites them in immortal purpose",

    frozenset(["ank", "grain", "pot"]):
        "the offering of life's abundance: grain and sacred vessel together present the "
        "fullness of earthly nourishment as a divine gift sustaining the river of eternal life",

    frozenset(["beetle", "ank", "water"]):
        "Khepri reborn from the primordial waters: the scarab emerges from Nun carrying "
        "the ankh of life, re-enacting creation's first moment at every sacred dawn",

    frozenset(["hand", "mouth", "ank"]):
        "divine creation through speech and action: the hands of Ptah craft the world, "
        "the mouth utters Hu's creative word, and the ankh seals each act with eternal life",

    frozenset(["egg", "sunrise", "ank"]):
        "the primordial solar birth: from the cosmic egg the sun god emerges at dawn carrying "
        "the ankh of life, the supreme creative act that initiated all existence",

    frozenset(["star", "water", "boat"]):
        "the nocturnal sacred Nile: stars illuminate the dark celestial waters "
        "through which the dead sail, guided by the heavens' own silver light toward paradise",

    frozenset(["ank", "snake", "water"]):
        "life renewed through the serpent and the sacred waters: the cobra of regeneration "
        "moves through the Nile's flow, renewing existence and purifying all it touches",

    frozenset(["sunrise", "cobra_kai", "ank"]):
        "the winged solar disk of Horus Behedety: the supreme royal emblem — sun rising "
        "with the uraeus fused into one symbol of absolute pharaonic celestial dominion",

    frozenset(["ank", "moon", "eye", "water"]):
        "the full lunar rite of life and protection: moon-ordered waters, Horus's eye, and "
        "the ankh combine to express healing renewal governed by sacred celestial timing",

    frozenset(["boat", "moon", "star", "water"]):
        "the complete nocturnal voyage: the barque crosses sacred waters beneath moon and "
        "imperishable stars, depicting guided transition through the celestial underworld",

    frozenset(["person", "eye", "ank", "feather"]):
        "the mortal before the covenant of life and truth: a person is witnessed by the "
        "divine eye, measured by Ma'at's feather, and blessed with the ankh of eternal destiny",

    frozenset(["table", "pot", "water", "ank"]):
        "the life-sealed offering liturgy: altar, ritual vessel, and sacred water culminate "
        "in the ankh, transforming material offering into an immortal divine exchange",

    frozenset(["mansion", "tower", "eye", "sunrise"]):
        "the temple complex at first light: mansion and pylon awaken at dawn under the "
        "divine eye, portraying sacred architecture as a living instrument of solar worship",


    frozenset(["bird", "egg", "moon"]):
        "the soul's journey through creation's night: the ba bird flies beneath the sacred "
        "moonlight past the primordial egg — the first act of divine existence witnessed "
        "by the soul itself, which is reborn with each turn of the sacred lunar cycle",

    frozenset(["bird", "arms_up", "table"]):
        "the ba soul receives worship at the offering altar: arms raised in the ka gesture "
        "of praise, the living celebrate the bird of the spirit as it descends to the sacred "
        "table to accept divine nourishment — the ba honoured between the worlds",

    frozenset(["bird", "egg", "arms_up"]):
        "praise of the creative soul: worshippers raise their arms toward the ba bird "
        "hovering above the primordial egg — ecstatic devotion at the moment of divine "
        "spiritual genesis, the soul acclaimed as a participant in the first creation",

    frozenset(["bird", "moon", "table"]):
        "the ba soul nourished under Thoth's moon: the bird of the spirit descends to the "
        "sacred offering table by moonlight — the divine scribe Thoth records the rite "
        "as the ba accepts nourishment for its passage through the lunar underworld",

    frozenset(["brush", "bird", "feather"]):
        "the ba soul inscribed in truth: the sacred brush records the flight of the spirit "
        "bird while Ma'at's feather confirms the writing as righteous, preserving the soul's "
        "story as a divine testimony",

    frozenset(["egg", "moon", "table"]):
        "the primordial altar under the moon: the cosmic egg of creation presides over the "
        "sacred offering table beneath Thoth's lunar gaze — earthly nourishment transformed "
        "into the substance of creation itself in a rite of cosmic genesis and renewal",

    frozenset(["arms_up", "table", "egg"]):
        "praise at the moment of creation: arms raised in the ka gesture before the "
        "primordial egg over the altar — worshippers celebrate the very first divine act, "
        "honouring the eternal mystery of existence arising from the sacred void",

    frozenset(["dog", "pot", "feather"]):
        "Anubis receives the offering judged by truth: ritual vessels are presented to the "
        "jackal god as Ma'at's feather confirms the purity of the gift and its offerer",

    frozenset(["mace", "cobra_kai", "ank"]):
        "the pharaoh's sacred power of life and sovereignty: the royal mace strikes down "
        "enemies, the uraeus repels evil, and the ankh confirms the king's divine immortality",

    frozenset(["triangle", "star", "boat"]):
        "the pyramid aligned with the stars and the barque: the sacred triangular tomb "
        "points to the circumpolar stars as the night barque carries the soul to their realm",

    frozenset(["person", "ank", "feather"]):
        "the mortal who has earned eternal life: a person bearing the ankh is declared worthy "
        "by Ma'at's feather — the ultimate gift of immortality granted to the righteous",

    frozenset(["snake", "moon", "water"]):
        "the serpent in the sacred lunar waters of the underworld: the cobra of regeneration "
        "moves through the dark Nile beneath the moon, renewing the world in nocturnal silence",

    frozenset(["horns", "ank", "eye"]):
        "Hathor and Horus in divine union: the horned goddess's creative power, the ankh of "
        "eternal life, and the all-seeing eye of her son combine in total divine protection",

    frozenset(["fathead_plant", "water", "ank"]):
        "the lotus of rebirth rising from the sacred Nile: the plant of resurrection emerges "
        "from the purifying waters, and the ankh confirms that beauty and life are forever reborn",

    frozenset(["sunrise", "water", "ank"]):
        "the sun rising from the primordial Nile: Ra emerges from the sacred waters at dawn, "
        "the ankh of life rising with him as existence is renewed at the first light of day",

    frozenset(["spiral", "ank", "star"]):
        "the eternal spiral of stellar immortality: the infinite cycle of time described by "
        "the spiral carries the soul bearing the ankh upward to the imperishable stars",

    frozenset(["drop", "water", "ank"]):
        "the tears of Isis and the gift of life: the sacred drop falls into the Nile's "
        "flood waters, and the ankh of life rises from the inundation, purified and renewed",

    frozenset(["mansion", "ank", "eye"]):
        "the divine temple of eternal life: the god's sacred dwelling is guarded by the eye "
        "of Horus and blessed with the ankh — a sacred precinct where immortality dwells",

    frozenset(["tower", "ank", "eye"]):
        "the sacred pylon gateway to immortal life: the temple tower marks the threshold "
        "between mortal and divine worlds, guarded by the eye and sealed with the ankh of life",

    frozenset(["hook", "whip", "ank"]):
        "the crook and flail of Osiris: the shepherd's hook and the royal flail proclaim "
        "divine authority over the living and the dead, the ankh confirming eternal sovereignty",

    frozenset(["claw", "cobra_kai", "ank"]):
        "the fiercest divine protection of life: the predatory claw strikes, the uraeus "
        "repels, and the ankh guards the soul — an impenetrable triad of divine defence",

    frozenset(["garden", "water", "ank"]):
        "the Field of Reeds watered by eternal life: the paradise of Aaru is irrigated by "
        "the sacred Nile as the ankh confirms that the worthy dead dwell in perpetual abundance",

    frozenset(["branch", "water", "ank"]):
        "new life fed by sacred waters: the living branch of growth is nourished by the "
        "Nile's flood, and the ankh seals the covenant that life renews itself perpetually",

    frozenset(["stacked_lines", "feather", "scale"]):
        "divine measurement and cosmic truth: the layered horizons of ordered reality are "
        "weighed against Ma'at's feather on the sacred scale — the cosmic ledger of all deeds",

    frozenset(["person", "arms_up", "ank"]):
        "a worshipper consecrated by eternal life: a person raises their arms in the ka "
        "gesture of divine praise, and the ankh descends to confirm their immortal blessing",

    frozenset(["sunrise", "triangle", "star"]):
        "the pyramid aligned with dawn and stars: the sacred triangular form catches the "
        "first rays of Ra at sunrise while its apex points to the circumpolar stars of eternity",

    frozenset(["cow", "ank", "eye"]):
        "Hathor, the divine mother, bestows life under the divine gaze: the celestial cow "
        "nurtures all with her milk, the ankh flows from her divine grace, and the eye of "
        "Horus watches over every soul she shelters beneath her star-speckled wings",

    frozenset(["horns", "feather", "ank"]):
        "Hathor and Ma'at in the service of eternal life: the horns of divine authority, "
        "the feather of cosmic truth, and the ankh of immortality form a trinity of the "
        "divine feminine principles that govern both earthly abundance and the afterlife",

    frozenset(["drop", "fathead_plant", "water"]):
        "the Nile in its most fertile form: the sacred drop of Isis's tears waters the "
        "lotus of rebirth, and the Nile's flood confirms that beauty and life perpetually "
        "arise from mourning, death, and the transformative power of sacred water",

    frozenset(["mace", "ank", "feather"]):
        "divine authority balanced by truth: the royal mace proclaims the sovereign's power "
        "to act, the feather of Ma'at ensures that power is wielded with perfect justice, "
        "and the ankh confirms that righteous rule is the very source of eternal life",

    frozenset(["beetle", "egg", "sunrise"]):
        "Khepri born from the cosmic egg at dawn: the scarab of self-creation hatches from "
        "the primordial egg as the sun rises — the first act of divine self-generation that "
        "underpins all subsequent cycles of death and resurrection in the Egyptian cosmos",

    frozenset(["spiral", "water", "moon"]):
        "the lunar tide of eternal cycles: the spiral of infinite time turns with the "
        "moon's sacred phases above the dark waters — Thoth counts each revolution as "
        "the world is continuously renewed in its great nocturnal spiral of existence",

    frozenset(["snake", "egg", "moon"]):
        "the serpent guards the cosmic egg by moonlight: the cobra of hidden wisdom "
        "encircles the primordial egg beneath Thoth's lunar gaze — the mystery of creation "
        "protected through the sacred night until the appointed hour of divine birth arrives",

    frozenset(["bird", "star", "ank"]):
        "the ba soul achieves stellar immortality: the spirit bird soars bearing the ankh "
        "toward the imperishable circumpolar stars — the soul's flight from mortal existence "
        "to the eternal realm where it joins the divine assembly of the undying ones",

    frozenset(["table", "arms_up", "feather"]):
        "the offering found worthy by Ma'at: arms raised in the ka gesture of divine praise "
        "present gifts at the sacred altar, and the feather of truth descends to confirm "
        "that the offering is pure and accepted into the divine economy of the afterlife",

    frozenset(["boat", "ank", "feather"]):
        "the barque of the righteous soul: the sacred vessel carries the soul bearing the "
        "ankh across the celestial waters, Ma'at's feather having confirmed its worthiness "
        "for the eternal voyage to the realm of the imperishable and the blessed dead",

    frozenset(["mansion", "tower", "feather"]):
        "the temple of truth: the great pylon tower opens into the divine mansion, and the "
        "feather of Ma'at presides over every threshold — the entire sacred precinct is "
        "consecrated to truth, justice, and the right ordering of the divine and human worlds",

    frozenset(["beetle", "water", "sunrise"]):
        "Khepri rising from the primordial waters at dawn: the scarab of eternal renewal "
        "emerges from the depths of Nun as the sun crests the horizon — the most fundamental "
        "act of cosmic resurrection re-enacted at every sacred sunrise across eternity",

    frozenset(["spear", "cobra_kai", "ank"]):
        "the warrior-god's defence of life: the divine spear strikes down the enemies of "
        "order, the uraeus repels the serpent of chaos, and the ankh confirms that the "
        "cosmic battle is always fought in defence of the gift of eternal life",

    frozenset(["bow", "spear", "cobra_kai"]):
        "the martial triad of divine power: the bow's reach, the spear's precision, and "
        "the uraeus's venom combine into the complete arsenal of divine protection, ensuring "
        "that the cosmic order is defended against every threat from every direction",

    frozenset(["garden", "grain", "water"]):
        "the Field of Reeds in its full abundance: the paradise of Aaru blossoms with grain "
        "and is irrigated by the sacred Nile — the afterlife harvest that sustains all "
        "righteous souls through their eternal existence in the divine realm of the blessed",

    frozenset(["person", "table", "pot"]):
        "the worshipper at the offering altar: a person stands before the sacred table "
        "bearing the ritual vessel — the act of divine nourishment performed with devotion, "
        "completing the sacred economy that binds the living to the gods through offering",

    frozenset(["egg", "water", "moon"]):
        "the cosmic egg upon the lunar waters: the primordial egg of creation rests on the "
        "dark waters of Nun beneath Thoth's moonlight — the sacred stillness before the "
        "sun was born, the most ancient moment of divine genesis preserved in symbol",

    frozenset(["cross", "ank", "feather"]):
        "the fourfold truth of eternal life: the cross marks the four sacred directions "
        "of the created cosmos, the feather of Ma'at ensures justice in all four quarters, "
        "and the ankh seals the whole with the covenant of immortal divine life",

    frozenset(["sunrise", "bird", "ank"]):
        "the ba soul reborn at dawn: the spirit bird soars at sunrise bearing the ankh "
        "of eternal life — the soul's daily resurrection mirroring Ra's own, the divine "
        "promise that every death is followed by a glorious and inevitable rebirth",

    frozenset(["drop", "eye", "feather"]):
        "divine grief witnessed and judged by truth: the tears of Isis fall under the gaze "
        "of the all-seeing eye as Ma'at's feather measures the sincerity of mourning — "
        "sorrow itself is weighed and found to be a sacred act of devotion to the dead",

    frozenset(["horns", "cow", "water"]):
        "Hathor at the celestial Nile: the divine cow goddess of the sky bends to drink "
        "from the sacred waters — a scene of divine maternal nourishment in which the "
        "boundaries between heaven, earth, and the fertile Nile dissolve into one holy presence",

    frozenset(["mansion", "garden", "ank"]):
        "the temple with the paradise garden of eternal life: the god's divine dwelling "
        "opens onto the Field of Reeds, and the ankh confirms that all who enter this "
        "sacred precinct dwell in the abundance and beauty of immortal divine existence",

    frozenset(["scythe", "grain", "water"]):
        "the harvest of Osiris: the scythe cuts the sacred grain at the height of the Nile "
        "flood — the divine act of death that is simultaneously the promise of resurrection, "
        "since Osiris must fall before he can rise and feed the world through eternity",

    frozenset(["club", "mace", "cobra_kai"]):
        "the pharaoh's martial triad of divine authority: the club and the royal mace "
        "proclaim the king's power to subdue all enemies, while the uraeus confirms that "
        "this power flows directly from the solar gods and cannot be challenged by any force",

    frozenset(["bug", "beetle", "sunrise"]):
        "the lowly and the mighty united in resurrection at dawn: the ordinary bug and "
        "the sacred scarab share the power of transformation, both rising at sunrise to "
        "declare that even the humblest life participates in the eternal cycle of rebirth",

    frozenset(["person", "dog", "scale"]):
        "the soul led by Anubis to the scales of judgment: a person is guided by the divine "
        "jackal to the moment of divine reckoning — the most intimate and solemn encounter "
        "between a mortal soul and the machinery of divine cosmic justice",

    frozenset(["hook", "ank", "grain"]):
        "the crook of Osiris tends the field of eternal life: the shepherd's hook of divine "
        "rule guides the living, the grain of Osiris feeds the dead, and the ankh seals "
        "the covenant that righteous rule is the very foundation of immortal existence",

    frozenset(["whip", "ank", "feather"]):
        "the flail of divine authority measured by truth: the Nekhakha flail commands the "
        "harvest and proclaims royal power over the seasons, the feather of Ma'at ensures "
        "that power is exercised justly, and the ankh rewards the righteous with eternal life",

    frozenset(["ank", "moon", "eye"]):
        "the lunar eye of immortal awareness: the ankh of life joins Horus's eye beneath "
        "Thoth's moon, uniting healing vision, sacred knowledge, and enduring divine vitality",

    frozenset(["ank", "water", "moon"]):
        "the nocturnal waters of life: the moon governs the sacred flood while the ankh "
        "confirms that life renews through the measured rhythms of the Nile and night sky",

    frozenset(["eye", "moon", "star"]):
        "the eye that reads the night heavens: Horus's gaze joins Thoth's moon and the "
        "imperishable stars, revealing divine navigation, vigilance, and celestial order",

    frozenset(["boat", "moon", "water"]):
        "the moonlit barque passage: the sacred vessel moves across dark waters under "
        "lunar guidance, marking safe transition through the underworld's hidden channels",

    frozenset(["table", "water", "pot"]):
        "the completed libation rite: vessel and altar are united by sacred water, "
        "signifying purification, offering, and covenant between worshipper and deity",

    frozenset(["person", "eye", "feather"]):
        "the worshipper under truth and witness: a mortal stands before Ma'at's feather "
        "while the eye of Horus observes, declaring devotion accountable to divine justice",

    frozenset(["mansion", "eye", "water"]):
        "the temple purified under divine sight: sacred waters cleanse the divine mansion "
        "as Horus's eye guards each threshold and ritual act within the holy precinct",

    frozenset(["tower", "sunrise", "eye"]):
        "the dawn gateway under watchful protection: the temple pylon receives first light "
        "while the divine eye sanctifies passage between mortal and sacred realms",

    frozenset(["dog", "eye", "feather"]):
        "Anubis, witness, and truth aligned: the jackal guide, Horus's eye, and Ma'at's "
        "feather together seal a rite of guarded judgment and purified intention",

    frozenset(["dog", "moon", "water"]):
        "Anubis at the lunar crossing: under moonlit waters the jackal god leads souls "
        "through perilous transitions, ensuring safe nocturnal passage to rebirth",

    frozenset(["beetle", "moon", "star"]):
        "Khepri in the night sky cycle: the scarab's power of renewal continues beneath "
        "moon and stars, revealing resurrection as a cosmic process beyond daylight alone",

    # =========================================================================
    # 2-SYMBOL COMBINATIONS
    # =========================================================================

    frozenset(["ank", "pot"]):
        "ritual offering of life: the sacred vessel carries nourishment consecrated by the "
        "power of the ankh, transforming material food into an immortal divine gift",

    frozenset(["ank", "eye"]):
        "divine protection of life: the all-seeing eye of Horus watches over the soul "
        "bearing the ankh, ensuring that eternal life is shielded from all harm",

    frozenset(["ank", "feather"]):
        "life judged by truth: the soul declared worthy by Ma'at's feather receives the "
        "full gift of the ankh — immortality earned through a righteous earthly life",

    frozenset(["ank", "boat"]):
        "the voyage to eternal life: the sacred barque carries the soul, ankh in hand, "
        "across the celestial waters to the shores of the undying afterlife",

    frozenset(["ank", "sunrise"]):
        "solar immortality: Ra's eternal rising sun and the ankh of life unite to declare "
        "that existence, like the sun, can never be permanently extinguished",

    frozenset(["ank", "star"]):
        "stellar immortality: the soul bearing the ankh ascends to join the imperishable "
        "circumpolar stars, achieving the everlasting existence of the divine firmament",

    frozenset(["ank", "grain"]):
        "Osiris the life-giver: the grain god's resurrection and the ankh together proclaim "
        "that life, like wheat, is cut down only to rise again more abundantly than before",

    frozenset(["ank", "water"]):
        "the waters of life: sacred Nile water blessed with the power of the ankh becomes "
        "the primordial fluid of creation, purification, and eternal regeneration",

    frozenset(["ank", "cobra_kai"]):
        "the uraeus guards the living: the royal cobra, poised to strike all enemies, "
        "encircles the ankh in protective sovereignty — the living god's divine seal",

    frozenset(["ank", "scale"]):
        "life weighed in the balance: the soul's eternal fate is determined as the ankh "
        "is measured against the feather-scale of Ma'at in the hall of divine judgment",

    frozenset(["ank", "snake"]):
        "life through regeneration: the serpent that sheds its skin embodies the same "
        "renewal promised by the ankh — existence renewed, death transcended, life eternal",

    frozenset(["ank", "beetle"]):
        "Khepri's promise of life: the scarab deity's self-creation mirrors the eternal "
        "renewal offered by the ankh — life arising spontaneously from its own sacred power",

    frozenset(["ank", "dog"]):
        "Anubis grants passage to eternal life: the divine jackal, guardian of tombs and "
        "embalmer of bodies, leads the soul bearing the ankh into the afterlife's embrace",

    frozenset(["ank", "egg"]):
        "life from the creative void: the primordial egg of creation and the ankh together "
        "represent the earliest and most fundamental act of divine life-giving",

    frozenset(["ank", "triangle"]):
        "the pyramid as a life-machine: the triangular sacred form concentrates the sun's "
        "resurrectional power to guarantee the ankh-bearer's eternal survival",

    frozenset(["ank", "hand"]):
        "the hand of life: Ptah's creative hand that shapes all things is sealed "
        "with the ankh — divine craftsmanship always in service of eternal living beauty",

    frozenset(["ank", "mouth"]):
        "the word that gives life: the creative utterance (Hu) of the divine logos carries "
        "the power of the ankh — speech itself is the first and most sacred act of creation",

    frozenset(["ank", "spiral"]):
        "life in the eternal spiral: the ankh of immortality meets the infinite coil of "
        "cosmic time — existence spiralling without beginning or end through the sacred cycle",

    frozenset(["ank", "moon"]):
        "Thoth grants the gift of life: the lunar scribe of the gods bestows the ankh "
        "upon the worthy — knowledge and immortality united in the gift of the moon god",

    frozenset(["ank", "horns"]):
        "Hathor bestows eternal life: the divine cow goddess with sacred horns extends "
        "the ankh to all who seek her grace — maternal divine love as a gift of immortality",

    frozenset(["ank", "drop"]):
        "the tear that gives life: the sacred drop of Isis's mourning for Osiris carries "
        "the power of the ankh — grief transformed into resurrection through divine love",

    frozenset(["ank", "fathead_plant"]):
        "the lotus and the ankh: the sacred plant of rebirth and the symbol of eternal life "
        "unite — beauty arising from the waters, a perpetual declaration that life renews itself",

    frozenset(["ank", "garden"]):
        "the Field of Reeds and eternal life: the paradise of Aaru is entered bearing the "
        "ankh — immortal existence in the divine garden of abundance and sacred peace",

    frozenset(["ank", "branch"]):
        "the branch of living growth and immortality: new vegetation and the ankh together "
        "proclaim that growth, like eternal life, cannot be permanently halted",

    frozenset(["ank", "cow"]):
        "Hathor the divine mother grants eternal life: the celestial cow of the sky "
        "extends the ankh to her beloved — divine nourishment flowing into immortal existence",

    frozenset(["ank", "hook"]):
        "the crook of eternal rule: the Heqa crook of divine sovereignty and the ankh of "
        "immortality together proclaim that righteous shepherding of souls leads to eternal life",

    frozenset(["ank", "whip"]):
        "the flail of eternal authority: the Nekhakha flail commands the harvest of souls "
        "as the ankh confirms that divine power wielded justly grants immortal life",

    frozenset(["ank", "mace"]):
        "the mace of eternal sovereignty: the royal instrument of divine authority is sealed "
        "with the ankh — the king's power over death confirmed by the gift of eternal life",

    frozenset(["ank", "mansion"]):
        "the divine temple as a home for eternal life: the god's sacred dwelling shelters "
        "the ankh — a place where mortal time dissolves into the infinite divine present",

    frozenset(["ank", "tower"]):
        "the pylon gateway to immortal life: the great temple tower marks the threshold "
        "between the mortal world and the divine realm where the ankh of life resides",

    frozenset(["ank", "person"]):
        "the mortal granted eternal life: a person receives the ankh from the gods — "
        "the supreme divine gift that transforms a finite life into an immortal sacred existence",

    frozenset(["ank", "claw"]):
        "fierce divine protection of eternal life: the predatory claw guards the ankh bearer "
        "with unrelenting power — immortality protected by the most primal force of nature",

    frozenset(["ank", "spear"]):
        "the divine warrior guards eternal life: the spear of sacred battle is wielded in "
        "defence of the ankh — existence protected through the precise and determined force of the gods",

    frozenset(["eye", "feather"]):
        "the divine eye of truth: Horus sees all and Ma'at judges all — together they "
        "ensure that no falsehood escapes divine notice and no truth goes unrewarded",

    frozenset(["eye", "beetle"]):
        "the eye of Horus and the scarab of Khepri: divine perception joins transformative "
        "solar renewal, revealing a vision that heals and rebirths what it beholds",

    frozenset(["eye", "cobra_kai"]):
        "divine vigilance and royal protection: the all-seeing eye and the striking uraeus "
        "combine into the supreme protective force that guards the pharaoh and the sacred",

    frozenset(["eye", "scale"]):
        "divine sight at the scales of judgment: nothing escapes the eye as Ma'at's scales "
        "reveal the soul's deepest moral reality for all the gods of the tribunal to witness",

    frozenset(["eye", "snake"]):
        "the eye and the serpent as dual guardians: the seeing power of Horus and the "
        "striking power of the cobra together make an invincible combination of protection",

    frozenset(["eye", "pot"]):
        "the divine eye blesses the offering: ritual libations placed under the watchful "
        "gaze of Horus are sanctified and received as genuine by the gods of the temple",

    frozenset(["eye", "grain"]):
        "divine abundance witnessed: the all-seeing eye of Horus watches over the fields "
        "of grain, ensuring Osiris's gift of sustenance reaches all who are truthful",

    frozenset(["eye", "star"]):
        "the eye that sees through the night: Horus's divine gaze pierces even the darkness "
        "of the underworld, naming the stars and guiding all souls through the sacred night",

    frozenset(["eye", "triangle"]):
        "the all-seeing eye atop the pyramid: the divine gaze watches from the apex of the "
        "sacred triangular form — the pharaoh's eternal vigilance over the living and the dead",

    frozenset(["eye", "sunrise"]):
        "the eye of Ra at the dawn of creation: Horus's divine gaze opens with the rising "
        "sun, the whole world illuminated and brought into being by the act of divine seeing",

    frozenset(["eye", "water"]):
        "the eye reflected in the sacred Nile: Horus's divine vision is mirrored in the "
        "flood waters — seeing and being seen as the same act of divine illumination",

    frozenset(["eye", "dog"]):
        "Anubis and Horus both witness the soul: the jackal guides the dead as the eye "
        "watches — together they ensure no soul is lost and no deception goes undetected",

    frozenset(["eye", "moon"]):
        "Horus and Thoth in divine partnership: the eye of the solar falcon and the moon "
        "of the divine scribe together illuminate both day and night with divine awareness",

    frozenset(["boat", "water"]):
        "the sacred journey across the Nile: the divine barque traverses the ritual waters "
        "linking the worlds of the living and the dead in their eternal negotiation",

    frozenset(["boat", "star"]):
        "the night barque navigates by starlight: the vessel of Ra sails the subterranean "
        "darkness guided by the fixed stars toward its daily dawn resurrection",

    frozenset(["boat", "sunrise"]):
        "the solar barque of Ra: the great disc rides in its sacred vessel across the "
        "sky from east to west, the most fundamental journey governing all cosmic time",

    frozenset(["boat", "feather"]):
        "the barque of the worthy soul: Ma'at's feather has confirmed the soul's purity "
        "and the sacred vessel now carries it to the realm of the immortal blessed dead",

    frozenset(["feather", "scale"]):
        "the heart weighed against truth: the precise moment of the cosmic judgment — "
        "Ma'at's feather placed on the scale to measure the worthiness of a human soul",

    frozenset(["feather", "grain"]):
        "truth sustains life: the feather of justice and the grain of Osiris together "
        "declare that only a truthful life generates real and enduring nourishment",

    frozenset(["feather", "moon"]):
        "Ma'at and Thoth in divine partnership: the feather of cosmic truth and the lunar "
        "scribe together keep the divine record — truth measured and inscribed for eternity",

    frozenset(["sunrise", "star"]):
        "day and night as a unified whole: the solar disk rising and the stars together "
        "encompass all of time — Ra ruling the day as the imperishable stars govern the sacred night",

    frozenset(["sunrise", "water"]):
        "Ra above the primordial waters: the sun rising from Nun at creation — the first "
        "light emerging from the limitless dark ocean that precedes all existence",

    frozenset(["sunrise", "beetle"]):
        "Khepri the morning sun: the scarab deity rolling the solar disk out of the "
        "underworld at each dawn, the living hieroglyph of perpetual cosmic renewal",

    frozenset(["sunrise", "snake"]):
        "Apep and Ra in eternal contest: the solar barque daily overcomes the great serpent "
        "of chaos, and light perpetually defeats darkness in the cosmic struggle of creation",

    frozenset(["sunrise", "grain"]):
        "Ra and Osiris in creative partnership: the solar energy and the grain god's "
        "resurrection combine to produce the food and light upon which all of Egypt depends",

    frozenset(["sunrise", "triangle"]):
        "the pyramid focuses solar power at dawn: the triangular slope catches and channels "
        "Ra's light from the first rays of morning to the last burning glow of dusk",

    frozenset(["sunrise", "egg"]):
        "the solar egg of creation: the primordial egg from which Ra hatched at the first "
        "dawn — the most ancient symbol of the cosmos awakening to its own divine existence",

    frozenset(["water", "grain"]):
        "the Nile flood and the harvest: the annual inundation deposits the sacred silt "
        "that grows the grain — Egypt's eternal cycle of destruction, renewal, and abundance",

    frozenset(["water", "star"]):
        "the celestial ocean of night: the stars swim in the cosmic sea of the heavens "
        "just as the dead sail the underground Nile — two mirrors of the same sacred journey",

    frozenset(["water", "snake"]):
        "Apep in the underworld river: the great serpent of chaos inhabits the underground "
        "waters that Ra's barque must traverse — darkness within the sacred river of the dead",

    frozenset(["water", "moon"]):
        "the lunar tides of the sacred Nile: the moon governs the sacred flood, and "
        "Thoth the moon god measures the waters that give Egypt life at the appointed time",

    frozenset(["water", "egg"]):
        "the primordial egg upon the cosmic ocean: the egg of the great cackler resting "
        "upon the waters of Nun — the sacred origin point of all that is and ever shall be",

    frozenset(["water", "drop"]):
        "the sacred inundation and the tear of Isis: the great flood is both the gift of the "
        "Nile and the divine grief of Isis, whose mourning for Osiris fills the river each year",

    frozenset(["water", "fathead_plant"]):
        "the lotus on the Nile: the sacred plant rises from the flood waters — the most "
        "visible symbol of Egypt's faith that beauty, purity, and life arise from the deep",

    frozenset(["cobra_kai", "feather"]):
        "royal justice: the uraeus of the pharaoh enforces the laws of Ma'at — the "
        "king's serpentine power is exercised always in the service of cosmic truth",

    frozenset(["cobra_kai", "sunrise"]):
        "the uraeus of the solar pharaoh: the royal cobra rears before the rising sun "
        "on the royal brow — the living image of Ra's sovereignty and fierce protective light",

    frozenset(["cobra_kai", "triangle"]):
        "the uraeus guards the pyramid: the royal cobra rears before the sacred triangular "
        "tomb, ensuring that no force of chaos can violate the pharaoh's eternal resting place",

    frozenset(["cobra_kai", "scale"]):
        "the royal cobra enforces divine judgment: the uraeus ensures that no soul "
        "can escape or corrupt the scales of Ma'at — justice is absolute under the pharaoh's protection",

    frozenset(["dog", "scale"]):
        "Anubis at the scales: the divine jackal presides over the weighing of the heart, "
        "ensuring every judgment is conducted with perfect solemn accuracy and fairness",

    frozenset(["dog", "pot"]):
        "Anubis receives the offering: ritual vessels are presented to the jackal god "
        "who oversees the preparation of the body and the provisioning of the tomb",

    frozenset(["dog", "star"]):
        "Anubis guides the soul to the stars: the divine jackal leads each deceased through "
        "the dark underworld passages toward the imperishable stellar realm of eternity",

    frozenset(["dog", "water"]):
        "Anubis at the waters of the underworld: the jackal god guides souls across the "
        "dark subterranean Nile, ensuring safe passage through the most dangerous crossing",

    frozenset(["beetle", "water"]):
        "Khepri emerging from Nun: the scarab of renewal rises from the primordial waters "
        "recreating the original moment of self-generated solar creation at each new dawn",

    frozenset(["beetle", "star"]):
        "the scarab among the imperishable stars: Khepri's power of self-renewal places "
        "him among the stars that never set — the ultimate symbol of undying existence",

    frozenset(["beetle", "egg"]):
        "the scarab and the cosmic egg: both are symbols of self-generated creation — "
        "the scarab rolling the sun and the egg containing it are two faces of the same mystery",

    frozenset(["grain", "pot"]):
        "the harvest offering: grain placed in the sacred vessel becomes the ritual food "
        "of the gods — earthly abundance transformed into divine sustenance through ceremony",

    frozenset(["grain", "star"]):
        "Osiris as the stellar grain: the god dies like the harvest cut at season's end "
        "and rises like the stars that faithfully return after their period of absence",

    frozenset(["grain", "egg"]):
        "the grain and the cosmic egg of creation: the seed that feeds the world and the "
        "egg that hatched the sun share the same sacred mystery of life arising from apparent death",

    frozenset(["snake", "moon"]):
        "the serpent of the lunar night: the cobra goddess guards the moon's nightly cycle, "
        "the waxing and waning mirroring the serpent's shedding of the old skin of death",

    frozenset(["moon", "star"]):
        "the night sky in its full glory: Thoth's moon and the imperishable stars together "
        "illuminate the sacred darkness through which all great divine journeys must pass",

    frozenset(["moon", "egg"]):
        "the cosmic egg beneath the sacred moon: the primordial egg of creation rests under "
        "Thoth's lunar light — the moon god oversees the mystery of all beginnings",

    frozenset(["triangle", "star"]):
        "the pyramid aligned with the stars: the sacred geometric form points precisely "
        "to the circumpolar stars, the destination of the pharaoh's eternal celestial soul",

    frozenset(["hand", "mouth"]):
        "the creative act of Ptah: the divine craftsman thinks, speaks (Hu), and works "
        "with his hands to bring each element of the created cosmos into physical being",

    frozenset(["egg", "water"]):
        "the primordial egg upon the cosmic ocean: the egg of the great cackler resting "
        "upon the waters of Nun — the sacred origin point of all that is and ever shall be",

    frozenset(["cross", "circle"]):
        "the four quarters of the sun: the cross marking the cardinal directions inscribed "
        "within the solar circle — the complete sacred geometry of the ordered cosmos",

    frozenset(["pot", "water"]):
        "the libation vessel filled with sacred water: temple priests pour the pure Nile "
        "water from the ritual pot as a divine offering sanctifying the sacred space",

    frozenset(["mouth", "feather"]):
        "the opening of the mouth ritual: the sacred ceremony restores the power of speech "
        "to the mummified dead so that they may speak the truths of Ma'at before the gods",

    frozenset(["bird", "egg"]):
        "the ba soul and the primordial egg: the spirit present at creation itself — the bird "
        "of the soul beside the world-egg declares this soul to be of divine and ancient origin",

    frozenset(["bird", "moon"]):
        "the ba soul under the moon's sacred light: the bird of the spirit flies by night "
        "guided by Thoth's lunar glow — the moon god watches over all souls in their nocturnal journeys",

    frozenset(["bird", "table"]):
        "the ba soul at the offering altar: the bird of the spirit descends to accept the "
        "sacred food from the altar of the gods — the ka offerings sustain the ba through eternity",

    frozenset(["bird", "arms_up"]):
        "worshippers hail the ba soul: arms raised in the ka gesture of divine praise, the "
        "living celebrate the bird of the spirit as it descends to accept devotion and nourishment",

    frozenset(["arms_up", "table"]):
        "the offering ceremony of praise: arms raised to heaven in worship over the sacred "
        "altar — the gesture of devotion transforms earthly food into divine nourishment",

    frozenset(["arms_up", "egg"]):
        "praise at the moment of creation: arms raised in the ka gesture before the "
        "primordial egg — worshippers celebrate the very first divine act of existence",

    frozenset(["spiral", "water"]):
        "the eternal spiral of the Nile: the river coils in its infinite course through "
        "the land, the spiral of time made visible in the most sacred of all Egyptian waters",

    frozenset(["spiral", "star"]):
        "the spiral of stellar time: the circumpolar stars trace their spiral paths through "
        "the night sky — the eternal coil of cosmic time made visible in the heavens above",

    frozenset(["spiral", "moon"]):
        "the spiral of the lunar cycle: the moon's waxing and waning traces the sacred "
        "spiral of time — Thoth counting each revolution as the world turns without end",

    frozenset(["drop", "eye"]):
        "the tear of Horus: the eye weeps in grief and healing — the divine tear that "
        "restores sight, heals wounds, and transforms mourning into a sacred act of regeneration",

    frozenset(["drop", "feather"]):
        "the sacred tear weighed by truth: Isis's mourning drop is measured by the feather "
        "of Ma'at — divine grief found to be pure and its love confirmed as the truest of offerings",

    frozenset(["fathead_plant", "sunrise"]):
        "the lotus at dawn: the sacred flower opens with the rising sun, re-enacting the "
        "first morning when the lotus opened on the primordial waters and the sun god was born",

    frozenset(["fathead_plant", "star"]):
        "the lotus under the stars: the sacred flower of rebirth rests in the stellar night, "
        "closed until the sun returns — a symbol of the soul awaiting its own celestial dawn",

    frozenset(["horns", "cow"]):
        "Hathor in her fullest form: the divine cow goddess crowned with her sacred horns "
        "embodies the complete power of divine motherhood, celestial fertility, and sacred beauty",

    frozenset(["horns", "sunrise"]):
        "Hathor receives the rising sun between her horns: the divine cow goddess holds "
        "the solar disk between her crescent horns — the sky herself cradling the newborn Ra",

    frozenset(["horns", "moon"]):
        "the crescent horns and the crescent moon: the horns of Hathor mirror the "
        "crescent of Thoth's moon — the divine feminine principles of heaven and wisdom united",

    frozenset(["mansion", "garden"]):
        "the divine temple and its paradise garden: the god's sacred dwelling opens onto "
        "the Field of Reeds — the boundary between the holy precinct and eternal paradise dissolved",

    frozenset(["mansion", "tower"]):
        "the complete sacred temple complex: the great pylon tower marks the entrance to "
        "the divine mansion — the full architecture of sacred space between god and worshipper",

    frozenset(["tower", "star"]):
        "the temple pylon aligned with the stars: the great gateway of the sacred precinct "
        "is oriented to the circumpolar stars — the temple itself a machine for stellar ascension",

    frozenset(["tower", "sunrise"]):
        "the temple pylon at dawn: the great gateway catches the first rays of Ra and "
        "radiates them into the sacred precinct — the entire temple illuminated by divine light",

    frozenset(["hook", "whip"]):
        "the crook and flail: the two emblems of Osiris and the pharaoh — the shepherd's "
        "crook that gathers souls and the flail that drives the harvest of the sacred dead",

    frozenset(["hook", "ank"]):
        "the crook of eternal rule: divine sovereignty over all souls expressed through "
        "the Heqa crook, the ankh confirming that just rule leads inevitably to immortal life",

    frozenset(["whip", "scale"]):
        "the flail and the scales of Ma'at: royal authority and divine judgment united — "
        "the pharaoh commands the harvest as Ma'at measures the yield of every moral life",

    frozenset(["scythe", "grain"]):
        "the harvest of Osiris: the scythe cuts the sacred grain — the divine act of "
        "ritual death that precedes and guarantees the resurrection of the grain god himself",

    frozenset(["scythe", "moon"]):
        "the lunar scythe: the crescent moon mirrors the shape of the harvest blade — "
        "Thoth counts the seasons as the scythe falls, marking each cycle of divine death and renewal",

    frozenset(["mace", "cobra_kai"]):
        "the royal weapons of divine power: the mace smites the enemies of order and "
        "the uraeus repels the forces of chaos — the pharaoh's complete martial divine authority",

    frozenset(["spear", "cobra_kai"]):
        "the guardian's paired weapons: the spear and the uraeus together protect the "
        "sacred from every direction, the spear's reach combining with the cobra's lethal vigilance",

    frozenset(["bow", "spear"]):
        "the complete martial arsenal of the divine warrior: the bow reaches the distant "
        "enemy while the spear strikes close — together they represent total dominion over warfare",

    frozenset(["claw", "cobra_kai"]):
        "the fiercest protective pair in the divine arsenal: the predatory claw and the "
        "venomous uraeus together create an encounter that no enemy of the sacred can survive",

    frozenset(["club", "mace"]):
        "the double instruments of pharaonic authority: the club and the mace together "
        "proclaim absolute royal power over all enemies of the cosmic order",

    frozenset(["person", "arms_up"]):
        "the worshipper in divine praise: a person raises their arms in the ka gesture "
        "of open-hearted worship — the fundamental human posture of devotion before the gods",

    frozenset(["person", "feather"]):
        "the mortal measured by divine truth: a person stands before the feather of Ma'at "
        "to be weighed — the most personal and consequential encounter with divine justice",

    frozenset(["person", "dog"]):
        "the soul accompanied by Anubis: a person walks with the divine jackal through the "
        "underworld — the most comforting and necessary companionship of the sacred dead",

    frozenset(["person", "table"]):
        "the worshipper at the sacred altar: a person stands before the offering table "
        "in an act of devotion, completing the divine economy of nourishment between human and god",

    frozenset(["person", "boat"]):
        "the soul embarked on the eternal voyage: a person boards the sacred barque for "
        "the journey across the celestial waters — the mortal life ended, the divine life begun",

    frozenset(["garden", "water"]):
        "the Field of Reeds irrigated by the sacred Nile: the paradise of the righteous "
        "dead is watered by the eternal river — abundance and peace flowing through eternity",

    frozenset(["garden", "star"]):
        "the Field of Reeds beneath the eternal stars: the afterlife paradise lies under "
        "the same imperishable stars that guided the soul's journey across the celestial sea",

    frozenset(["garden", "grain"]):
        "the paradise harvest: the Field of Reeds grows the grain of Osiris in eternal "
        "abundance — the righteous dead reap a harvest that never fails and always nourishes",

    frozenset(["hump", "egg"]):
        "creation in the desert of beginnings: the primordial egg appears upon the arid "
        "horizon, joining the hump of the desert landscape to proclaim life emerging even "
        "from hardship and sacred emptiness",

    frozenset(["hump", "sunrise"]):
        "dawn over the desert ridge: the rising sun crowns the hump-shaped horizon, "
        "signifying endurance, renewal, and the spirit's strength through trials",

    frozenset(["branch", "water"]):
        "new growth fed by sacred waters: the living branch of the world tree is nourished "
        "by the Nile's eternal flood — the most fundamental act of divine agricultural renewal",

    frozenset(["branch", "sunrise"]):
        "the living branch at dawn: new growth reaches toward the rising sun, the branch "
        "and the solar disk together proclaiming the irresistible drive of life toward the light",

    frozenset(["stacked_lines", "feather"]):
        "divine measurement and cosmic truth: the layered horizons of ordered reality are "
        "aligned with Ma'at's feather — the structured cosmos confirmed as an act of perfect justice",

    frozenset(["stacked_lines", "water"]):
        "the measured Nile: the layered lines of divine order track the Nile's sacred rise "
        "and fall — the annual flood measured by the gods and found to be perfectly ordained",

    frozenset(["crooked_line", "water"]):
        "the winding Nile: the crooked path of the sacred river traces the divine body of "
        "Osiris through the land — the river itself a sacred hieroglyph of the god's life-giving form",

    frozenset(["crooked_line", "snake"]):
        "the serpent's winding path and the crooked river: both trace the same sacred "
        "undulating course through the world — wisdom and the Nile as two expressions of divine flow",

    frozenset(["spiral", "egg"]):
        "the spiral of creation: the cosmic egg and the infinite spiral together represent "
        "the two great symbols of emergence — life appearing from the coil of sacred potential",

    frozenset(["drop", "grain"]):
        "the sacred rain upon the grain of Osiris: the life-giving drop of water falls "
        "upon the sacred grain — the smallest act of divine nourishment that sustains the world",

    frozenset(["drop", "moon"]):
        "the lunar dew: the moon draws up the sacred moisture of the Nile as dew — "
        "Thoth measuring out the divine drops of water that sustain the world through the sacred night",

    frozenset(["cross", "ank"]):
        "the fourfold world and the gift of life: the cross of four directions receives "
        "the ankh at its centre — the cosmic architecture of the world sealed with divine immortality",

    frozenset(["circle", "sunrise"]):
        "the solar disk at dawn: the circular form of Ra rises at the horizon — the perfect "
        "wholeness of the sun god made manifest in the most fundamental act of daily cosmic renewal",

    frozenset(["circle", "ank"]):
        "the solar circle and eternal life: the wholeness of Ra's disk and the gift of the "
        "ankh unite — existence as circular as the sun, life as eternal as its daily return",

    frozenset(["circle", "star"]):
        "the sun disk among the imperishable stars: the circular solar form and the fixed "
        "stars together encompass the totality of the Egyptian sacred sky in all its divine glory",

    frozenset(["cello", "table"]):
        "sacred music at the divine altar: the sound of divine harmony is offered at the "
        "gods' table — music and nourishment together completing the fullness of sacred worship",

    frozenset(["brush", "feather"]):
        "the scribal art of truth: the reed brush of the sacred scribe and the feather of "
        "Ma'at together declare that writing itself is an act of divine cosmic truth-telling",

    frozenset(["brush", "stacked_lines"]):
        "the scribe records the divine order: the scribal brush traces the layered lines of "
        "sacred knowledge — every hieroglyph a pillar of the cosmic structure of the world",

    frozenset(["container_with_lines", "feather"]):
        "the sacred inscription judged by truth: the vessel inscribed with divine text is "
        "measured by the feather of Ma'at — knowledge found to be worthy of eternal preservation",

    frozenset(["box", "ank"]):
        "the sarcophagus of eternal life: the sacred container that preserves the body is "
        "sealed with the ankh — the coffin as a womb of resurrection from which life re-emerges",

    frozenset(["box", "feather"]):
        "the sarcophagus measured by truth: the sacred container of the body is placed "
        "under the feather of Ma'at — the deceased within found worthy of eternal preservation",

    frozenset(["hat", "cobra_kai"]):
        "the crown with the uraeus: divine headgear bearing the royal cobra — the most "
        "visible declaration of the pharaoh's divinity and the gods' protection of the crown",

    frozenset(["hat", "ank"]):
        "the divine crown and eternal life: the sacred headgear of divine authority is "
        "paired with the ankh — the crown both bestowing and symbolising immortal divine rule",

    frozenset(["head", "eye"]):
        "the divine mind and its all-seeing gaze: the sacred head — seat of consciousness — "
        "and the divine eye together embody the totality of divine awareness and perception",

    frozenset(["head", "ank"]):
        "the conscious mind sealed with eternal life: the head as the seat of the soul "
        "bears the ankh — consciousness and immortality as the two gifts of the divine",

    frozenset(["lions_head", "ank"]):
        "Sekhmet grants fierce eternal life: the divine lioness's solar fury is tempered "
        "by the ankh — fierce protection and immortality as the two faces of the solar goddess",

    frozenset(["lions_head", "sunrise"]):
        "Sekhmet as the fury of the morning sun: the lioness goddess rises with Ra at dawn, "
        "her fierce solar power blazing across the sky as a declaration of divine sovereignty",

    frozenset(["cow", "sunrise"]):
        "Hathor receives the morning sun: the celestial cow goddess rises with Ra, the sky "
        "itself — her body arched above the horizon, holding the solar disk between her sacred horns",

    frozenset(["cow", "star"]):
        "Hathor the star-speckled cow of heaven: her divine body is the night sky adorned "
        "with stars, the goddess of love and beauty identified with the Milky Way's sacred arch",

    frozenset(["mammal", "water"]):
        "the animal kingdom nourished by the sacred Nile: the earthly creatures drink from "
        "the divine river — the bond between all living things and the source of Egypt's abundance",

    frozenset(["rabbit", "sunrise"]):
        "the hare leaps into existence at dawn: the swiftness of the hare hieroglyph 'wn' "
        "— meaning 'to be' — is sealed by the rising sun, existence itself declared at daybreak",

    frozenset(["bug", "sunrise"]):
        "transformation at the dawning of a new day: even the lowliest creature is renewed "
        "at sunrise, the most humble life participating in the cosmic act of daily resurrection",

    frozenset(["goat_leg", "water"]):
        "the agile navigator of sacred terrain: the goat's leg crosses the desert as the "
        "sacred Nile crosses the land — resilience and the life-giving river in divine partnership",

    frozenset(["2_humps", "water"]):
        "the double horizon over the sacred waters: the dual mound of the horizon rises "
        "above the Nile, the sun passing between the twin peaks in its eternal daily circuit",

    frozenset(["2_legs", "boat"]):
        "the walking dead and the sacred barque: the paired legs of the living journey "
        "toward the divine vessel — the moment when walking ends and the eternal voyage begins",

    frozenset(["3_flowers", "water"]):
        "the abundance of flowering vegetation fed by the sacred Nile: three blooms "
        "declare divine fertility and the overflowing generosity of the Nile's annual flood",

    frozenset(["3_pots", "table"]):
        "the triple offering at the sacred altar: three ritual vessels placed upon the "
        "divine table — the fullness of generosity offered to the gods in a single sacred act",

    frozenset(["3_water", "grain"]):
        "the Nile in its threefold abundance nourishes the sacred grain: three streams of "
        "the sacred river feed Osiris's wheat — the multiplied divine generosity of the flood",

    frozenset(["amulet", "ank"]):
        "the protective charm of eternal life: the amulet's divine shielding power and the "
        "ankh's gift of immortality combine into the most complete personal sacred protection",

    frozenset(["amulet", "cobra_kai"]):
        "the amulet and the uraeus as paired protection: two shields of divine power — "
        "the amulet deflects harm while the uraeus strikes it down, together covering every threat",

    frozenset(["banner", "ank"]):
        "the divine standard bearer of eternal life: the banner of the god's presence "
        "is paired with the ankh — marking the sacred space where immortality is granted",

    frozenset(["belt", "ank"]):
        "the sacred girdle of eternal authority: the royal belt of power bound with the "
        "ankh of immortality — divine sovereignty and eternal life worn as one upon the body",

    frozenset(["brush", "ank"]):
        "the scribal gift of sacred life: the scribal brush that records divine knowledge "
        "is sealed with the ankh — writing itself as an act that grants immortal existence",

    frozenset(["sled", "boat"]):
        "the ground support and the celestial vessel: the ritual sled that carries the "
        "barque to the water's edge marks the moment of transition from earth to eternity",

    frozenset(["snail", "spiral"]):
        "the snail's shell as the living spiral of time: the slow creature carries the "
        "sacred spiral pattern on its back — patience, persistence, and the eternal coil of the cosmos",

    frozenset(["spiral", "sunrise"]):
        "the spiral of the new day: the infinite coil of cosmic time is renewed at each "
        "sunrise — the world unwinding and rewinding its sacred spiral with each sacred dawn",

    frozenset(["stop_light", "ank"]):
        "the sacred boundary and the gift of life: the marking of holy thresholds is "
        "paired with the ankh — the boundary itself as a gateway to the gift of eternal life",

    frozenset(["drop", "sunrise"]):
        "the morning dew and the rising sun: the sacred drop of divine moisture catches "
        "the first rays of Ra at dawn — the smallest act of renewal reflecting the greatest",

    frozenset(["stacked_lines", "star"]):
        "the ordered cosmos beneath the imperishable stars: the layered horizons of sacred "
        "order are measured against the circumpolar stars — the architecture of heaven and earth aligned",

    frozenset(["container_with_lines", "ank"]):
        "the sacred inscription sealed with eternal life: the vessel of inscribed divine "
        "knowledge bears the ankh — sacred text as a container and a source of immortal existence",

    frozenset(["box", "star"]):
        "the sarcophagus aligned with the stars: the sacred coffin is oriented toward the "
        "circumpolar stars — the deceased within aimed at their eternal stellar destination",

    frozenset(["claw", "scale"]):
        "the fierce claw of divine justice: predatory power grips the scales of Ma'at — "
        "divine judgment executed with the relentless force of the most powerful sacred hunter",

    frozenset(["spear", "star"]):
        "the spear that reaches the stars: the divine weapon of precision strikes at the "
        "highest point of the sacred sky — divine force extended to the realm of the eternal",

    frozenset(["bow", "star"]):
        "the celestial archer: the bow of divine precision is drawn toward the imperishable "
        "stars — divine force aimed at the highest and most sacred targets in the heavens above",

    frozenset(["garden", "bird"]):
        "the ba soul in the Field of Reeds: the bird of the spirit soars over the paradise "
        "garden of the afterlife — the soul arrived at its eternal home of divine abundance",

    frozenset(["garden", "sunrise"]):
        "the paradise garden at dawn: the Field of Reeds is bathed in the first light of "
        "Ra — the afterlife itself renewed each morning by the eternal return of the solar god",

    frozenset(["mansion", "star"]):
        "the temple aligned with the celestial realm: the divine dwelling is oriented toward "
        "the imperishable stars — the temple as a meeting point between earthly and heavenly existence",

    frozenset(["tower", "ank"]):
        "the pylon of eternal life: the great temple gateway through which all must pass "
        "bears the ankh of immortality — crossing the threshold is an act of sacred regeneration",

    frozenset(["person", "sunrise"]):
        "the mortal reborn at dawn: a person witnesses the rising of Ra and is renewed — "
        "the daily resurrection of the sun god mirrored in the renewal of every human soul",

    frozenset(["person", "star"]):
        "the mortal ascending to the stars: a person looks up at the imperishable stars "
        "and is reminded of their own divine destiny — the soul that was once mortal now eternal",

    frozenset(["hook", "grain"]):
        "the crook harvests the sacred grain: the shepherd's hook of divine rule gathers "
        "the wheat of Osiris — sovereignty over the living expressed through care for the harvest",

    frozenset(["scythe", "star"]):
        "the stellar harvest: the scythe cuts through the field of stars — the souls of "
        "the dead gathered like grain at the appointed time and brought into the divine realm",

    frozenset(["mace", "feather"]):
        "the mace wielded in justice: royal striking power is exercised under the direct "
        "authority of Ma'at's feather — force applied only where truth demands and approves",

    frozenset(["spear", "feather"]):
        "the spear of truth: the divine weapon of precision strikes only where Ma'at's "
        "feather approves — force and justice as inseparable aspects of the same divine will",

    frozenset(["bow", "feather"]):
        "the archer of truth: the bow is drawn only with the approval of Ma'at's feather "
        "— the reach of divine force governed entirely by the requirements of cosmic justice",

    frozenset(["cello", "ank"]):
        "the music of eternal life: divine harmony offered at the altar is sealed with the "
        "ankh — sacred sound as a direct pathway to the gift of immortal divine existence",

    frozenset(["dream_catcher", "star"]):
        "the divine net captures the messages of the stars: the protective net of sacred "
        "dreams gathers the communications of the imperishable ones — stellar wisdom made accessible",

    frozenset(["dream_catcher", "moon"]):
        "the net of nocturnal visions: the divine dream-catcher works by Thoth's moonlight "
        "to gather sacred messages from the lunar realm and deliver them to the dreaming soul",

    frozenset(["dream_catcher", "brush"]):
        "inscribed visions of the sacred night: the dream-catcher gathers divine messages "
        "while the scribal brush records them, transforming dreams into preserved sacred knowledge",

    frozenset(["circle", "dream_catcher", "water"]):
        "the solar net upon sacred waters: the circle of Ra and the dream-catcher's divine "
        "web gather omens above the Nile, where flowing water carries visions into purified "
        "understanding and spiritual protection",

    frozenset(["dress_tie", "ank"]):
        "the sacred garment sealed with eternal life: ceremonial dress binding and the ankh "
        "together declare that sacred identity, worn in ritual, is an act of immortal devotion",

    frozenset(["flag", "ank"]):
        "the divine standard of eternal life: the banner marking the god's sacred presence "
        "flies over the ankh — the whole precinct declared to be a space of immortal divine life",

    frozenset(["tie", "ank"]):
        "the sacred knot of eternal life: the binding of mortal and divine realms is "
        "sealed with the ankh — connection itself as the very mechanism of immortal existence",

    frozenset(["galea", "cobra_kai"]):
        "the warrior's helmet and the uraeus: the soldier's divine protection in battle "
        "is doubled by the royal cobra — physical armour and divine force as one complete shield",

    frozenset(["galea", "spear"]):
        "the fully armed divine warrior: the helmet and the spear together equip the "
        "sacred soldier for the cosmic battle against the forces of chaos and dissolution",

    frozenset(["brush", "star"]):
        "the scribe records the stars: the sacred scribal brush traces the names of the "
        "imperishable ones — the act of writing as a means of conferring and confirming stellar immortality",

    frozenset(["n", "water"]):
        "the phonetic sign of the sacred Nile: the water-ripple hieroglyph 'n' is the "
        "sound and the image of the Nile itself — language and the sacred river as one divine gift",

    frozenset(["a", "ank"]):
        "the first sound and the first gift of life: the phonetic glyph 'a' and the ankh "
        "of immortality together — the beginning of speech and the beginning of eternal existence",

    frozenset(["u", "ank"]):
        "the lord of all eternal life: the basket hieroglyph 'nb' meaning 'lord' or 'all' "
        "is paired with the ankh — universal sovereignty and immortal existence as one divine truth",

    # Fix: canonical key only. upside_down_cancer normalizes to cancer.
    frozenset(["cancer", "water"]):
        "the crab in the sacred waters: the crustacean of hidden cycles moves through the "
        "divine Nile — the mysteries of the deep made visible in the watery realm of creation",

    frozenset(["downward_c", "water"]):
        "the descending arc into the sacred waters: the setting sun enters the underworld "
        "river through the descending arc — the daily transition from light into the sacred dark",

    frozenset(["downward_g", "water"]):
        "the descending spiral into the sacred waters: the soul turns downward into the "
        "underworld Nile through the sacred spiral — introspection and depth before resurrection",

    frozenset(["curvy_thing", "water"]):
        "the fluid flow of sacred water: the curving form and the Nile mirror each other "
        "in their graceful motion — the divine flow of power and water as one sacred expression",

    frozenset(["2_lines_slanted", "water"]):
        "the dual waters of creation: two slanted lines represent the primordial duality "
        "of the sacred Nile — the river's two banks as the two shores of divine existence",

    frozenset(["3_vertical_lines", "ank"]):
        "the plural gift of life: three vertical lines multiplying the ankh's divine "
        "power — the many gifts of immortality poured out upon the worthy in abundance",

    frozenset(["2_vertical_lines", "feather"]):
        "the dual measurement of truth: two vertical lines stand as paired witnesses "
        "to the feather of Ma'at — duality and justice as the twin pillars of the divine order",

    frozenset(["amulet", "eye"]):
        "the protective charm under the divine gaze: the amulet is empowered by the "
        "all-seeing eye of Horus — sacred protection visible to the god and therefore most effective",

    frozenset(["pot", "grain"]):
        "the vessel filled with the sacred grain of Osiris: the ritual pot holds the "
        "harvest — earthly abundance made into divine offering through the act of sacred containment",

    frozenset(["pot", "star"]):
        "the ritual vessel offered to the stars: the sacred pot is lifted toward the "
        "imperishable ones — nourishment presented to the stellar souls of the divine dead",

    frozenset(["plate", "grain"]):
        "the offering plate laden with sacred grain: the ritual dish of Osiris's wheat "
        "is presented at the altar — the most fundamental of all divine nourishment made visible",

    frozenset(["plate", "water"]):
        "the ritual plate filled with Nile water: the sacred vessel of liquid offering "
        "presents the divine river's power to the gods as a gift of purification and renewal",

    frozenset(["cup", "water"]):
        "the ritual cup filled with sacred water: the libation vessel brimming with Nile "
        "water is poured before the altar — the most ancient and fundamental of all divine offerings",

    frozenset(["cup", "ank"]):
        "the cup of eternal life: the ritual vessel of divine drinking is sealed with the "
        "ankh — the sacred liquid within transformed into the elixir of immortal existence",

    frozenset(["tea_cup", "water"]):
        "the ritual drinking vessel at the sacred Nile: the ceremonial cup is filled "
        "with divine water — the act of sacred drinking as a direct communion with the life-giving river",

    frozenset(["person", "scale"]):
        "the mortal before the scales of Ma'at: a person faces the divine judgment — "
        "the most solemn and consequential moment of any human existence, mortal or eternal",
}


# -----------------------------------------------------------------------------
# LOOKUP FUNCTION
# -----------------------------------------------------------------------------
def find_symbol_fusion(symbol_set: set) -> tuple:
    return find_symbol_fusion_best(symbol_set)


def find_symbol_fusion_best(symbol_set: set, symbol_confidence: dict | None = None) -> tuple:

    if not symbol_set:
        return None, None

    symbols = sorted(symbol_set)
    n = len(symbols)
    max_combo_size = min(n, 5)

    candidates = []
    for size in range(max_combo_size, 1, -1):
        for combo in combinations(symbols, size):
            key = frozenset(combo)
            if key in FUSION_RULES:
                candidates.append(key)

    if not candidates:
        return None, None

    def _conf_avg(key: frozenset) -> float:
        if not symbol_confidence:
            return 0.0
        vals = [float(symbol_confidence.get(sym, 0.0)) for sym in key]
        return sum(vals) / len(vals) if vals else 0.0

    best_key = min(
        candidates,
        key=lambda key: (
            -len(key),
            -_conf_avg(key),
            tuple(sorted(key)),
        ),
    )
    return FUSION_RULES[best_key], best_key


"""# -----------------------------------------------------------------------------
Chooses best candidate based on:

1️⃣ More symbols
2️⃣ Higher confidence
3️⃣ Stable lexical order
# Quick sanity check
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print("  Fusion Rules — Lookup Test")
    print("=" * 65)

    test_cases = [
        {"ank", "eye", "pot"},
        {"ank", "boat", "sunrise"},
        {"feather", "scale"},
        {"ank", "eye", "feather", "scale", "dog"},
        {"grain", "water", "ank", "sunrise", "egg"},
        {"unknown_symbol_a", "unknown_symbol_b"},
    ]

    for symbols in test_cases:
        interp, key = find_symbol_fusion(symbols)
        print(f"\n  Input  : {sorted(symbols)}")
        if key:
            print(f"  Match  : {sorted(key)}")
            print(f"  Result : {interp}")
        else:
            print("  Result : No fusion rule found.")

    print("\n" + "=" * 65)
    print(f"  Total fusion rules defined: {len(FUSION_RULES)}")
    print("=" * 65)"""