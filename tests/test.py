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

import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX OCR'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max-ocr'
    assert metadata['name'] == 'MAX OCR'
    assert metadata['description'] == 'Identify text in an image.'
    assert metadata['license'] == 'Apache v2'
    assert metadata['type'] == 'Optical Character Recognition'
    assert 'max-ocr' in metadata['source']


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/quick_start_watson_studio.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'

    assert len(response) == 2
    assert len(response['text'][1]) == 6
    assert response['text'][0][0] == 'Quick Start with Watson Studio'
    assert response['text'][1][3] == 'but Watson Studio offers all of the frameworks and languages that'


def test_predict_with_numbers():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/text_with_numbers.png'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/png')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()
    assert response['status'] == 'ok'

    assert len(response) == 2
    assert len(response['text'][1]) == 1
    assert '1531752157593' in response['text'][3][0]


def test_predict_jpeg():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'samples/chap4_summary.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpg')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert len(response) == 2
    assert len(response['text'][0]) == 5
    assert response['text'][0][1] == 'Many of its core concepts, however, can be understood with simple'


def test_invalid():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'tests/test.py'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/png')}
        r = requests.post(url=model_endpoint, files=file_form)

    assert r.status_code == 400

    response = r.json()

    assert response['status'] == 'error'
    assert response['message'] == 'The provided input is not a valid image.'


if __name__ == '__main__':
    pytest.main([__file__])
