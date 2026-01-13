"""
Utility functions for the ToolChain platform.

This module provides helper functions used across the application:
- Text processing and formatting
- Data validation
- Common conversions
"""

import re
from typing import Any


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug.
    
    Args:
        text: Input text to slugify
        
    Returns:
        Lowercase slug with hyphens
        
    Example:
        >>> slugify("Hello World!")
        'hello-world'
    """
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def truncate(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to max length with suffix.
    
    Args:
        text: Text to truncate
        max_length: Maximum length including suffix
        suffix: String to append when truncated
        
    Returns:
        Truncated text or original if shorter
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix


def safe_get(data: dict[str, Any], key: str, default: Any = None) -> Any:
    """Safely get nested dictionary value.
    
    Args:
        data: Dictionary to search
        key: Dot-separated key path (e.g., "user.profile.name")
        default: Default value if not found
        
    Returns:
        Value at key path or default
    """
    keys = key.split('.')
    value = data
    
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, default)
        else:
            return default
    
    return value


def format_tool_summary(tool: dict[str, Any]) -> str:
    """Format a tool dict into a readable summary.
    
    Args:
        tool: Tool dictionary with name, category, description
        
    Returns:
        Formatted multi-line string
    """
    name = tool.get('name', 'Unknown')
    category = tool.get('category', 'Uncategorized')
    description = tool.get('description', 'No description')
    pricing = tool.get('pricing', 'Unknown pricing')
    
    return f"""
{name} ({category})
{'-' * len(name)}
{truncate(description, 200)}
Pricing: {pricing}
""".strip()


def parse_query_intent(query: str) -> dict[str, Any]:
    """Parse user query to extract intent signals.
    
    Args:
        query: Raw user query string
        
    Returns:
        Dict with detected intents
    """
    query_lower = query.lower()
    
    intent = {
        'is_comparison': any(w in query_lower for w in ['vs', 'versus', 'compare', 'difference']),
        'is_recommendation': any(w in query_lower for w in ['best', 'recommend', 'should i use', 'which']),
        'is_definition': any(w in query_lower for w in ['what is', 'what are', 'explain', 'how does']),
        'wants_free': 'free' in query_lower,
        'wants_open_source': 'open source' in query_lower or 'opensource' in query_lower,
    }
    
    return intent


def validate_tool_data(tool: dict[str, Any]) -> list[str]:
    """Validate tool data structure.
    
    Args:
        tool: Tool dictionary to validate
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    required_fields = ['name', 'category', 'description']
    for field in required_fields:
        if not tool.get(field):
            errors.append(f"Missing required field: {field}")
    
    if tool.get('name') and len(tool['name']) > 100:
        errors.append("Tool name exceeds 100 characters")
    
    if tool.get('description') and len(tool['description']) < 10:
        errors.append("Description too short (min 10 characters)")
    
    valid_categories = ['LLM', 'RAG', 'Vector DB', 'Framework', 'API', 'SDK', 'Other']
    if tool.get('category') and tool['category'] not in valid_categories:
        errors.append(f"Invalid category. Must be one of: {valid_categories}")
    
    return errors
