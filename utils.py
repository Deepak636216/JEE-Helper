import json
import os
from pathlib import Path
from typing import List, Dict, Optional

class ProblemLoader:
    """Utility class to load and manage JEE physics problems"""

    def __init__(self, problems_dir: str = "Topic_prblm"):
        self.problems_dir = Path(problems_dir)
        self.problems = []
        self.load_all_problems()

    def load_all_problems(self):
        """Load all problems from JSON files in the problems directory"""
        self.problems = []

        if not self.problems_dir.exists():
            return

        for json_file in self.problems_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    problems = json.load(f)
                    if isinstance(problems, list):
                        self.problems.extend(problems)
                    else:
                        self.problems.append(problems)
            except Exception as e:
                print(f"Error loading {json_file}: {e}")

    def get_all_topics(self) -> List[str]:
        """Get unique list of all topics"""
        topics = set()
        for problem in self.problems:
            if 'topic' in problem:
                topics.add(problem['topic'])
        return sorted(list(topics))

    def get_all_chapters(self) -> List[str]:
        """Get unique list of all chapters"""
        chapters = set()
        for problem in self.problems:
            if 'chapter' in problem:
                chapters.add(problem['chapter'])
        return sorted(list(chapters))

    def filter_problems(self,
                       chapter: Optional[str] = None,
                       topic: Optional[str] = None,
                       difficulty: Optional[str] = None) -> List[Dict]:
        """Filter problems by chapter, topic, or difficulty"""
        filtered = self.problems

        if chapter:
            filtered = [p for p in filtered if p.get('chapter') == chapter]

        if topic:
            filtered = [p for p in filtered if p.get('topic') == topic]

        if difficulty:
            filtered = [p for p in filtered if p.get('difficulty') == difficulty]

        return filtered

    def get_problem_by_id(self, problem_id: str) -> Optional[Dict]:
        """Get a specific problem by its ID"""
        for problem in self.problems:
            if problem.get('id') == problem_id:
                return problem
        return None

    def get_total_count(self) -> int:
        """Get total number of problems"""
        return len(self.problems)


def format_problem_text(problem: Dict) -> str:
    """Format problem text for display"""
    text = f"**Problem ID:** {problem.get('id', 'N/A')}\n\n"
    text += f"**Chapter:** {problem.get('chapter', 'N/A')}\n\n"
    text += f"**Topic:** {problem.get('topic', 'N/A')}\n\n"
    text += f"**Difficulty:** {problem.get('difficulty', 'N/A').upper()}\n\n"
    text += f"---\n\n"
    text += f"{problem.get('text', 'Problem text not available')}\n\n"

    return text


def display_options(problem: Dict) -> str:
    """Format options for display"""
    if problem.get('type') == 'objective_single_correct' and 'options' in problem:
        options_text = "**Options:**\n\n"
        for option in problem['options']:
            options_text += f"**({option['id'].upper()})** {option['text']}\n\n"
        return options_text
    return ""
