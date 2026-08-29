class AIError(Exception):
    """Base exception for AI-related errors."""


class AIProviderError(AIError):
    """Raised when the AI provider fails."""


class AIConfigurationError(AIError):
    """Raised when the AI provider is incorrectly configured."""