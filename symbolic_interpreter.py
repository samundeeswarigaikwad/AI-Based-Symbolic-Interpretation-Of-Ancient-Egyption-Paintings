
# Full interpretation pipeline: 
#   1. normalize_symbols()                 – variant names → canonical
#   2. remove_duplicates()                 – deduplicate, count occurrences
#   3. rank_symbols_by_confidence()        – sort by confidence score
#   4. extract_symbol_meanings()           – pull meanings from knowledge base
#   5. apply_fusion_rules()                – find multi-symbol interpretation
#   6. compute_interpretation_confidence() – calculate mean confidence
#   7. generate_interpretation()           – produce natural language output

from collections import Counter
from knowledge_base import SYMBOL_NORMALIZATION, get_symbol_meaning
from fusion_rules import find_symbol_fusion_best


def _human_symbol(symbol: str) -> str:
    return symbol.replace("_", " ")
#half_moon_top → half moon top

def _join_natural(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    return ", ".join(items[:-1]) + f" and {items[-1]}"
#["ank", "eye", "feather"]  - ank, eye and feather

def _is_unknown_meaning(meaning: str) -> bool:
    return "yet to be fully documented" in meaning


def _extract_theme(meaning: str) -> str:
    if not meaning or _is_unknown_meaning(meaning):
        return ""
    parts = [p.strip() for p in meaning.split(";") if p.strip()]
    candidate = parts[1] if len(parts) > 1 else parts[0]
    return candidate.split(",")[0].strip().rstrip(".")


# =============================================================================
# STEP 1 — SYMBOL NORMALIZATION #preprocessing
# =============================================================================

def normalize_symbols(detections: list) -> list:
    """[
 {"symbol":"ankh","confidence":0.91},
 {"symbol":"scarab","confidence":0.87}
]
[
 {"symbol":"ank","confidence":0.91},
 {"symbol":"beetle","confidence":0.87}
]
    Returns:
        list[dict]: Same structure with "symbol" replaced by the canonical name.
    """
    normalized = []
    for det in detections:
        entry = det.copy()
        entry["symbol"] = SYMBOL_NORMALIZATION.get(det["symbol"], det["symbol"])
        normalized.append(entry)
    return normalized


# =============================================================================
# STEP 2 — DUPLICATE REMOVAL #removes repeated detections of the same symbol.
# =============================================================================

def remove_duplicates(detections: list) -> list:
    """
    [
 {"symbol":"ank","confidence":0.91},
 {"symbol":"ank","confidence":0.84},
 {"symbol":"eye","confidence":0.88}
]
[
 {"symbol":"ank","confidence":0.91,"count":2},
 {"symbol":"eye","confidence":0.88,"count":1}
]
    """
    best_confidence = {}
    symbol_count = Counter()

    for det in detections:
        sym  = det["symbol"]
        conf = det["confidence"]
        symbol_count[sym] += 1
        if sym not in best_confidence or conf > best_confidence[sym]:
            best_confidence[sym] = conf

    return [
        {
            "symbol":     sym,
            "confidence": best_confidence[sym],
            "count":      symbol_count[sym],
        }
        for sym in best_confidence
    ]


# =============================================================================
# STEP 3 — CONFIDENCE RANKING #top symbol gets priority
# =============================================================================

def rank_symbols_by_confidence(detections: list) -> list:
    """
    This function ranks symbols by highest confidence, and if confidence is equal, repeated symbols get priority.
    """
    return sorted(detections, key=lambda d: (d["confidence"], d["count"]), reverse=True)


# =============================================================================
# STEP 4 — SYMBOL MEANING EXTRACTION #stores in dictionary
# =============================================================================

def extract_symbol_meanings(detections: list) -> dict:
   
    return {det["symbol"]: get_symbol_meaning(det["symbol"]) for det in detections}


# =============================================================================
# STEP 5 — FUSION RULE APPLICATION #checks
# =============================================================================

def apply_fusion_rules(detections: list) -> tuple:
    """
        tuple:
            - fusion_text  (str | None)
            - matched_syms (list | None)
    """
    symbol_set = {det["symbol"] for det in detections}
    symbol_confidence = {det["symbol"]: float(det["confidence"]) for det in detections}
    fusion_text, matched_key = find_symbol_fusion_best(symbol_set, symbol_confidence)
    matched_syms = sorted(matched_key) if matched_key is not None else None
    return fusion_text, matched_syms


# =============================================================================
# STEP 6 — INTERPRETATION CONFIDENCE 2.final_confidence=base_conf−penalty
# =============================================================================

def compute_interpretation_confidence(detections: list, fusion_syms: list | None = None) -> float:
    """
        float: Mean confidence rounded to 4 decimal places, or 0.0 if empty.
    """
    if not detections:
        return 0.0

    base_conf = sum(d["confidence"] for d in detections) / len(detections)

    if fusion_syms:
        fusion_set = set(fusion_syms)
        matched = [d["confidence"] for d in detections if d["symbol"] in fusion_set]
        fusion_conf = (sum(matched) / len(matched)) if matched else 0.0
        coverage = len(fusion_set) / len(detections)
        score = (0.65 * base_conf) + (0.25 * fusion_conf) + (0.10 * coverage)
        return round(min(1.0, max(0.0, score)), 4)

    # Without fusion support, confidence should be slightly conservative.
    uncertainty_penalty = 0.08 if len(detections) >= 3 else 0.04 if len(detections) == 2 else 0.0
    return round(max(0.0, base_conf - uncertainty_penalty), 4)


# =============================================================================
# STEP 7 — NATURAL LANGUAGE INTERPRETATION GENERATOR
# =============================================================================

def generate_interpretation(detections: list) -> dict:
    
    if not detections:
        return {
            "detected_symbols":   [],
            "symbol_counts":      {},
            "ranked_detections":  [],
            "symbol_meanings":    {},
            "fusion_symbols":     None,
            "fusion_text":        None,
            "confidence_score":   0.0,
            "frequency_analysis": "No symbols were detected in this image.",
            "final_paragraph":    (
                "No Egyptian symbols were detected. "
                "Try a clearer image or lower the confidence threshold."
            ),
            "final_explanation":  (
                "No Egyptian symbols were detected. "
                "Try a clearer image or lower the confidence threshold."
            ),
            "primary_symbols_used": [],
            "supporting_symbols_used": [],
            "repeated_symbols_used": [],
            "themes_used": [],
        }

    # --- Pipeline ---
    normalized   = normalize_symbols(detections)
    deduplicated = remove_duplicates(normalized)
    ranked       = rank_symbols_by_confidence(deduplicated)
    meanings     = extract_symbol_meanings(ranked)
    fusion_text, fusion_syms = apply_fusion_rules(ranked)
    confidence   = compute_interpretation_confidence(ranked, fusion_syms)

    # --- Frequency analysis text --- The system checks how often symbols repeat.
    def _snippet(meaning: str) -> str:
        theme = _extract_theme(meaning)
        return theme if theme else "meaning under study"

    freq_lines = []
    for det in ranked:
        sym    = det["symbol"]
        count  = det["count"]
        snip   = _snippet(meanings[sym])
        strength = "strong" if count >= 3 else "moderate" if count == 2 else "single"
        freq_word = "time" if count == 1 else "times"
        freq_lines.append(
            f"  • {_human_symbol(sym)} appears {count} {freq_word} ({strength} presence) -> {snip}"
        )
    frequency_analysis = "\n".join(freq_lines)

    # --- Natural language explanation ---
    symbol_list_str = _join_natural([_human_symbol(d["symbol"]) for d in ranked])
    meanings_block  = "\n".join(  #This creates line-by-line meanings & Align symbol names neatly ank, eye and feather
        f"  • {_human_symbol(sym):<22} -> {meanings[sym]}"
        for sym in [d["symbol"] for d in ranked]
    )

    if fusion_syms and fusion_text:
        fusion_syms_str = " + ".join(_human_symbol(sym) for sym in fusion_syms)
        fusion_block    = f"  {fusion_syms_str}\n  → {fusion_text}"
        matched_set = set(fusion_syms)
        supporting_syms = [d["symbol"] for d in ranked if d["symbol"] not in matched_set]
        primary_symbols = list(fusion_syms)
        final_paragraph = _compose_final_paragraph(
            ranked, meanings, fusion_text, fusion_syms, confidence, supporting_syms
        )
    else:
        fusion_block    = "  No multi-symbol fusion rule matched this set."
        primary_symbols = [d["symbol"] for d in ranked]
        supporting_syms = []
        final_paragraph = _compose_fallback_paragraph(ranked, meanings, confidence)

    repeated_symbols = [d["symbol"] for d in ranked if d["count"] >= 2]
    themes_used = []
    for det in ranked:
        theme = _extract_theme(meanings.get(det["symbol"], ""))
        if theme and theme not in themes_used:
            themes_used.append(theme)

    final_explanation = (
        "AI-Based Symbolic Interpretation of Ancient Egyptian Paintings\n"
        "\n"
        "Detected Symbols\n"
        f"  {symbol_list_str}\n"
        "\n"
        "Symbol Meanings\n"
        f"{meanings_block}\n"
        "\n"
        "Symbol Frequency Analysis\n"
        f"{frequency_analysis}\n"
        "\n"
        "Fusion Interpretation\n"
        f"{fusion_block}\n"
        "\n"
        "Final Interpretation\n"
        f"{final_paragraph}\n"
        "\n"
        "Interpretation Confidence\n"
        f"  {confidence:.2%}  ({confidence:.4f})"
    )

    return {
        "detected_symbols":   [d["symbol"] for d in ranked],
        "symbol_counts":      {d["symbol"]: d["count"] for d in ranked},
        "ranked_detections":  ranked,
        "symbol_meanings":    meanings,
        "fusion_symbols":     fusion_syms,
        "fusion_text":        fusion_text,
        "confidence_score":   confidence,
        "frequency_analysis": frequency_analysis,
        "final_paragraph":    final_paragraph,
        "final_explanation":  final_explanation,
        "primary_symbols_used": primary_symbols,
        "supporting_symbols_used": supporting_syms,
        "repeated_symbols_used": repeated_symbols,
        "themes_used": themes_used,
    }


# =============================================================================
# PRIVATE HELPERS
# =============================================================================

def _compose_final_paragraph(ranked, meanings, fusion_text, fusion_syms, confidence, supporting_syms):
    """Compose a natural-language paragraph when a fusion rule matched."""
    top      = ranked[0]["symbol"]
    top_mean = _extract_theme(meanings.get(top, "")) or "divine significance"

    recurrent = [d for d in ranked if d["count"] >= 2]
    rec_str = ""
    if recurrent:
        recurrent_names = [_human_symbol(d["symbol"]) for d in recurrent]
        rec_str = (
            f"{_join_natural(recurrent_names)} appear repeatedly, amplifying their themes. "
        )

    conf_word  = (
        "very high" if confidence >= 0.85 else
        "high"      if confidence >= 0.70 else
        "moderate"  if confidence >= 0.55 else
        "low"
    )

    syms_joined = _join_natural([_human_symbol(sym) for sym in fusion_syms])

    support_str = ""
    if supporting_syms:
        support_names = [_human_symbol(sym) for sym in supporting_syms]
        support_meanings = []
        for sym in supporting_syms:
            theme = _extract_theme(meanings.get(sym, ""))
            if theme and theme not in support_meanings:
                support_meanings.append(theme)
        if support_meanings:
            support_str = (
                " Additional context from "
                + _join_natural(support_names)
                + " deepens the scene's meaning, showing "
                + _join_natural(support_meanings)
                + "."
            )
        else:
            support_str = (
                " Additional context from "
                + _join_natural(support_names)
                + " offers supplementary visual cues, though some meanings remain under study."
            )

    return (
        f"This painting most prominently features {_human_symbol(top)} ({top_mean}). "
        f"{rec_str}"
        f"The combination of {syms_joined} suggests that the scene depicts "
        f"{fusion_text}. "
        f"{support_str}"
        f"Overall, the visual evidence supports this reading with {conf_word} confidence ({confidence:.2%})."
    )


def _compose_fallback_paragraph(ranked, meanings, confidence):
    """Compose a paragraph when no fusion rule matched."""
    if not ranked:
        return "No symbols detected."

    all_symbols = [d["symbol"] for d in ranked]
    themes = [_extract_theme(meanings.get(sym, "")) for sym in all_symbols]
    themes = [t for t in themes if t]

    # Keep unique themes in order to avoid repetitive wording.
    unique_themes = []
    for t in themes:
        if t not in unique_themes:
            unique_themes.append(t)

    themes_str = _join_natural(unique_themes)

    syms_str = _join_natural([_human_symbol(sym) for sym in all_symbols])

    recurrent = [d["symbol"] for d in ranked if d["count"] >= 2]
    recurrent_str = ""
    if recurrent:
        if len(recurrent) == 1:
            recurrent_theme = _extract_theme(meanings.get(recurrent[0], "")) or "their central symbolic theme"
            recurrent_str = (
                f" Repetition of {_human_symbol(recurrent[0])} reinforces the motif of "
                f"{recurrent_theme}."
            )
        else:
            recurrent_themes = []
            for sym in recurrent:
                theme = _extract_theme(meanings.get(sym, ""))
                if theme and theme not in recurrent_themes:
                    recurrent_themes.append(theme)
            if recurrent_themes:
                recurrent_str = (
                    " Repeated symbols ("
                    + ", ".join(_human_symbol(sym) for sym in recurrent)
                    + ") reinforce motifs of "
                    + _join_natural(recurrent_themes)
                    + "."
                )
            else:
                recurrent_str = (
                    " Repeated symbols ("
                    + ", ".join(_human_symbol(sym) for sym in recurrent)
                    + ") reinforce this symbolic motif."
                )

    unknown_syms = [
        d["symbol"]
        for d in ranked
        if _is_unknown_meaning(meanings.get(d["symbol"], ""))
    ]
    unknown_str = ""
    if unknown_syms:
        unknown_str = (
            " Some glyphs are still under-documented ("
            + ", ".join(_human_symbol(sym) for sym in unknown_syms)
            + "), so this reading remains provisional."
        )

    conf_word = (
        "very high" if confidence >= 0.85 else
        "high"      if confidence >= 0.70 else
        "moderate"  if confidence >= 0.55 else
        "low"
    )

    if len(ranked) == 1:
        return (
            f"The painting features the symbol {syms_str}, "
            f"which is associated with themes of {themes_str}. "
            f"Its singular presence conveys a focused sacred message rooted in "
            f"ancient Egyptian spiritual tradition. "
            f"Detection confidence is {conf_word} ({confidence:.2%})."
        )
    return (
        f"No exact fusion rule matched this symbol set, so the interpretation is derived "
        f"from symbolic context. The painting contains {syms_str}, which together point to "
        f"themes of {themes_str}."
        f"{recurrent_str}"
        f"{unknown_str}"
        f" Overall confidence is {conf_word} ({confidence:.2%})." 
        #indicating a "
        #f"contextual but meaningful reading of the scene."
    )


# =============================================================================
# CONVENIENCE WRAPPER — integrate with Ultralytics YOLO output
# =============================================================================

def detections_from_yolo(results, model_names: dict) -> list:
    """
    Convert raw Ultralytics YOLO result objects into the dictionary format
    expected by generate_interpretation().
        list[dict]: Each entry has "symbol", "confidence", and "bbox".
    """
    detections = []
    for result in results:
        for box in result.boxes:
            cls_idx    = int(box.cls[0])
            confidence = float(box.conf[0])
            bbox       = box.xyxy[0].tolist()
            detections.append({
                "symbol":     model_names[cls_idx],
                "confidence": confidence,
                "bbox":       bbox,
            })
    return detections




"""# =============================================================================
# Quick sanity check
# =============================================================================
if __name__ == "__main__":
    sample = [
        {"symbol": "ank",     "confidence": 0.92, "bbox": [10,  10,  80,  90]},
        {"symbol": "ank",     "confidence": 0.85, "bbox": [200, 30,  270, 110]},
        {"symbol": "eye",     "confidence": 0.89, "bbox": [300, 50,  380, 120]},
        {"symbol": "pot2",    "confidence": 0.81, "bbox": [150, 200, 220, 270]},
        {"symbol": "feather", "confidence": 0.60, "bbox": [400, 10,  450, 90]},
        {"symbol": "boat",    "confidence": 0.55, "bbox": [100, 300, 250, 390]},
    ]

    report = generate_interpretation(sample)
    print(report["final_explanation"])

    print("\n--- Raw report keys ---")
    for k, v in report.items():
        if k != "final_explanation":
            print(f"  {k}: {v}")"""