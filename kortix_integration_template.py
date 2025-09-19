"""
Kortix Integration Template for Instagram Automation Tool
This shows how the Instagram automation would integrate with Kortix's tool system
"""

from agentpress.tool import ToolResult, openapi_schema, usage_example
from agentpress.thread_manager import ThreadManager
from sandbox.tool_base import SandboxToolsBase
from utils.logger import logger
from typing import Optional, Dict, Any
import asyncio

class InstagramAutomationTool(SandboxToolsBase):
    """
    Instagram Automation Tool for Kortix Platform
    
    Provides Instagram automation capabilities including:
    - Direct messaging with media attachments
    - Post interaction (liking and AI-powered commenting)
    - Follower scraping and analysis
    - Session management with cookie persistence
    """
    
    def __init__(self, project_id: str, thread_id: str, thread_manager: ThreadManager):
        super().__init__(project_id, thread_manager)
        self.thread_id = thread_id
        self.instagram_client = None
        
    async def _ensure_instagram_client(self):
        """Ensure Instagram client is initialized"""
        if not self.instagram_client:
            # Import here to avoid circular imports
            from instagram_tool import InstagramAutomationTool as Client
            self.instagram_client = Client()
            await self.instagram_client.init()
            
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "instagram_send_direct_message",
            "description": "Send a direct message to an Instagram user",
            "parameters": {
                "type": "object",
                "properties": {
                    "username": {
                        "type": "string",
                        "description": "Instagram username to send message to"
                    },
                    "message": {
                        "type": "string",
                        "description": "Message content to send"
                    },
                    "media_path": {
                        "type": "string",
                        "description": "Optional path to media file to attach"
                    }
                },
                "required": ["username", "message"]
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="instagram_send_direct_message">
        <parameter name="username">target_user</parameter>
        <parameter name="message">Hello! Check out our new product 🚀</parameter>
        </invoke>
        </function_calls>
        
        <function_calls>
        <invoke name="instagram_send_direct_message">
        <parameter name="username">influencer123</parameter>
        <parameter name="message">Love your content! Would you be interested in collaboration?</parameter>
        <parameter name="media_path">/workspace/media/collaboration_offer.pdf</parameter>
        </invoke>
        </function_calls>
        ''')
    async def instagram_send_direct_message(self, username: str, message: str, media_path: Optional[str] = None) -> ToolResult:
        """Send a direct message to an Instagram user"""
        try:
            await self._ensure_instagram_client()
            await self.instagram_client.send_direct_message(username, message, media_path)
            
            return self.success_response({
                "message": f"Message sent successfully to {username}",
                "username": username,
                "message_content": message,
                "media_attached": media_path is not None
            })
            
        except Exception as e:
            logger.error(f"Failed to send Instagram DM: {e}")
            return self.fail_response(f"Failed to send message: {str(e)}")
            
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "instagram_interact_with_posts",
            "description": "Like posts and generate AI-powered comments on Instagram feed",
            "parameters": {
                "type": "object",
                "properties": {
                    "max_posts": {
                        "type": "number",
                        "description": "Maximum number of posts to interact with",
                        "default": 20
                    },
                    "target_account": {
                        "type": "string",
                        "description": "Specific account to interact with (optional)"
                    }
                }
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="instagram_interact_with_posts">
        <parameter name="max_posts">10</parameter>
        <parameter name="target_account">tech_influencer</parameter>
        </invoke>
        </function_calls>
        ''')
    async def instagram_interact_with_posts(self, max_posts: int = 20, target_account: Optional[str] = None) -> ToolResult:
        """Like posts and generate AI-powered comments"""
        try:
            await self._ensure_instagram_client()
            
            if target_account:
                # Navigate to specific account first
                await self.instagram_client.page.goto(f"https://www.instagram.com/{target_account}/")
                await asyncio.sleep(3)
                
            await self.instagram_client.interact_with_posts(max_posts)
            
            return self.success_response({
                "message": f"Interacted with {max_posts} posts successfully",
                "target_account": target_account,
                "posts_processed": max_posts
            })
            
        except Exception as e:
            logger.error(f"Failed to interact with posts: {e}")
            return self.fail_response(f"Failed to interact with posts: {str(e)}")
            
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "instagram_scrape_followers",
            "description": "Scrape followers from a target Instagram account",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_account": {
                        "type": "string",
                        "description": "Instagram username to scrape followers from"
                    },
                    "max_followers": {
                        "type": "number",
                        "description": "Maximum number of followers to scrape",
                        "default": 100
                    }
                },
                "required": ["target_account"]
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="instagram_scrape_followers">
        <parameter name="target_account">popular_brand</parameter>
        <parameter name="max_followers">50</parameter>
        </invoke>
        </function_calls>
        ''')
    async def instagram_scrape_followers(self, target_account: str, max_followers: int = 100) -> ToolResult:
        """Scrape followers from a target Instagram account"""
        try:
            await self._ensure_instagram_client()
            followers = await self.instagram_client.scrape_followers(target_account, max_followers)
            
            # Store followers in Kortix database
            # TODO: Implement Kortix database integration
            
            return self.success_response({
                "message": f"Successfully scraped {len(followers)} followers from {target_account}",
                "target_account": target_account,
                "followers_count": len(followers),
                "followers": followers[:10],  # Return first 10 for preview
                "total_available": f"{len(followers)}/{max_followers}"
            })
            
        except Exception as e:
            logger.error(f"Failed to scrape followers: {e}")
            return self.fail_response(f"Failed to scrape followers: {str(e)}")
            
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "instagram_generate_comment",
            "description": "Generate AI-powered comment for an Instagram post using Kortix LLM",
            "parameters": {
                "type": "object",
                "properties": {
                    "post_caption": {
                        "type": "string",
                        "description": "The caption/text of the Instagram post"
                    },
                    "tone": {
                        "type": "string",
                        "description": "Desired tone for the comment",
                        "enum": ["casual", "funny", "serious", "sarcastic", "enthusiastic"],
                        "default": "casual"
                    }
                },
                "required": ["post_caption"]
            }
        }
    })
    @usage_example('''
        <function_calls>
        <invoke name="instagram_generate_comment">
        <parameter name="post_caption">Just launched our new product! So excited to share this with everyone 🚀 #innovation</parameter>
        <parameter name="tone">enthusiastic</parameter>
        </invoke>
        </function_calls>
        ''')
    async def instagram_generate_comment(self, post_caption: str, tone: str = "casual") -> ToolResult:
        """Generate AI-powered comment using Kortix LLM"""
        try:
            # TODO: Integrate with Kortix's LLM system
            # This would replace the placeholder implementation
            
            prompt = f"""Generate a human-like Instagram comment based on this post: "{post_caption}".
            
            Tone: {tone}
            Requirements:
            - Sound organic and authentic
            - Use appropriate emojis and casual language
            - 1-2 sentences maximum
            - React specifically to the post content
            """
            
            # Placeholder - will be replaced with Kortix LLM integration
            comment = "This looks amazing! Can't wait to try it out 🚀👏"
            
            return self.success_response({
                "message": "Comment generated successfully",
                "generated_comment": comment,
                "post_caption_preview": post_caption[:100] + "..." if len(post_caption) > 100 else post_caption,
                "tone": tone
            })
            
        except Exception as e:
            logger.error(f"Failed to generate comment: {e}")
            return self.fail_response(f"Failed to generate comment: {str(e)}")
            
    async def close(self):
        """Clean up resources"""
        if self.instagram_client:
            await self.instagram_client.close()
            self.instagram_client = None