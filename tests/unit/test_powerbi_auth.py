import pytest
from src.powerbi.auth import get_powerbi_embed_token

def test_powerbi_auth_fallback_rendering(mocker):
    # Mock network failure to verify fallback structure
    mocker.patch("requests.post", side_effect=Exception("Network Timeout"))
    token_data = get_powerbi_embed_token()
    
    assert "embed_token" in token_data
    assert "embed_url" in token_data
    assert "dashboardEmbed" in token_data["embed_url"] or "reportEmbed" in token_data["embed_url"]