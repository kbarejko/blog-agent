"""
Review Service

Validates article sections for quality (readability, length, style).
"""
import textstat
from typing import Dict, List, Optional


class ReviewService:
    """Review article sections for quality"""

    def __init__(self, config: Optional[Dict[str, any]] = None):
        """
        Initialize review service

        Config:
            min_words: Minimum words per section (default: 300)
            max_words: Maximum words per section (default: 400)
            min_flesch: Minimum Flesch score (default: 40)
            max_flesch: Maximum Flesch score (default: 60)
        """
        config = config or {}
        self.min_words = config.get('min_words', 300)
        self.max_words = config.get('max_words', 400)
        self.min_flesch = config.get('min_flesch', 40)
        self.max_flesch = config.get('max_flesch', 60)

    def count_words(self, text: str) -> int:
        """Count words in text"""
        # Simple word count - split by whitespace
        return len(text.split())

    def calculate_flesch_reading_ease(self, text: str) -> float:
        """
        Calculate Flesch Reading Ease score

        Returns:
            Score (0-100, higher = easier to read)
        """
        try:
            # Use textstat library
            score = textstat.flesch_reading_ease(text)
            return score
        except:
            # If calculation fails, return neutral score
            return 50.0

    def review_section(self, content: str) -> Dict[str, any]:
        """
        Review a section for quality

        Args:
            content: Section content

        Returns:
            Review result with issues and metrics
        """
        issues = []
        metrics = {}

        # Word count
        word_count = self.count_words(content)
        metrics['word_count'] = word_count

        if word_count < self.min_words:
            issues.append(f"Too short: {word_count} words (min {self.min_words})")
        elif word_count > self.max_words:
            issues.append(f"Too long: {word_count} words (max {self.max_words})")

        # Flesch Reading Ease
        flesch = self.calculate_flesch_reading_ease(content)
        metrics['flesch_score'] = flesch

        if flesch < self.min_flesch:
            issues.append(f"Too complex: Flesch {flesch:.1f} (min {self.min_flesch})")
        elif flesch > self.max_flesch:
            issues.append(f"Too simple: Flesch {flesch:.1f} (max {self.max_flesch})")

        # Check for empty paragraphs
        paragraphs = [p.strip() for p in content.split('\n\n') if p.strip()]
        if len(paragraphs) < 2:
            issues.append("Section should have multiple paragraphs")

        metrics['paragraph_count'] = len(paragraphs)

        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'metrics': metrics
        }

    def generate_review_feedback(self, review_result: Dict[str, any]) -> str:
        """
        Generate human-readable feedback from review result

        Args:
            review_result: Result from review_section()

        Returns:
            Feedback string for AI to fix issues
        """
        if review_result['valid']:
            return "✅ Sekcja spełnia wymagania jakościowe."

        metrics = review_result['metrics']
        issues = review_result['issues']

        feedback_lines = ["❌ Sekcja wymaga poprawek:\n"]

        for issue in issues:
            feedback_lines.append(f"- {issue}")

        feedback_lines.append(f"\n**Metryki:**")
        feedback_lines.append(f"- Liczba słów: {metrics['word_count']}")
        feedback_lines.append(f"- Flesch Reading Ease: {metrics['flesch_score']:.1f}")
        feedback_lines.append(f"- Liczba akapitów: {metrics['paragraph_count']}")

        feedback_lines.append(f"\n**Jak poprawić:**")
        for issue in issues:
            if "Too short" in issue:
                feedback_lines.append("- Rozwiń sekcję: dodaj więcej szczegółów, przykłady, kontekst")
            elif "Too long" in issue:
                feedback_lines.append("- Skróć sekcję: usuń redundancje, podziel na mniejsze akapity")
            elif "Too complex" in issue:
                feedback_lines.append("- Uprość język: krótsze zdania, prostsze słowa, więcej akapitów")
            elif "Too simple" in issue:
                feedback_lines.append("- Wzbogać treść: dodaj detale eksperckie, terminologię branżową")

        return "\n".join(feedback_lines)

    def review_article_draft(self, draft_content: str) -> Dict[str, any]:
        """
        Review entire article draft

        Args:
            draft_content: Full draft content

        Returns:
            Review result
        """
        total_words = self.count_words(draft_content)
        flesch = self.calculate_flesch_reading_ease(draft_content)

        return {
            'total_words': total_words,
            'flesch_score': flesch,
            'metrics': {
                'word_count': total_words,
                'flesch_score': flesch
            }
        }

    def check_headings(self, content: str) -> List[Dict[str, str]]:
        """
        Extract and check heading structure

        Args:
            content: Article content

        Returns:
            List of headings with levels
        """
        headings = []
        lines = content.split('\n')

        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                # Count # symbols
                level = 0
                while level < len(line) and line[level] == '#':
                    level += 1

                # Get heading text
                text = line[level:].strip()

                headings.append({
                    'level': level,
                    'text': text
                })

        return headings

    def validate_heading_structure(self, headings: List[Dict[str, str]]) -> List[str]:
        """
        Validate heading hierarchy

        Args:
            headings: List of headings from check_headings()

        Returns:
            List of issues
        """
        issues = []

        if not headings:
            return ["No headings found"]

        # Check if first heading is H1
        if headings[0]['level'] != 1:
            issues.append("First heading should be H1")

        # Check for heading level jumps (e.g., H2 -> H4)
        for i in range(1, len(headings)):
            prev_level = headings[i-1]['level']
            curr_level = headings[i]['level']

            if curr_level > prev_level + 1:
                issues.append(f"Heading level jump: H{prev_level} -> H{curr_level} (line: '{headings[i]['text']}')")

        return issues
