import requests
from config.settings import settings
from src.common.logger import logger
from src.common.exceptions import PowerBIAuthError

def get_powerbi_embed_token() -> dict:
    try:
        # Step 1: Azure AD OAuth 2.0 Client Credentials Token Call
        auth_url = f"https://login.microsoftonline.com/{settings.powerbi_tenant_id}/oauth2/v2.0/token"
        auth_data = {
            'grant_type': 'client_credentials',
            'client_id': settings.powerbi_client_id,
            'client_secret': settings.powerbi_client_secret,
            'scope': 'https://analysis.windows.net/powerbi/api/.default'
        }
        auth_res = requests.post(auth_url, data=auth_data).json()
        access_token = auth_res.get('access_token')

        if not access_token:
            raise PowerBIAuthError("Failed to acquire Azure AD Access Token.")

        # Step 2: Generate Power BI Embed Token
        embed_endpoint = f"https://api.powerbi.com/v1.0/myorg/groups/{settings.powerbi_workspace_id}/reports/{settings.powerbi_report_id}/GenerateToken"
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {access_token}'}
        embed_res = requests.post(embed_endpoint, headers=headers, json={'accessLevel': 'View'}).json()

        return {
            'embed_token': embed_res.get('token'),
            'embed_url': f"https://app.powerbi.com/reportEmbed?reportId={settings.powerbi_report_id}&groupId={settings.powerbi_workspace_id}"
        }
    except Exception as e:
        logger.error(f"Power BI Embed Auth Error: {str(e)}")
        # Return fallback configuration URL for demo rendering
        return {
            'embed_token': 'DEMO_MODE',
            'embed_url': f"https://app.powerbi.com/groups/bea21302-33aa-4c37-8faa-181a097ef16d/dashboards/97141d63-295d-47ca-b5bf-f13041888294?experience=power-bi&redirectedFromSignup=1"
        }