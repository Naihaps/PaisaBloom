
import streamlit as st
import pandas as pd
import random
from datetime import date

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="PaisaBloom",
    page_icon="🌸",
    layout="wide"
)

# ---------------- CUTE PASTEL THEME ----------------
st.markdown("""
<style>
.stApp {
    background-color: #fff5fa;
}
h1, h2, h3 {
    color: #b34f87;
}
div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #f2cfe1;
    border-radius: 18px;
    padding: 15px;
}
.stButton > button {
    background-color: #edb4d0;
    color: #642c4e;
    border-radius: 15px;
    border: none;
    font-weight: bold;
}
.stButton > button:hover {
    background-color: #d88bb5;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION DATA ----------------
defaults = {
    "transactions": [],
    "budget": 5000.0,
    "budget_period": "Monthly",
    "goal_name": "My Dream",
    "goal_target": 2000.0,
    "goal_saved": 0.0,
    "points": 0,
    "completed_challenges": [],
    "challenge": "Save ₹20 today.",
    "quiz_index": 0,
    "quiz_score": 0,
    "quiz_feedback": "",
    "quiz_finished": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------------- CALCULATIONS ----------------
df = pd.DataFrame(
    st.session_state.transactions,
    columns=["Date", "Type", "Category", "Description", "Amount"]
)

income = (
    df.loc[df["Type"] == "Income", "Amount"].sum()
    if not df.empty else 0
)
expenses = (
    df.loc[df["Type"] == "Expense", "Amount"].sum()
    if not df.empty else 0
)
balance = income - expenses

# ---------------- SIDEBAR ----------------
st.sidebar.title("🌸 PaisaBloom")
st.sidebar.caption("Spend Smart. Save More. Bloom Brighter.")

page = st.sidebar.radio(
    "Explore",
    [
        "🏠 My Space",
        "💳 Money Activity",
        "🎯 Dream Fund",
        "🌱 Daily Challenge",
        "📊 Money Insights",
        "🧠 Money Quiz"
    ]
)

st.sidebar.markdown("---")
st.sidebar.metric("⭐ Bloom Points", st.session_state.points)
st.sidebar.caption("A little saving goes a long way!")

# ---------------- HOME ----------------
if page == "🏠 My Space":
    st.title("🌷 Welcome to PaisaBloom!")
    st.write("Your cute space to manage money and reach your dreams 💗")

    st.subheader("💰 Your Money Snapshot")

    col1, col2, col3 = st.columns(3)
    col1.metric("💵 Money Received", f"₹{income:,.0f}")
    col2.metric("🛍️ Spent So Far", f"₹{expenses:,.0f}")
    col3.metric("🌈 Available Balance", f"₹{balance:,.0f}")

    st.markdown("---")
    st.subheader("⚙️ Set Your Budget")

    with st.form("budget_form"):
        period = st.selectbox(
            "Budget period",
            ["Weekly", "Monthly", "Custom"],
            index=["Weekly", "Monthly", "Custom"].index(
                st.session_state.budget_period
            )
        )
        budget = st.number_input(
            "Budget amount (₹)",
            min_value=0.0,
            value=float(st.session_state.budget),
            step=100.0
        )
        update_budget = st.form_submit_button("Save My Budget 💗")

        if update_budget:
            st.session_state.budget = budget
            st.session_state.budget_period = period
            st.success("Your budget has been updated!")
            st.rerun()

    st.markdown("---")
    st.subheader("🌼 Budget Health")

    ratio = (
        expenses / st.session_state.budget
        if st.session_state.budget > 0 else 0
    )
    st.progress(min(ratio, 1.0))
    st.write(
        f"₹{expenses:,.0f} spent out of "
        f"₹{st.session_state.budget:,.0f}"
    )

    if ratio > 1:
        st.error("You have exceeded your budget. Review your expenses.")
    elif ratio >= 0.8:
        st.warning("You are close to your budget limit!")
    else:
        st.success("You are within your budget. Keep going! 🌸")

    st.markdown("---")
    st.subheader("🌱 Your Savings Garden")

    goal_progress = min(
        st.session_state.goal_saved / st.session_state.goal_target,
        1.0
    ) if st.session_state.goal_target > 0 else 0

    st.progress(goal_progress)
    st.write(
        f"🌷 {st.session_state.goal_name}: "
        f"₹{st.session_state.goal_saved:,.0f} / "
        f"₹{st.session_state.goal_target:,.0f}"
    )

    if goal_progress >= 1:
        st.balloons()
        st.success("You reached your savings goal! 🎉")

    if st.session_state.points >= 100:
        st.success("🏆 Achievement unlocked: Money Master!")

# ---------------- MONEY ACTIVITY ----------------
elif page == "💳 Money Activity":
    st.title("💳 Money Activity")
    st.write("Keep track of the money you receive and spend.")

    activity = st.radio(
        "Select activity",
        ["💚 Add Money", "🛍️ Add Expense"],
        horizontal=True
    )

    with st.form("activity_form"):
        transaction_date = st.date_input("Date", value=date.today())

        if activity == "💚 Add Money":
            kind = "Income"
            category = st.selectbox(
                "Money source",
                [
                    "Family Allowance",
                    "Part-time Job",
                    "Scholarship",
                    "Gift",
                    "Other"
                ]
            )
        else:
            kind = "Expense"
            category = st.selectbox(
                "Expense category",
                [
                    "🍔 Food / Canteen",
                    "🚌 Bus / Travel",
                    "🏠 Hostel / Rent",
                    "📚 Books / Stationery",
                    "📱 Mobile / Recharge",
                    "🛍️ Shopping",
                    "🎬 Entertainment",
                    "💊 Personal Care",
                    "💸 Other"
                ]
            )

        description = st.text_input(
            "Description",
            placeholder="Example: College canteen lunch"
        )
        amount = st.number_input(
            "Amount (₹)",
            min_value=1.0,
            step=10.0
        )

        submit = st.form_submit_button("Save Activity ✨")

        if submit:
            st.session_state.transactions.append(
                [transaction_date, kind, category, description, amount]
            )
            st.success("Activity saved successfully! 🌸")
            st.rerun()

    st.markdown("---")
    st.subheader("🧾 Recent Activity")

    if df.empty:
        st.info("No activities recorded yet.")
    else:
        st.dataframe(
            df.sort_index(ascending=False),
            use_container_width=True,
            hide_index=True
        )

        transaction_options = {
            f"{i + 1}. {item[3] or item[2]} - ₹{item[4]:.0f}": i
            for i, item in enumerate(st.session_state.transactions)
        }

        selected_transaction = st.selectbox(
            "Select a transaction to delete",
            list(transaction_options.keys())
        )

        if st.button("Delete Selected Transaction"):
            index = transaction_options[selected_transaction]
            st.session_state.transactions.pop(index)
            st.rerun()

# ---------------- DREAM FUND ----------------
elif page == "🎯 Dream Fund":
    st.title("🎯 Dream Fund")
    st.write("Save little by little for something you love! 💗")

    with st.form("dream_form"):
        name = st.text_input(
            "What are you saving for?",
            value=st.session_state.goal_name
        )
        target = st.number_input(
            "Savings target (₹)",
            min_value=1.0,
            value=float(st.session_state.goal_target),
            step=100.0
        )
        update_goal = st.form_submit_button("Update My Dream 🌷")

        if update_goal:
            st.session_state.goal_name = name
            st.session_state.goal_target = target
            st.success("Dream fund updated!")
            st.rerun()

    st.markdown("---")
    st.subheader("🌸 Add Savings")

    with st.form("savings_form"):
        contribution = st.number_input(
            "Savings contribution (₹)",
            min_value=1.0,
            step=50.0
        )
        save = st.form_submit_button("Add to My Dream 💰")

        if save:
            if contribution > max(0, balance):
                st.error("Your available balance is not enough.")
            else:
                st.session_state.goal_saved += contribution
                st.session_state.points += 5
                st.success("Your dream is growing! 🌱")
                st.rerun()

    progress = min(
        st.session_state.goal_saved / st.session_state.goal_target,
        1.0
    )

    st.subheader(f"🌷 {st.session_state.goal_name}")
    st.progress(progress)
    st.write(
        f"₹{st.session_state.goal_saved:,.0f} / "
        f"₹{st.session_state.goal_target:,.0f}"
    )

    if progress >= 1:
        st.balloons()
        st.success("Congratulations! Goal completed! 🎉")
    else:
        st.info(
            f"₹{st.session_state.goal_target - st.session_state.goal_saved:,.0f} "
            "left to reach your goal."
        )

# ---------------- DAILY CHALLENGE ----------------
elif page == "🌱 Daily Challenge":
    st.title("🌱 Daily Money Challenge")
    st.write("Complete fun challenges and earn Bloom Points!")

    challenges = [
        "Save ₹20 from your available money.",
        "Track every expense you make today.",
        "Avoid unnecessary online shopping today.",
        "Carry water from home instead of buying it.",
        "Plan tomorrow's spending before going to bed."
    ]

    st.markdown("### 🌸 Your Challenge")
    st.info(st.session_state.challenge)

    if st.session_state.challenge in st.session_state.completed_challenges:
        st.success("You have already completed this challenge!")
    elif st.button("I Completed This! 🏆"):
        st.session_state.completed_challenges.append(
            st.session_state.challenge
        )
        st.session_state.points += 20
        st.success("Amazing! You earned 20 Bloom Points!")
        remaining = [
            c for c in challenges
            if c not in st.session_state.completed_challenges
        ]
        st.session_state.challenge = (
            random.choice(remaining) if remaining else
            "You completed all the challenges!"
        )
        st.balloons()
        st.rerun()

    if st.button("Get Another Challenge 🔄"):
        remaining = [
            c for c in challenges
            if c not in st.session_state.completed_challenges
        ]
        if remaining:
            st.session_state.challenge = random.choice(remaining)
            st.rerun()
        else:
            st.success("All challenges completed! 🌷")

    st.markdown("---")
    st.subheader("🏆 Your Progress")
    st.write(
        f"{len(st.session_state.completed_challenges)} "
        f"of {len(challenges)} challenges completed"
    )
    progress = min(
    1.0,
    len(st.session_state.completed_challenges) / len(challenges)
)

st.progress(progress)

# ---------------- MONEY INSIGHTS ----------------
elif page == "📊 Money Insights":
    st.title("📊 Money Insights")
    st.write("Understand your spending habits.")

    expense_df = df[df["Type"] == "Expense"].copy() if not df.empty else pd.DataFrame()

    if expense_df.empty:
        st.info("Record some expenses to see your insights.")
    else:
        st.subheader("🍓 Spending by Category")
        category_totals = expense_df.groupby("Category")["Amount"].sum()
        st.bar_chart(category_totals)

        st.subheader("📅 Daily Spending")
        expense_df["Date"] = pd.to_datetime(expense_df["Date"])
        daily_totals = expense_df.groupby("Date")["Amount"].sum()
        st.line_chart(daily_totals)

        st.subheader("💡 Smart Spending Tip")
        largest_category = category_totals.idxmax()
        st.info(
            f"Your highest spending category is {largest_category}. "
            "Check if you can reduce unnecessary expenses there."
        )

        csv = expense_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Expense Report 📥",
            data=csv,
            file_name="paisabloom_expenses.csv",
            mime="text/csv"
        )

# ---------------- MONEY QUIZ ----------------
elif page == "🧠 Money Quiz":
    st.title("🧠 Smart Money Quiz")
    st.write("Test your money management skills!")

    questions = [
        {
            "question": "What is 20% of ₹500?",
            "options": ["₹50", "₹100", "₹150", "₹200"],
            "answer": "₹100",
            "explanation": "20% of ₹500 is ₹100."
        },
        {
            "question": "Which is usually a student necessity?",
            "options": [
                "Textbook",
                "Gaming console",
                "Luxury watch",
                "Extra shoes"
            ],
            "answer": "Textbook",
            "explanation": "Textbooks are generally an educational necessity."
        },
        {
            "question": "What is a budget?",
            "options": [
                "A shopping list",
                "A money plan",
                "A bank account",
                "A loan"
            ],
            "answer": "A money plan",
            "explanation": "A budget helps you plan income and expenses."
        },
        {
            "question": "What should you do before an unnecessary purchase?",
            "options": [
                "Spend immediately",
                "Ignore your budget",
                "Check your needs and goals",
                "Borrow money"
            ],
            "answer": "Check your needs and goals",
            "explanation": "Think about your needs and goals before spending."
        }
    ]

    if not st.session_state.quiz_finished:
        index = st.session_state.quiz_index
        question = questions[index]

        st.progress(index / len(questions))
        st.subheader(f"Question {index + 1} of {len(questions)}")
        st.write(question["question"])

        answer = st.radio(
            "Choose your answer",
            question["options"],
            key=f"quiz_{index}"
        )

        if st.button("Submit Answer"):
            if answer == question["answer"]:
                st.session_state.quiz_score += 1
                st.session_state.quiz_feedback = (
                    "Correct! 🎉 " + question["explanation"]
                )
            else:
                st.session_state.quiz_feedback = (
                    f"Not quite. Correct answer: {question['answer']}. "
                    + question["explanation"]
                )

            st.session_state.quiz_index += 1

            if st.session_state.quiz_index >= len(questions):
                st.session_state.quiz_finished = True

            st.rerun()

        if st.session_state.quiz_feedback:
            st.info(st.session_state.quiz_feedback)

    else:
        st.balloons()
        st.subheader("🎉 Quiz Completed!")
        st.write(
            f"Your score: {st.session_state.quiz_score} / "
            f"{len(questions)}"
        )

        if st.button("Play Again 🔄"):
            st.session_state.quiz_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_feedback = ""
            st.session_state.quiz_finished = False
            st.rerun()

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("🌸 PaisaBloom | Made for every student's money journey 💗")
