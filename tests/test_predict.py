import sys
from pathlib import Path
from unittest.mock import MagicMock

# Mock heavy dependencies before importing the app
mock_session = MagicMock()
mock_session.run.return_value = [[ [0.0, 1.0] ]]
ort_mock = MagicMock()
ort_mock.InferenceSession.return_value = mock_session
sys.modules['onnxruntime'] = ort_mock

class DummyScaler:
    def transform(self, X):
        import numpy as np
        return np.array(X)

joblib_mock = MagicMock()
joblib_mock.load.return_value = DummyScaler()
sys.modules['joblib'] = joblib_mock

import numpy as np
np.load = lambda *args, **kwargs: np.array(["class0", "class1"])

sys.path.append(str(Path(__file__).resolve().parents[1] / 'elk-stack' / 'ml-api'))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_endpoint():
    response = client.post('/predict', json={'log': {'Dst Port': 80}})
    assert response.status_code == 200
    data = response.json()
    assert 'predicted_class' in data
    assert 'class_name' in data


def test_missing_log_returns_422():
    response = client.post('/predict', json={})
    assert response.status_code == 422


def test_numeric_string_coerced():
    response = client.post('/predict', json={'log': {'Dst Port': '80'}})
    assert response.status_code == 200
    data = response.json()
    assert 'predicted_class' in data


def test_invalid_numeric_value_returns_error():
    response = client.post('/predict', json={'log': {'Dst Port': 'abc'}})
    assert response.status_code == 200
    data = response.json()
    assert 'error' in data
