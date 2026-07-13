from unittest import result
from urllib import request
from fastapi import APIRouter, HTTPException
from services.chatbot_service import search_course_question
from fastapi import APIRouter, HTTPException
from schemas import ChatRequest
from schemas import FAQRequest
from schemas import FeedbackRequest
from schemas import EndChatRequest
from utils.validations import validate_message
from schemas import CallbackRequest
from services.chatbot_service import (
    get_faq_questions,
    get_faq_answer,
    search_question,
    get_fallback_response,
    get_sub_options,
    get_sub_option_answer,
    save_feedback,
    save_message,
    create_chat_session,
    session_exists,
    end_chat_session,
    save_chat_log,
    search_course_question,
    save_unanswered_question,
    search_settings_question,
    save_callback_request,
    save_chatbot_action

    

)
router = APIRouter()
@router.get("/faq-questions")
def faq_questions():

    return {
        "status": 200,
        "data": get_faq_questions()
    }
@router.get("/faq-answer/{faq_id}")
def faq_answer(faq_id: int):

    answer = get_faq_answer(faq_id)

    if not answer:

        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return {
        "status": 200,
        "answer": answer
    }
@router.post("/chat")
def chat(request: ChatRequest):

    try:

        validate_message(request.message)

        # Create session if it doesn't exist
        if not session_exists(
            request.session_id
        ):
            create_chat_session(
                request.session_id
            )

        # Save User Message
        save_message(
            request.session_id,
            "user",
            request.message
        )

        intent_id = None

        # 1. Check settings first
        answer = search_settings_question(
            request.message
        )

        if answer:

            response_type = "settings_match"

        else:

            # 2. Check keywords
            result = search_question(
                request.message
            )

            if result:

                intent_id = result["intent_id"]
                answer = result["response"]
                response_type = "keyword_match"

            else:

                # 3. Check courses
                answer = search_course_question(
                    request.message
                )

                if answer:

                    response_type = "course_match"

                else:

                    # 4. Fallback
                    answer = get_fallback_response()
                    response_type = "fallback"

                    save_unanswered_question(
                        request.session_id,
                        request.message
                    )

        log_id= save_chat_log(
            request.session_id,
            intent_id,
            request.message,
            answer,
            response_type
        )

        # Save Bot Message
        save_message(
            request.session_id,
            "bot",
            answer
        )

        return {
            "success": True,
            "answer": answer,
            "log_id": log_id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@router.get("/sub-options")
def sub_options():

    data = get_sub_options()

    return {
        "success": True,
        "data": data
    }


@router.get("/sub-option-answer/{option_id}")
def sub_option_answer(option_id: int):

    answer = get_sub_option_answer(option_id)

    if not answer:

        raise HTTPException(
            status_code=404,
            detail="Option not found"
        )

    return {
        "success": True,
        "answer": answer
    }


@router.post("/end-chat")
def end_chat(request: EndChatRequest):

    try:

        end_chat_session(
            request.session_id
        )

        save_chatbot_action(
            None,
            "end_chat"
        )

        return {
            "success": True,
            "message": "Chat ended successfully"
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to end chat"
        )
@router.post("/callback-request")
def callback_request(request: CallbackRequest):

    try:

        save_callback_request(
            request.user_id,
            request.course_interest,
            request.preferred_time,
            request.notes
        )

        save_chatbot_action(
            request.user_id,
            "callback_request"
        )

        return {
            "success": True,
            "message": "Callback request submitted successfully"
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to save request"
        )
    

@router.post("/feedback")
def feedback(request: FeedbackRequest):

    try:

        save_feedback(
            request.log_id,
            request.rating
        )

        return {
            "success": True,
            "message": "Feedback saved successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    