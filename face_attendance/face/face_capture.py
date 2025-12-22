import cv2


class FaceCapture:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index

    def capture_face(self, window_title="Capture Face"):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            raise RuntimeError("Cannot open camera")

        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        captured_face = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow(window_title, frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("c") and len(faces) > 0:
                x, y, w, h = faces[0]
                captured_face = frame[y:y + h, x:x + w]
                break
            if key == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

        if captured_face is None:
            raise RuntimeError("Face capture cancelled or no face detected.")

        return captured_face
