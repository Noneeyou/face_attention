import numpy as np
import cv2


class FaceRecognizer:
    def __init__(self, target_size=(100, 100)):
        self.target_size = target_size

    def extract_encoding(self, face_image):
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, self.target_size)
        normalized = resized.astype("float32") / 255.0
        return normalized.flatten()

    def compare(self, encoding, candidates):
        if encoding is None or not candidates:
            return None, None
        best_id = None
        best_score = None
        for person_id, candidate in candidates:
            score = self.cosine_similarity(encoding, candidate)
            if best_score is None or score > best_score:
                best_score = score
                best_id = person_id
        return best_id, best_score

    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        vec_a = np.array(vec_a)
        vec_b = np.array(vec_b)
        denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        if denom == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / denom)
