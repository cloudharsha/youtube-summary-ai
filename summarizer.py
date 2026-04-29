import os
import sys


def summarize_text(transcript, backend=None):
    """
    Summarize transcript text using AI.

    Args:
        transcript: The transcript text to summarize
        backend: 'openai' or 'anthropic' (default: auto-detect from env vars)

    Returns:
        Formatted summary string
    """
    # Auto-detect backend if not specified
    if backend is None:
        if os.getenv('OPENAI_API_KEY'):
            backend = 'openai'
        elif os.getenv('ANTHROPIC_BASE_URL'):
            backend = 'anthropic'
        else:
            raise ValueError(
                "No AI backend configured. Set either OPENAI_API_KEY or "
                "ANTHROPIC_BASE_URL environment variables."
            )

    # Route to appropriate backend
    if backend == 'openai':
        return _summarize_with_openai(transcript)
    elif backend == 'anthropic':
        return _summarize_with_anthropic(transcript)
    else:
        raise ValueError(f"Unknown backend: {backend}")


def _summarize_with_openai(transcript):
    """Summarize using OpenAI API."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes YouTube video transcripts. "
                    "Provide a concise summary with TL;DR, key points, and actionable insights."
                },
                {
                    "role": "user",
                    "content": f"Please summarize this transcript:\n\n{transcript}"
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )

        return response.choices[0].message.content

    except ImportError:
        raise ValueError(
            "OpenAI library not installed. Install with: pip install openai"
        )
    except Exception as e:
        raise ValueError(f"OpenAI API error: {e}")


def _summarize_with_anthropic(transcript):
    """Summarize using Anthropic API (or local LLM)."""
    try:
        from anthropic import Anthropic

        client = Anthropic(
            base_url=os.getenv('ANTHROPIC_BASE_URL'),
            api_key=os.getenv('ANTHROPIC_AUTH_TOKEN', 'freecc')
        )

        # Try streaming first (for local LLM servers that use SSE)
        try:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,  # Increased to allow for both thinking and response
                messages=[
                    {
                        "role": "user",
                        "content": f"Please summarize this YouTube transcript. "
                        f"Provide a concise summary with TL;DR, key points, and actionable insights:\n\n{transcript}"
                    }
                ],
                stream=True
            )

            # Collect the streamed response
            full_text = ""
            for chunk in response:
                if chunk.type == "content_block_delta":
                    # Handle both text and thinking deltas
                    if hasattr(chunk.delta, 'text'):
                        full_text += chunk.delta.text
                    # Note: we ignore thinking deltas as they're internal reasoning

            return full_text if full_text else "No response generated"

        except Exception as stream_error:
            # Fall back to non-streaming if streaming fails
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,  # Increased to allow for both thinking and response
                messages=[
                    {
                        "role": "user",
                        "content": f"Please summarize this YouTube transcript. "
                        f"Provide a concise summary with TL;DR, key points, and actionable insights:\n\n{transcript}"
                    }
                ]
            )

            return response.content[0].text

    except ImportError:
        raise ValueError(
            "Anthropic library not installed. Install with: pip install anthropic"
        )
    except Exception as e:
        raise ValueError(f"Anthropic API error: {e}")