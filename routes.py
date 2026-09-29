from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from .schemas import UserInput, FeedbackRequest
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan

from .database import (
    save_user,
    save_plan,
    get_original_plan,
    update_plan,
    get_user,
    get_all_users,
    get_all_plans,
    get_latest_plan,
    delete_user
)

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@router.post("/generate-workout")
async def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    user_data = UserInput(
        username=username,
        user_id=user_id,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )

    try:
        workout_plan = generate_workout_gemini(
            username=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )

        nutrition_tip = generate_nutrition_tip_with_flash(
            user_data.goal
        )

        save_user(user_data)

        save_plan(
            user_id=user_data.user_id,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user_data.username,
                "user_id": user_data.user_id,
                "age": user_data.age,
                "weight": user_data.weight,
                "goal": user_data.goal,
                "intensity": user_data.intensity,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "updated_plan": None,
                "message": None
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": username,
                "user_id": user_id,
                "age": age,
                "weight": weight,
                "goal": goal,
                "intensity": intensity,
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None,
                "message": f"Error generating plan: {str(e)}"
            }
        )


@router.post("/submit-feedback")
async def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...)
):
    feedback_data = FeedbackRequest(
        user_id=user_id,
        feedback=feedback
    )

    user = get_user(feedback_data.user_id)
    original_plan = get_original_plan(feedback_data.user_id)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "message": "User not found.",
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None
            }
        )

    if not original_plan:
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "message": "No workout plan found for this user.",
                "workout_plan": None,
                "nutrition_tip": None,
                "updated_plan": None
            }
        )

    try:
        revised_plan = update_workout_plan(
            original_plan=original_plan,
            feedback=feedback_data.feedback
        )

        update_plan(
            user_id=feedback_data.user_id,
            updated_plan=revised_plan
        )

        latest_plan = get_latest_plan(feedback_data.user_id)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user.username,
                "user_id": user.user_id,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": original_plan,
                "nutrition_tip": (
                    latest_plan.nutrition_tip
                    if latest_plan
                    else None
                ),
                "updated_plan": revised_plan,
                "message": "Your workout plan has been updated successfully."
            }
        )

    except Exception as e:
        latest_plan = get_latest_plan(user_id)

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "username": user.username,
                "user_id": user.user_id,
                "age": user.age,
                "weight": user.weight,
                "goal": user.goal,
                "intensity": user.intensity,
                "workout_plan": original_plan,
                "nutrition_tip": (
                    latest_plan.nutrition_tip
                    if latest_plan
                    else None
                ),
                "updated_plan": None,
                "message": f"Error updating plan: {str(e)}"
            }
        )


@router.get("/view-all-users")
async def view_all_users(request: Request):
    users = get_all_users()
    plans = get_all_plans()

    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={
            "users": users,
            "plans": plans
        }
    )


@router.post("/delete-user/{user_id}")
async def remove_user(user_id: str):
    delete_user(user_id)

    return RedirectResponse(
        url="/view-all-users",
        status_code=303
    )