import os
import google.generativeai as genai
from typing import List, Dict, Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from config directory
config_dir = Path(__file__).parent.parent.parent.parent / "config"
env_file = config_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)
else:
    # Fallback to root directory
    load_dotenv()

class PhysicsAITutor:
    """Socratic AI tutor for JEE Physics using Google Gemini"""

    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')

        # System prompt for Socratic tutoring
        self.system_prompt = """You are an expert JEE Physics tutor who uses the Socratic method to guide students.

YOUR TEACHING PHILOSOPHY:
- NEVER give direct answers or full solutions in chat
- Ask guiding questions to make students THINK
- Help students discover the solution themselves through dialogue
- Be patient, encouraging, and supportive
- Break down complex problems into smaller steps

YOUR APPROACH:
1. First, ask what the problem is asking them to find
2. Ask about given information and what they know
3. Guide them to identify relevant concepts and formulas
4. Ask questions that lead them toward the solution
5. Validate their thinking when correct
6. Gently redirect when they're off track
7. Provide hints only when truly stuck
8. The student can click "Solution" button to see the full answer - don't provide it in chat

IMPORTANT RULES:
- Use simple, clear language
- Ask ONE question at a time
- Wait for student response before proceeding
- Encourage even partial correct answers
- Connect concepts to real-world examples when helpful
- Keep responses concise (2-4 sentences max)
- Use LaTeX for equations when needed: $equation$
- NEVER write "Complete Solution" or show full step-by-step solutions in your messages
- Guide with questions, not solutions

HINT LEVELS (when student requests):
- Level 1: Gentle nudge about approach ("Think about what's conserved here")
- Level 2: Specific concept ("This involves energy conservation")
- Level 3: Direct guidance ("Use: KE + PE = constant")

Remember: Your goal is to teach THINKING through questions, not to provide answers!"""

    def get_initial_message(self, problem: Dict) -> str:
        """Generate the first tutoring message based on the problem"""

        problem_text = problem.get('text', '')
        problem_type = problem.get('type', 'numerical')
        topic = problem.get('topic', 'Physics')

        prompt = f"""A student has brought this {topic} problem:

"{problem_text}"

This is your first interaction. Greet them warmly and ask your FIRST Socratic question to get them thinking.
Do NOT solve the problem. Just ask what they understand about what's being asked."""

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Hello! I'm your physics tutor. Let's work through this problem together. To start, can you tell me: What is this problem asking you to find?"

    def get_response(self,
                    problem: Dict,
                    conversation_history: List[Dict],
                    user_message: str) -> str:
        """Get AI tutor response based on conversation context"""

        # Build conversation context
        context = self._build_context(problem, conversation_history, user_message)

        try:
            response = self.model.generate_content(context)
            return response.text
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating AI response: {e}", exc_info=True)
            return f"I'm having trouble connecting right now. Let me try to help: Could you explain your thinking so far?"

    def get_hint(self,
                problem: Dict,
                conversation_history: List[Dict],
                hint_level: int) -> str:
        """Generate progressive hints"""

        problem_text = problem.get('text', '')

        hint_prompts = {
            1: "Give a GENTLE hint (Level 1) - just a subtle nudge about the general approach. Don't reveal specifics.",
            2: "Give a MODERATE hint (Level 2) - mention the specific physics concept or principle needed.",
            3: "Give a DIRECT hint (Level 3) - suggest the exact formula or equation to use, but don't solve."
        }

        level = min(hint_level, 3)
        conversation_context = self._format_conversation(conversation_history)

        prompt = f"""{self.system_prompt}

PROBLEM:
{problem_text}

CONVERSATION SO FAR:
{conversation_context}

The student has requested a hint (Level {level}).
{hint_prompts[level]}

Provide the hint in a supportive way that encourages them to keep trying."""

        try:
            response = self.model.generate_content(prompt)
            return f"💡 **Hint {level}:** {response.text}"
        except Exception as e:
            fallback_hints = {
                1: "💡 **Hint 1:** Think about what physical principles or laws apply to this situation.",
                2: "💡 **Hint 2:** Consider what quantities are conserved or what equations relate the given variables.",
                3: "💡 **Hint 3:** Look at the given information - which formula connects these quantities?"
            }
            return fallback_hints.get(level, fallback_hints[1])

    def _build_context(self,
                      problem: Dict,
                      conversation_history: List[Dict],
                      user_message: str) -> str:
        """Build full context for AI model"""

        problem_text = problem.get('text', '')
        topic = problem.get('topic', 'Physics')
        options = problem.get('options', [])

        # Format options if MCQ
        options_text = ""
        if options:
            options_text = "\nOPTIONS:\n"
            for opt in options:
                options_text += f"({opt['id'].upper()}) {opt['text']}\n"

        # Format conversation history
        conversation_context = self._format_conversation(conversation_history)

        context = f"""{self.system_prompt}

PROBLEM ({topic}):
{problem_text}
{options_text}

CONVERSATION SO FAR:
{conversation_context}

STUDENT'S LATEST MESSAGE:
{user_message}

YOUR RESPONSE (remember: ask questions, guide thinking, don't solve directly):"""

        return context

    def _format_conversation(self, conversation_history: List[Dict]) -> str:
        """Format conversation history for context"""

        if not conversation_history:
            return "No conversation yet - this is the first interaction."

        formatted = ""
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            role = "Tutor" if msg['role'] == 'assistant' else "Student"
            formatted += f"{role}: {msg['content']}\n\n"

        return formatted.strip()

    def generate_solution(self, problem: Dict) -> str:
        """Generate complete solution (only after student has tried)"""

        problem_text = problem.get('text', '')
        topic = problem.get('topic', 'Physics')

        # Check if it's a curated problem with official solution
        if 'official_solution' in problem and not problem.get('user_submitted', False):
            return None  # Will use the pre-written solution from JSON

        # Generate solution for user-submitted questions
        # Use a DIFFERENT prompt for solutions (not the Socratic one)
        solution_prompt = f"""You are an expert JEE Physics teacher providing a complete solution.

PROBLEM ({topic}):
{problem_text}

Provide a COMPLETE, STEP-BY-STEP solution using this EXACT markdown structure for better readability:

## What We Need to Find
[1-2 sentences stating the question clearly]

## Given Information
- **Mass 1 (m₁):** [value] kg
- **Velocity 1 (v₁):** [value] m/s
- **Mass 2 (m₂):** [value] kg
[List all given values as bullet points with units]

## Physics Concepts
- **[Concept name]:** Brief explanation
- **Formula:** `equation in code format`
[List key concepts as bullet points]

## Solution Steps

### Step 1: [Clear step title]
- **Formula:** `v = u + at` (use code format for formulas)
- **Substituting values:** 10 = 0 + a(5)
- **Calculation:** a = 10/5 = 2 m/s²
- **Result:** ✅ Acceleration = 2 m/s²

### Step 2: [Next step title]
[Continue with same format]

[Repeat for all steps with clear titles]

## Final Answer
**The [quantity] is [value with units].**

[1 sentence explaining the significance]

## Key Insights
- ✅ [Important concept students should remember]
- ⚠️ [Common mistake to avoid]
- 💡 [Pro tip or additional insight]

IMPORTANT FORMATTING RULES:
- Use ## for main sections (What We Need, Given Info, etc.)
- Use ### for step titles
- Use - for bullet points
- Use ** for bold emphasis
- Use ` ` for formulas and equations
- Use emojis (✅ ⚠️ 💡) for visual cues
- Keep paragraphs short (2-3 sentences max)
- Add blank lines between sections
- Make it scannable and easy to read"""

        try:
            response = self.model.generate_content(solution_prompt)
            return response.text
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error generating solution: {e}", exc_info=True)
            return "I'm having trouble generating the solution right now. Please try again or ask your teacher for help."


# Utility function for quick testing
def test_tutor():
    """Test the AI tutor with a sample problem"""

    sample_problem = {
        'text': 'A ball is thrown from a 45m cliff at 20 m/s horizontally. Find the range.',
        'type': 'numerical',
        'topic': 'Projectile Motion',
        'difficulty': 'medium'
    }

    tutor = PhysicsAITutor()
    print("Initial Message:")
    print(tutor.get_initial_message(sample_problem))
    print("\n" + "="*50 + "\n")

    # Simulate conversation
    conversation = [
        {'role': 'assistant', 'content': 'What is the problem asking you to find?'},
        {'role': 'user', 'content': 'The range of the projectile'}
    ]

    print("Tutor Response:")
    print(tutor.get_response(sample_problem, conversation, "The range of the projectile"))


if __name__ == "__main__":
    test_tutor()
