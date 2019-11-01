# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import io
from PIL import Image
import logging
import tesserocr
from werkzeug.exceptions import BadRequest
from config import MODEL_META_DATA as model_meta
from maxfw.model import MAXModelWrapper

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):
    """Model wrapper for TensorFlow models in SavedModel format"""
    MODEL_META_DATA = model_meta

    def read_image(self, image_data):
        try:
            image = Image.open(io.BytesIO(image_data))
        except IOError as img_exception:
            logger.error(str(img_exception))
            e = BadRequest()
            e.data = {'status': 'error', 'message': 'The provided input is not a valid image.'}
            raise e

        return image

    def _post_process(self, x):
        x = x.rstrip()
        x = [y.split("\n") for y in x.split("\n\n")]
        return x

    def _predict(self, x):
        text = tesserocr.image_to_text(x.convert('L'), lang='eng')
        return text
