import asyncio
from typing import Optional, List
from playwright.async_api import async_playwright, Browser, Page
import os
from dotenv import load_dotenv

load_dotenv()

class InstagramAutomationTool:
    """Instagram automation tool using Playwright for browser automation"""
    
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.playwright = None
        
    async def init(self):
        """Initialize browser and page"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=False,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )
        
        # Create new context with viewport settings
        context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        )
        
        self.page = await context.new_page()
        
    async def login(self, username: Optional[str] = None, password: Optional[str] = None):
        """Log in to Instagram using credentials or cookies"""
        if not self.page:
            raise ValueError("Page not initialized")
            
        # Use environment variables if credentials not provided
        username = username or os.getenv('IG_USERNAME')
        password = password or os.getenv('IG_PASSWORD')
        
        if not username or not password:
            raise ValueError("Instagram credentials not provided")
            
        try:
            await self.page.goto("https://www.instagram.com/accounts/login/", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # Fill login form
            username_input = await self.page.query_selector('input[name="username"]')
            password_input = await self.page.query_selector('input[name="password"]')
            
            if username_input and password_input:
                await username_input.fill(username)
                await password_input.fill(password)
                await asyncio.sleep(1)
                
                # Click login button
                login_button = await self.page.query_selector('button[type="submit"]')
                if login_button:
                    await login_button.click()
                    await asyncio.sleep(5)
                    
                    # Handle potential security checks
                    await self._handle_security_checks()
                    
                    print("Login successful")
                    return True
            
            print("Login form elements not found")
            return False
            
        except Exception as e:
            print(f"Login failed: {e}")
            return False
            
    async def _handle_security_checks(self):
        """Handle Instagram security checks and popups"""
        if not self.page:
            return
            
        try:
            # Check for "Save Login Info" prompt
            save_info_button = await self.page.query_selector('button:has-text("Save Info")')
            if save_info_button:
                await save_info_button.click()
                await asyncio.sleep(2)
                
            # Check for notification popup
            not_now_button = await self.page.query_selector('button:has-text("Not Now")')
            if not_now_button:
                await not_now_button.click()
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"Security check handling failed: {e}")
            
    async def _handle_notification_popup(self):
        """Handle Instagram notification popup"""
        if not self.page:
            return
            
        try:
            not_now_selectors = [
                'button:has-text("Not Now")',
                'div:has-text("Not Now")',
                '//button[contains(text(), "Not Now")]',
                '//div[contains(text(), "Not Now")]'
            ]
            
            for selector in not_now_selectors:
                not_now_button = await self.page.query_selector(selector)
                if not_now_button:
                    await not_now_button.click()
                    await asyncio.sleep(1.5)
                    print("Notification popup dismissed")
                    return
                    
            print("'Not Now' button not found in notification dialog")
            
        except Exception as e:
            print(f"No notification popup appeared: {e}")
            
    async def send_direct_message(self, username: str, message: str, media_path: Optional[str] = None):
        """Send a direct message to a user"""
        if not self.page:
            raise ValueError("Page not initialized")
            
        try:
            await self.page.goto(f"https://www.instagram.com/{username}/", wait_until="networkidle")
            await asyncio.sleep(3)
            
            # Find and click message button
            message_button = await self.page.query_selector('button:has-text("Message"), div:has-text("Message")')
            if not message_button:
                raise ValueError("Message button not found")
                
            await message_button.click()
            await asyncio.sleep(2)
            await self._handle_notification_popup()
            
            # Handle media attachment if provided
            if media_path:
                file_input = await self.page.query_selector('input[type="file"]')
                if file_input:
                    await file_input.set_input_files(media_path)
                    await asyncio.sleep(2)
                else:
                    print("File input not found for media attachment")
                    
            # Find message input and send
            message_input_selectors = [
                'textarea[placeholder*="Message"]',
                'div[role="textbox"]',
                'div[contenteditable="true"]'
            ]
            
            message_input = None
            for selector in message_input_selectors:
                message_input = await self.page.query_selector(selector)
                if message_input:
                    break
                    
            if not message_input:
                raise ValueError("Message input not found")
                
            await message_input.fill(message)
            await asyncio.sleep(2)
            
            # Find and click send button
            send_button = await self.page.query_selector('button:has-text("Send"), div:has-text("Send")')
            if send_button:
                await send_button.click()
                print("Message sent successfully")
            else:
                raise ValueError("Send button not found")
                
        except Exception as e:
            print(f"Failed to send DM to {username}: {e}")
            raise
            
    async def interact_with_posts(self, max_posts: int = 20):
        """Like posts and generate AI-powered comments"""
        if not self.page:
            raise ValueError("Page not initialized")
            
        # TODO: Implement post interaction logic
        # This will include:
        # - Scrolling through posts
        # - Liking posts
        # - Generating AI comments using Kortix LLM
        # - Posting comments
        
        print(f"Post interaction for {max_posts} posts not yet implemented")
        
    async def scrape_followers(self, target_account: str, max_followers: int) -> List[str]:
        """Scrape followers from a target account"""
        if not self.page:
            raise ValueError("Page not initialized")
            
        # TODO: Implement follower scraping logic
        print(f"Follower scraping for {target_account} not yet implemented")
        return []
        
    async def close(self):
        """Clean up browser resources"""
        if self.browser:
            await self.browser.close()
            self.browser = None
            self.page = None
            
    # AI Integration Methods (to be implemented with Kortix LLM)
    async def generate_comment(self, post_caption: str) -> str:
        """Generate AI-powered comment using Kortix LLM"""
        # TODO: Integrate with Kortix's LLM system
        # This replaces Riona's Google Gemini integration
        
        prompt = f"""Generate a human-like Instagram comment based on this post: "{post_caption}".
        
        Requirements:
        - Match the tone of the caption (casual, funny, serious, or sarcastic)
        - Sound organic—avoid robotic phrasing or overly perfect grammar
        - Use relatable language with light slang and emojis if appropriate
        - Keep it concise (1-2 sentences max)
        - Avoid generic praise; react specifically to the content
        """
        
        # Placeholder - will be replaced with Kortix LLM call
        return "Great post! 😊👏"
        
async def main():
    """Example usage"""
    tool = InstagramAutomationTool()
    
    try:
        await tool.init()
        
        # Example: Send a test message
        # await tool.send_direct_message("test_user", "Hello from Kortix!")
        
        # Keep browser open for testing
        print("Browser initialized successfully. Press Ctrl+C to exit.")
        await asyncio.sleep(3600)  # Keep open for 1 hour
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await tool.close()

if __name__ == "__main__":
    asyncio.run(main())