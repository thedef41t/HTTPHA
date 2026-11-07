from playwright.sync_api import sync_playwright, Error as PlaywrightError

def send_request(target_url: str) -> dict:
    
    with sync_playwright() as spr:

        browser = spr.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page = context.new_page()
        
        status_code = 0
        headers = {}

        try:
            response = page.goto(target_url, timeout=50000)
            if response is not None:
                status_code = response.status
                headers = response.all_headers()
        except PlaywrightError as error:
            print(f"Error sending request: {error}")
            print()
        finally:
            context.close()
            browser.close()
        
        return {
            "status_code": status_code,
            "headers": headers
        }
