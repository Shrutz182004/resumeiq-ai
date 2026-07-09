from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.session import get_db
from app.models.resume import Resume
from app.models.user import User
from app.services.file_service import save_uploaded_file

from app.services.pdf_service import extract_text_from_pdf

from app.services.ai_service import analyze_resume

from app.schemas.job import JobMatchRequest
from app.services.ai_service import compare_resume_with_job

from app.schemas.rewrite import RewriteResumeRequest
from app.services.ai_service import rewrite_resume

from app.models.job_match import JobMatch

from app.services.pdf_generator import generate_resume_pdf

from fastapi.responses import FileResponse

from sqlalchemy import func

from app.schemas.chat import ResumeChatRequest
from app.services.ai_service import chat_with_resume

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename, filepath = save_uploaded_file(file)

    # Extract text from the uploaded PDF
    text = extract_text_from_pdf(filepath)
    analysis = analyze_resume(text)

    resume = Resume(
    filename=filename,
    filepath=filepath,
    extracted_text=text,
    ats_score=analysis["ats_score"],
    user_id=current_user.id,
)
    db.add(resume)
    db.commit()
    db.refresh(resume)

    return {
        "message": "Resume uploaded successfully",
        "resume_id": resume.id,
        "filename": filename,
        "analysis": analysis
    }

@router.post("/match")
def match_resume(
    request: JobMatchRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        return {"error": "Resume not found"}

    analysis = compare_resume_with_job(
    resume.extracted_text,
    request.job_description
)

# Save job match history
    job_match = JobMatch(
       resume_id=resume.id,
       job_description=request.job_description,
       match_score=analysis.get("match_score", 0),
       analysis=str(analysis)
)

    db.add(job_match)
    db.commit()

    return analysis

@router.post("/rewrite")
def rewrite_uploaded_resume(
    request: RewriteResumeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        return {"error": "Resume not found"}

    improved_resume = rewrite_resume(resume.extracted_text)

    filename, filepath = generate_resume_pdf(improved_resume)

    return {
        "message": "Resume rewritten successfully",
        "rewritten_resume": improved_resume,
        "pdf_filename": filename,
        "pdf_path": filepath
    }

@router.get("/download/{filename}")
def download_resume(filename: str):
    file_path = f"generated_resumes/{filename}"

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf",
    )

@router.get("/history")
def get_resume_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .all()
    )

    return [
        {
            "resume_id": resume.id,
            "filename": resume.filename,
            "ats_score": resume.ats_score,
            "uploaded_at": resume.created_at,
        }
        for resume in resumes
    ]

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resumes = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .all()
    )

    total_resumes = len(resumes)

    valid_scores = [
        resume.ats_score
        for resume in resumes
        if resume.ats_score is not None
    ]

    highest_score = max(valid_scores) if valid_scores else 0

    average_score = (
        round(sum(valid_scores) / len(valid_scores), 2)
        if valid_scores
        else 0
    )

    latest_resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
        .first()
    )

    return {
        "total_resumes": total_resumes,
        "highest_ats_score": highest_score,
        "average_ats_score": average_score,
        "latest_resume": latest_resume.filename if latest_resume else None,
    }

@router.post("/chat")
def resume_chat(
    request: ResumeChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = (
        db.query(Resume)
        .filter(
            Resume.id == request.resume_id,
            Resume.user_id == current_user.id
        )
        .first()
    )

    if not resume:
        return {"error": "Resume not found"}

    answer = chat_with_resume(
        resume.extracted_text,
        request.question
    )

    return {
        "answer": answer
    }