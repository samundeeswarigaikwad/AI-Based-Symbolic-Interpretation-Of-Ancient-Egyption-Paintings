import os
import hashlib
from datetime import datetime, timezone

from ultralytics import YOLO

from symbolic_interpreter import detections_from_yolo


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIGHTS_PATH = os.path.join(BASE_DIR, "Weights", "best.pt")

_model = None


def _get_model() -> YOLO:
    global _model
    if _model is None:
        _model = YOLO(WEIGHTS_PATH)
    return _model


def _symbol_color(symbol: str) -> tuple[int, int, int]:
    """Generate a stable, vivid BGR color for each symbol name."""
    digest = hashlib.md5(symbol.encode("utf-8")).digest()
    # Keep values in a bright range to ensure visibility on light/dark regions.
    b = 70 + (digest[0] % 156)
    g = 70 + (digest[1] % 156)
    r = 70 + (digest[2] % 156)
    return int(b), int(g), int(r)

#Draws bounding boxes and labels on image.
def _draw_detections(image, detections: list[dict]):
    import cv2  # pylint: disable=import-outside-toplevel

    for det in detections:
        symbol = det.get("symbol", "symbol")
        conf = float(det.get("confidence", 0.0))
        x1, y1, x2, y2 = [int(v) for v in det.get("bbox", [0, 0, 0, 0])]
        color = _symbol_color(symbol)

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        label = f"{symbol} {conf:.2f}"
        text_y = y1 - 8 if y1 - 8 > 12 else y1 + 16
        cv2.putText(
            image,
            label,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.52,
            color,
            2,
            cv2.LINE_AA,
        )

    return image


def _render_detections(image_path: str, detections: list[dict]):
    """Loads image and sends it for drawing, reads uploaded image"""
    import cv2  # load , display and draw

    image = cv2.imread(image_path)
    if image is None:
        return None
    return _draw_detections(image, detections)


def detect_symbols(
    image_path: str,
    conf_threshold: float = 0.65,
    iou_threshold: float = 0.60,
    max_symbols: int = 10,
    output_dir: str | None = None,
):
    """
    Run YOLO and, load, run prediction,convert output, sort confi,keep top symbols, save annoted image.

    Returns:
        tuple[list[dict], str | None]:
            - detections in the expected interpreter format
            - saved annotated image path if output_dir is provided
    """
    model = _get_model()
    results = model.predict(
        source=image_path,
        conf=conf_threshold,
        iou=iou_threshold,
        verbose=False,
    )
    detections = detections_from_yolo(results, model.names)
    detections.sort(key=lambda d: d.get("confidence", 0.0), reverse=True)
    detections = detections[:max_symbols]

    detected_image_path = None
    if output_dir is not None:
        os.makedirs(output_dir, exist_ok=True)
        file_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        detected_image_path = os.path.join(output_dir, f"detected_{file_id}.jpg")

        rendered = _render_detections(image_path, detections)
        if rendered is not None:
            # Use OpenCV lazily to avoid importing cv2 unless rendering is needed.
            import cv2  

            cv2.imwrite(detected_image_path, rendered)
        else:
            detected_image_path = None

    return detections, detected_image_path


def draw_detections_on_frame(
    frame,
    conf_threshold: float = 0.25,
    iou_threshold: float = 0.60,
    max_symbols: int = 10,
):
    """Run detection on a single live camera frame and return annotated frame."""
    model = _get_model()
    results = model.predict(
        source=frame,
        conf=conf_threshold,
        iou=iou_threshold,
        max_det=max_symbols,
        verbose=False,
    )
    if not results:
        return frame
    detections = detections_from_yolo(results, model.names)
    return _draw_detections(frame.copy(), detections)
