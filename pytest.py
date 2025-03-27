import pytest
import json
from unittest.mock import patch, MagicMock
from cryptography.hazmat.primitives.asymmetric import rsa, ec
from cryptography.hazmat.primitives import serialization
from flask import template_rendered
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../gpgweb')))
from main import app, generate_key

# Import the function we want to test using absolute import


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestGenerateKey:
    """Test cases for generate_key function"""
    
    def test_generate_rsa_key(self):
        """Test RSA key generation with default parameters"""
        key, private_pem = generate_key(2048, 'rsa')
        
        # Verify key type
        assert isinstance(key, rsa.RSAPrivateKey)
        
        # Verify the private key is properly formatted
        assert private_pem.startswith(b'-----BEGIN PRIVATE KEY-----')
        assert private_pem.endswith(b'-----END PRIVATE KEY-----\n')

    def test_generate_ecdsa_key(self):
        """Test ECDSA key generation"""
        key, private_pem = generate_key(256, 'ecdsa')
        
        # Verify key type
        assert isinstance(key, ec.EllipticCurvePrivateKey)
        
        # Verify the private key is properly formatted
        assert private_pem.startswith(b'-----BEGIN PRIVATE KEY-----')
        assert private_pem.endswith(b'-----END PRIVATE KEY-----\n')

    def test_invalid_key_type(self):
        """Test error handling for invalid key type"""
        with pytest.raises(ValueError) as excinfo:
            generate_key(2048, 'invalid_type')
        
        assert "Unsupported key type" in str(excinfo.value)
        

class TestFlaskRoutes:
    """Test cases for Flask routes"""
    
    @patch('gpgweb.main.format_public_key')
    def test_generate_key_route(self, mock_format_public_key, client):
        """Test the generate-key endpoint"""
        # Mock the format_public_key function
        mock_public_key = b'ssh-rsa AAAAB3NzaC1yc2EAAAA...'
        mock_format_public_key.return_value = mock_public_key
        
        # Test data
        test_data = {
            'keyCode': 2048,
            'keyType': 'rsa',
            'publicKeyFormat': 'openssh'
        }
        
        # Send request
        response = client.post('/generate-key', 
                             json=test_data,
                             content_type='application/json')
        
        # Check response
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Verify response structure
        assert 'privateKey' in data
        assert 'publicKey' in data
        assert data['publicKey'] == mock_public_key.decode('utf-8')
        assert mock_format_public_key.called
    
    @patch('gpgweb.main.render_template')
    def test_index_route(self, mock_render_template, client):
        """Test the index route"""
        mock_render_template.return_value = "index page"
        
        response = client.get('/')
        
        assert response.status_code == 200
        mock_render_template.assert_called_once_with('index.html')


if __name__ == '__main__':
    pytest.main()

'''Test Plan:
Test generate_key function:

RSA key generation with different key sizes
ECDSA key generation
Error handling for invalid key types
Check structure of returned values
Test Flask routes:

/generate-key endpoint
Index route'''