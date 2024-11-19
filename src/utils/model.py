from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
import cv2
import numpy as np

from src.utils.base import preprocess_image, extract_word_images


class OCRModel(OnnxInferenceModel):

    def __init__(self, char_list: list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image_bytes: bytes) -> str:
        binary_image = preprocess_image(image_bytes)
        word_images = extract_word_images(binary_image)

        full_text = ""
        for word_image, _ in word_images:
            if word_image.size == 0:
                continue
            if word_image.shape[0] == 0 or word_image.shape[1] == 0:
                continue
            resized_word = cv2.resize(word_image, (128, 32), interpolation=cv2.INTER_LANCZOS4)
            resized_word = cv2.cvtColor(resized_word, cv2.COLOR_GRAY2BGR) if len(
                resized_word.shape) == 2 else resized_word
            image_pred = np.expand_dims(resized_word, axis=0).astype(np.float32)
            word_text = ctc_decoder(self.model.run(self.output_names, {self.input_names[0]: image_pred})[0], self.char_list)[0]
            full_text += f"{word_text} "

        return full_text.strip()