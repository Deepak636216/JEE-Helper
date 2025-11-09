import streamlit as st
from utils import ProblemLoader, format_problem_text, display_options
from ai_tutor import PhysicsAITutor
import os

# Page configuration
st.set_page_config(
    page_title="JEE Physics AI Tutor",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'problem_loader' not in st.session_state:
    st.session_state.problem_loader = ProblemLoader()

if 'selected_problem' not in st.session_state:
    st.session_state.selected_problem = None

if 'show_solution' not in st.session_state:
    st.session_state.show_solution = False

if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []

if 'hint_level' not in st.session_state:
    st.session_state.hint_level = 0

# User question state
if 'user_question' not in st.session_state:
    st.session_state.user_question = None

if 'question_submitted' not in st.session_state:
    st.session_state.question_submitted = False

# AI Tutor instance
if 'ai_tutor' not in st.session_state:
    try:
        st.session_state.ai_tutor = PhysicsAITutor()
        st.session_state.ai_enabled = True
    except Exception as e:
        st.session_state.ai_tutor = None
        st.session_state.ai_enabled = False
        st.session_state.ai_error = str(e)

# Main title
st.title("🧠 JEE Physics AI Tutor")
st.markdown("### Learn Physics Through Socratic Dialogue")

# Sidebar
with st.sidebar:
    st.header("📚 How to Use")

    st.markdown("""
    ### 🎯 Steps:
    1. **Enter your physics question** in the main area
    2. **Add options** (for MCQ) or expected answer type
    3. **Click "Start Learning"** to begin
    4. **Chat with AI** tutor who guides you
    5. **Request hints** when stuck
    6. **Discover the solution** yourself!
    """)

    st.markdown("---")

    st.subheader("💡 Sample Topics")
    st.markdown("""
    - Laws of Motion
    - Projectile Motion
    - Work & Energy
    - Rotation
    - Center of Mass
    - Friction & Forces
    """)

    st.markdown("---")

    # Reset button
    if st.button("🔄 Start New Question", use_container_width=True):
        st.session_state.user_question = None
        st.session_state.question_submitted = False
        st.session_state.selected_problem = None
        st.session_state.show_solution = False
        st.session_state.chat_messages = []
        st.session_state.hint_level = 0
        st.rerun()

    st.markdown("---")

    # Optional: Sample problems from database
    loader = st.session_state.problem_loader
    if loader.get_total_count() > 0:
        st.subheader("📋 Or Try Sample Problems")
        st.caption(f"{loader.get_total_count()} curated problems available")

        with st.expander("Browse Sample Problems"):
            topics = loader.get_all_topics()
            for topic in topics[:5]:  # Show first 5 topics
                problems = loader.filter_problems(topic=topic)
                if problems and len(problems) > 0:
                    st.markdown(f"**{topic}** ({len(problems)})")
                    if st.button(f"Load {topic} example", key=f"sample_{topic}"):
                        st.session_state.selected_problem = problems[0]
                        st.session_state.question_submitted = True
                        st.session_state.show_solution = False
                        st.session_state.chat_messages = []
                        st.session_state.hint_level = 0
                        st.rerun()

# Main content area
# Check if question is submitted (either user input or sample problem)
if st.session_state.question_submitted or st.session_state.selected_problem:
    problem = st.session_state.selected_problem or st.session_state.user_question

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Your Question")

        # Display question text
        st.markdown(f"**Topic:** {problem.get('topic', 'General Physics')}")
        st.markdown(f"**Difficulty:** {problem.get('difficulty', 'medium').upper()}")
        st.markdown("---")
        st.markdown(problem.get('text', 'Question not available'))
        st.markdown("")

        # Display options if multiple choice
        if problem.get('type') == 'objective_single_correct' and 'options' in problem:
            st.markdown("**Options:**")
            for option in problem['options']:
                st.markdown(f"**({option['id'].upper()})** {option['text']}")
            st.markdown("")

        # Show additional metadata only for pre-loaded problems
        if not problem.get('user_submitted', False):
            # Problem metadata
            with st.expander("📊 Problem Details"):
                st.markdown(f"**Exam:** {problem.get('exam', 'N/A')}")
                st.markdown(f"**Year:** {problem.get('year', 'N/A')}")
                st.markdown(f"**Marks:** {problem.get('marks', 'N/A')}")

                if 'ncert_mapping' in problem:
                    ncert = problem['ncert_mapping']
                    st.markdown(f"**NCERT Class:** {ncert.get('class', 'N/A')}")
                    st.markdown(f"**NCERT Chapter:** {ncert.get('chapter', 'N/A')}")
                    st.markdown(f"**Relevant Sections:** {', '.join(ncert.get('relevant_sections', []))}")

            # Concepts and formulas
            with st.expander("💡 Concepts Required"):
                if 'concepts_required' in problem:
                    for concept in problem['concepts_required']:
                        st.markdown(f"- {concept}")
                else:
                    st.info("AI will identify concepts during tutoring")

            with st.expander("📐 Formulas Used"):
                if 'formulas_used' in problem:
                    for formula in problem['formulas_used']:
                        st.markdown(f"- `{formula}`")
                else:
                    st.info("AI will guide you to discover formulas")
        else:
            st.info("💡 AI tutor will help you identify concepts, formulas, and approach during the conversation!")

    with col2:
        st.header("💬 AI Tutor Chat")

        # Chat interface
        chat_container = st.container()

        with chat_container:
            # Check if AI is enabled
            if not st.session_state.ai_enabled:
                st.error(f"⚠️ AI Tutor not available: {st.session_state.get('ai_error', 'API key missing')}")
                st.info("Please add your GOOGLE_API_KEY to a .env file to enable AI tutoring.")
                st.code("GOOGLE_API_KEY=your_key_here", language="bash")

            # Initialize chat with AI's first message
            if len(st.session_state.chat_messages) == 0 and st.session_state.ai_enabled:
                initial_msg = st.session_state.ai_tutor.get_initial_message(problem)
                st.session_state.chat_messages.append({
                    "role": "assistant",
                    "content": initial_msg
                })

            # Display chat messages
            for message in st.session_state.chat_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        # User input
        user_input = st.chat_input("Type your answer or question here...", disabled=not st.session_state.ai_enabled)

        if user_input and st.session_state.ai_enabled:
            # Add user message
            st.session_state.chat_messages.append({
                "role": "user",
                "content": user_input
            })

            # Get AI response
            with st.spinner("Thinking..."):
                ai_response = st.session_state.ai_tutor.get_response(
                    problem=problem,
                    conversation_history=st.session_state.chat_messages,
                    user_message=user_input
                )

            st.session_state.chat_messages.append({
                "role": "assistant",
                "content": ai_response
            })

            st.rerun()

        # Action buttons
        st.markdown("---")

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            hint_disabled = not st.session_state.ai_enabled or st.session_state.hint_level >= 3
            if st.button("💡 Request Hint", use_container_width=True, disabled=hint_disabled):
                if st.session_state.ai_enabled:
                    st.session_state.hint_level += 1

                    with st.spinner("Generating hint..."):
                        hint_msg = st.session_state.ai_tutor.get_hint(
                            problem=problem,
                            conversation_history=st.session_state.chat_messages,
                            hint_level=st.session_state.hint_level
                        )

                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": hint_msg
                    })

                    if st.session_state.hint_level >= 3:
                        st.session_state.chat_messages.append({
                            "role": "assistant",
                            "content": "You've used all 3 hints! Would you like to see the complete solution?"
                        })

                    st.rerun()

        with col_b:
            if st.button("📖 Show Solution", use_container_width=True):
                st.session_state.show_solution = True
                st.rerun()

        with col_c:
            if st.button("🔄 Reset Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.hint_level = 0
                st.session_state.show_solution = False
                st.rerun()

        # Display solution if requested
        if st.session_state.show_solution:
            st.markdown("---")
            st.header("✅ Complete Solution")

            # Check if this is a curated problem with official solution
            if 'official_solution' in problem and not problem.get('user_submitted', False):
                solution = problem['official_solution']

                if 'steps' in solution:
                    for step in solution['steps']:
                        with st.expander(f"Step {step['step_number']}: {step['description']}", expanded=True):
                            st.markdown(f"**Formula:** `{step.get('formula', 'N/A')}`")
                            st.markdown(f"**Calculation:** {step.get('calculation', 'N/A')}")
                            st.markdown(f"**Explanation:** {step.get('explanation', 'N/A')}")
                            if 'result' in step:
                                st.success(f"**Result:** {step['result']}")

                if 'answer_justification' in solution:
                    st.success(f"**Answer:** {solution['answer_justification']}")

                # Common mistakes
                if 'common_mistakes' in problem:
                    st.markdown("---")
                    st.subheader("⚠️ Common Mistakes to Avoid")
                    for mistake in problem['common_mistakes']:
                        st.warning(f"**Mistake:** {mistake['mistake']}\n\n**Correct Approach:** {mistake['correct_approach']}")

            # Generate solution for user-submitted questions
            elif st.session_state.ai_enabled:
                with st.spinner("Generating complete solution..."):
                    solution_text = st.session_state.ai_tutor.generate_solution(problem)

                if solution_text:
                    st.markdown(solution_text)
                else:
                    st.info("Solution generation is not available for this problem.")
            else:
                st.warning("AI is not enabled. Please add your API key to see AI-generated solutions.")

else:
    # Question input form
    st.header("📝 Enter Your Physics Question")

    st.markdown("""
    Paste any JEE Physics question below. The AI tutor will guide you through solving it using the Socratic method!
    """)

    with st.form("question_form"):
        # Question text
        question_text = st.text_area(
            "Question Text",
            placeholder="Example: A ball is thrown from a 45m cliff at 20 m/s horizontally. Find the range.",
            height=150,
            help="Copy-paste your physics problem here"
        )

        # Question type
        col_a, col_b = st.columns(2)

        with col_a:
            question_type = st.selectbox(
                "Question Type",
                ["Multiple Choice (MCQ)", "Numerical Answer", "Descriptive"],
                help="Select the type of question"
            )

        with col_b:
            difficulty = st.selectbox(
                "Difficulty (Optional)",
                ["Not Sure", "Easy", "Medium", "Hard"]
            )

        # Options for MCQ
        if question_type == "Multiple Choice (MCQ)":
            st.markdown("**Options:**")
            col1, col2 = st.columns(2)

            with col1:
                option_a = st.text_input("Option A", placeholder="Enter option A")
                option_b = st.text_input("Option B", placeholder="Enter option B")

            with col2:
                option_c = st.text_input("Option C", placeholder="Enter option C")
                option_d = st.text_input("Option D", placeholder="Enter option D")

        # Additional context
        with st.expander("➕ Add Additional Context (Optional)"):
            topic = st.text_input(
                "Topic/Chapter",
                placeholder="e.g., Projectile Motion, Laws of Motion",
                help="This helps the AI provide better guidance"
            )

            given_info = st.text_area(
                "Given Information",
                placeholder="What data is provided in the question?",
                height=100
            )

        # Submit button
        submitted = st.form_submit_button("🚀 Start Learning with AI Tutor", use_container_width=True)

        if submitted:
            if question_text.strip():
                # Create problem object from user input
                user_problem = {
                    'text': question_text,
                    'type': 'objective_single_correct' if question_type == "Multiple Choice (MCQ)" else 'numerical',
                    'difficulty': difficulty.lower() if difficulty != "Not Sure" else "medium",
                    'topic': topic if topic else "General Physics",
                    'user_submitted': True
                }

                # Add options if MCQ
                if question_type == "Multiple Choice (MCQ)":
                    options = []
                    if option_a:
                        options.append({'id': 'a', 'text': option_a})
                    if option_b:
                        options.append({'id': 'b', 'text': option_b})
                    if option_c:
                        options.append({'id': 'c', 'text': option_c})
                    if option_d:
                        options.append({'id': 'd', 'text': option_d})

                    user_problem['options'] = options

                # Store in session state
                st.session_state.user_question = user_problem
                st.session_state.question_submitted = True
                st.session_state.chat_messages = []
                st.session_state.hint_level = 0
                st.session_state.show_solution = False

                st.success("Question submitted! Let's start learning!")
                st.rerun()
            else:
                st.error("Please enter a question first!")

    st.markdown("---")

    # Example questions
    st.subheader("💡 Example Questions You Can Try")

    examples = [
        "A projectile is launched at 30° with velocity 50 m/s. Find maximum height.",
        "Two blocks of mass 2kg and 3kg connected by a string. Find tension when pulled with 10N force.",
        "A wheel of radius 0.5m rotates at 120 rpm. Find angular velocity."
    ]

    for idx, example in enumerate(examples):
        st.markdown(f"**{idx+1}.** {example}")

    st.markdown("---")

    st.info("👈 Check the sidebar for quick tips and sample problems!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for JEE aspirants | Powered by AI")
