import argparse
import sys
from transcript import get_transcript
from summarizer import summarize_text


def main():
    parser = argparse.ArgumentParser(
        description='Summarize a YouTube video using AI'
    )
    parser.add_argument(
        'url',
        help='YouTube video URL'
    )
    parser.add_argument(
        '--backend',
        choices=['openai', 'anthropic'],
        help='AI backend to use (default: auto-detect from env vars)'
    )

    args = parser.parse_args()

    try:
        # Fetch transcript
        print("Fetching transcript...")
        transcript, video_id = get_transcript(args.url)
        print(f"✓ Transcript fetched (video ID: {video_id})")
        print()

        # Generate summary
        print("Generating summary...")
        summary = summarize_text(transcript, backend=args.backend)
        print("✓ Summary generated")
        print()
        print("=" * 60)
        print()
        print(summary)
        print()
        print("=" * 60)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
