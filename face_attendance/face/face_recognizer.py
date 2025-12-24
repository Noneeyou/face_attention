import numpy as np
import cv2


class FaceRecognizer:
    def __init__(self, target_size=(100, 100)):
        self.target_size = target_size

    def extract_encoding(self, face_image):
        gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        resized = cv2.resize(equalized, self.target_size)
        normalized = resized.astype("float32")
        normalized = (normalized - normalized.mean()) / (normalized.std() + 1e-6)
        return normalized.flatten()

    def compare(self, encoding, candidates):
        if encoding is None or not candidates:
            return None, None
        encoding = self._normalize_vector(np.array(encoding, dtype="float32"))
        best_id = None
        best_score = -1.0
        for person_id, candidate in candidates:
            candidate_arr = self._normalize_vector(np.array(candidate, dtype="float32"))
            if candidate_arr.shape != encoding.shape:
                continue
            score = self.cosine_similarity(encoding, candidate_arr)
            if score > best_score:
                best_score = score
                best_id = person_id
        if best_score < 0:
            return None, None
        return best_id, best_score

    @staticmethod
    def cosine_similarity(vec_a, vec_b):
        vec_a = np.array(vec_a)
        vec_b = np.array(vec_b)
        denom = (np.linalg.norm(vec_a) * np.linalg.norm(vec_b))
        if denom == 0:
            return 0.0
        return float(np.dot(vec_a, vec_b) / denom)

    @staticmethod
    def _normalize_vector(vec):
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-6)
