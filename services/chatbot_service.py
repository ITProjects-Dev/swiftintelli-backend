from sqlalchemy import text
from database import engine
from uuid import uuid4
from sqlalchemy import text
def get_faq_questions():

    query = """
        SELECT faq_id, question
        FROM chat_faqs
        WHERE status = 1
        """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        rows = result.fetchall()

    return [
        {
            "faq_id": row[0],
            "question": row[1]
        }
        for row in rows
    ]

def get_faq_answer(faq_id):

    query = """
    SELECT answer
    FROM chat_faqs
    WHERE faq_id = :faq_id
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "faq_id": faq_id
            }
        )

        row = result.fetchone()

    if not row:
        return None

    return row[0]


def search_question(message):

    query = """
    SELECT
        ck.intent_id,
        cr.response_text
    FROM chat_keywords ck
    INNER JOIN chat_responses cr
        ON ck.intent_id = cr.intent_id
    WHERE LOWER(:message)
    LIKE CONCAT('%', LOWER(ck.keyword), '%')
    LIMIT 1
    """


    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "message": message.strip()
            }
        )

        row = result.fetchone()

    if row:

        return {
            "intent_id": row[0],
            "intent_name": row[1],
            "response": row[1]
        }

    return None

def get_fallback_response():

    query = """
    SELECT response_text
    FROM chat_fallbacks
    LIMIT 1
    """

    with engine.connect() as conn:

        result = conn.execute(text(query))

        row = result.fetchone()

    if row:
        return row[0]

    return "Sorry, I couldn't understand your question."


def get_sub_options():

    query = """
    SELECT
        option_id,
        option_name
    FROM chat_sub_options
    """

    with engine.connect() as conn:

        result = conn.execute(text(query))
        rows = result.fetchall()

    return [
        {
            "option_id": row[0],
            "option_name": row[1]
        }
        for row in rows
    ]


def get_sub_option_answer(option_id):

    query = """
    SELECT option_answer
    FROM chat_sub_options
    WHERE option_id = :option_id
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {"option_id": option_id}
        )

        row = result.fetchone()

    if row:
        return row[0]

    return None


def save_message(
    session_id,
    sender,
    message
):

    query = """
    INSERT INTO chat_messages
    (
        session_id,
        sender,
        message
    )
    VALUES
    (
        :session_id,
        :sender,
        :message
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "session_id": session_id,
                "sender": sender,
                "message": message
            }
        )

        conn.commit()




def session_exists(session_id):

    query = """
    SELECT session_id
    FROM chat_sessions
    WHERE session_id = :session_id
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "session_id": session_id
            }
        )

        row = result.fetchone()

    return row is not None

def end_chat_session(session_id):

    query = """
    UPDATE chat_sessions
    SET
        status = 'closed',
        ended_at = NOW()
    WHERE session_id = :session_id
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "session_id": session_id
            }
        )

        conn.commit()


def create_chat_session(session_id):

    query = """
    INSERT INTO chat_sessions
    (
        session_id,
        status
    )
    VALUES
    (
        :session_id,
        'active'
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "session_id": session_id
            }
        )

        conn.commit()

def save_chat_message(
    session_id,
    sender,
    message
):

    query = """
    INSERT INTO chat_messages
    (
        session_id,
        sender,
        message
    )
    VALUES
    (
        :session_id,
        :sender,
        :message
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "session_id": session_id,
                "sender": sender,
                "message": message
            }
        )

        conn.commit()

def save_chat_log(
    session_id,
    intent_id,
    user_question,
    bot_response,
    response_type
):

    query = """
    INSERT INTO chat_logs
    (
        session_id,
        intent_id,
        user_question,
        bot_response,
        response_type
    )
    VALUES
    (
        :session_id,
        :intent_id,
        :user_question,
        :bot_response,
        :response_type
    )
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "session_id": session_id,
                "intent_id": intent_id,
                "user_question": user_question,
                "bot_response": bot_response,
                "response_type": response_type
            }
        )

        conn.commit()

        return result.lastrowid


def search_course_question(message):

    query = """
    SELECT
        c.title,
        c.description,
        c.duration,
        c.price
    FROM chat_course_keywords ck
    INNER JOIN courses c
        ON ck.course_id = c.id
    WHERE LOWER(:message)
    LIKE CONCAT('%', LOWER(ck.keyword), '%')
    LIMIT 1
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "message": message.strip()
            }
        )

        row = result.fetchone()

    if row:

        return f"""
Course: {row[0]}

Description: {row[1]}

Duration: {row[2]}

Price: {row[3]}
"""

    return None


def save_unanswered_question(
    session_id,
    question
):

    query = """
    INSERT INTO chat_unanswered_questions
    (
        session_id,
        question
    )
    VALUES
    (
        :session_id,
        :question
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "session_id": session_id,
                "question": question
            }
        )

        conn.commit()

def get_setting(setting_name):

    query = """
    SELECT setting_value
    FROM chat_settings
    WHERE setting_name = :setting_name
    """

    with engine.connect() as conn:

        result = conn.execute(
            text(query),
            {
                "setting_name": setting_name
            }
        )

        row = result.fetchone()

    if row:
        return row[0]

    return None

def search_settings_question(message):

    message = message.lower()

    if "email" in message:
        return get_setting("support_email")

    if "phone" in message or "contact" in message:
        return get_setting("support_phone")

    return None

def save_callback_request(
    user_id,
    course_interest,
    preferred_time,
    notes
):

    query = """
    INSERT INTO callback_requests
    (
        user_id,
        course_interest,
        preferred_time,
        notes
    )
    VALUES
    (
        :user_id,
        :course_interest,
        :preferred_time,
        :notes
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "user_id": user_id,
                "course_interest": course_interest,
                "preferred_time": preferred_time,
                "notes": notes
            }
        )

        conn.commit()

def save_chatbot_action(
    user_id,
    action_type,
    reference_id=None,
    status="success"
):

    query = """
    INSERT INTO chatbot_actions
    (
        user_id,
        action_type,
        reference_id,
        status
    )
    VALUES
    (
        :user_id,
        :action_type,
        :reference_id,
        :status
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "user_id": user_id,
                "action_type": action_type,
                "reference_id": reference_id,
                "status": status
            }
        )

        conn.commit()
def save_feedback(log_id, rating):

    query = """
    INSERT INTO chat_feedback
    (
        log_id,
        rating
    )
    VALUES
    (
        :log_id,
        :rating
    )
    """

    with engine.connect() as conn:

        conn.execute(
            text(query),
            {
                "log_id": log_id,
                "rating": rating
            }
        )

        conn.commit()