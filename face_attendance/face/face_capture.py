import os
import cv2


class FaceCapture:
    def __init__(self, camera_index=0, prefer_directshow=True):
        self.camera_index = camera_index
        self.prefer_directshow = prefer_directshow
        cascade_path = self._resolve_cascade_path()
        self.detector = cv2.CascadeClassifier(cascade_path)
        if self.detector.empty():
            self.detector = None

    def _resolve_cascade_path(self):
        if hasattr(cv2, "data") and hasattr(cv2.data, "haarcascades"):
            return os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        module_dir = os.path.dirname(cv2.__file__)
        fallback = os.path.join(module_dir, "data", "haarcascade_frontalface_default.xml")
        return fallback

    def _open_camera(self):
        indices = [self.camera_index]
        if self.camera_index == 0:
            indices.extend([1, 2])

        backends = [cv2.CAP_DSHOW] if self.prefer_directshow else []
        backends.append(cv2.CAP_ANY)

        for index in indices:
            for backend in backends:
                cap = cv2.VideoCapture(index, backend)
                if cap.isOpened():
                    return cap
                cap.release()
        return None

    def capture_face(self, window_title="Capture Face"):
        cap = self._open_camera()
        if cap is None:
            raise RuntimeError(
                "Cannot open camera. Please check permissions or use image selection."
            )

        captured_face = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            faces = self._detect_faces(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow(window_title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c"):
                if faces:
                    x, y, w, h = faces[0]
                    captured_face = frame[y:y + h, x:x + w]
                else:
                    captured_face = frame
                break
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        if captured_face is None:
            raise RuntimeError("Face capture cancelled.")

        return captured_face

    def capture_from_file(self, file_path):
        image = cv2.imread(file_path)
        if image is None:
            raise RuntimeError("Failed to read image file.")
        face = self._extract_largest_face(image)
        return face if face is not None else image

    def _extract_largest_face(self, image):
        faces = self._detect_faces(image)
        if not faces:
            return None
        x, y, w, h = max(faces, key=lambda item: item[2] * item[3])
        return image[y:y + h, x:x + w]

    def _detect_faces(self, image):
        if self.detector is None:
            return []
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return self.detector.detectMultiScale(gray, 1.3, 5)
