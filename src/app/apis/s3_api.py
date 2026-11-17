import os
from dotenv import load_dotenv
from fastapi import APIRouter, Query, Depends, UploadFile, File, Form
from app.schemas.common_schema import ApiResponseDTO
from fastapi.responses import RedirectResponse
from app.services.s3_service import S3Service, get_s3_service
from app.enums.s3_enum import S3Folder

router = APIRouter()

@router.post(
    "/image",
    response_model=ApiResponseDTO,
    summary="이미지 업로드"
)
async def upload_image(
    file: UploadFile = File(...),
    folder: S3Folder = Form(...),
    s3_service: S3Service = Depends(get_s3_service)
):
    result = await s3_service.upload_image_with_thumbnail(
        file=file,
        folder=folder.value
    )

    return ApiResponseDTO(
        success=True,
        message="이미지 업로드 성공",
        data=result
    )


@router.get(
    "/image",
    summary="S3 Key로 이미지 url 조회"
)
async def get_image(
    key: str,
    s3_service: S3Service = Depends(get_s3_service)
):
    image_url = s3_service.get_url(key)

    return RedirectResponse(image_url)


@router.post(
    "/general-file",
    summary="일반 파일 업로드(PDF, Excel 등)",
    response_model=ApiResponseDTO
)
async def upload_general_file(
    file: UploadFile = File(...),
    folder: S3Folder = Form(...),
    s3_service: S3Service = Depends(get_s3_service)
):

    result = await s3_service.upload_file(
        file=file,
        folder=folder.value
    )

    return ApiResponseDTO(
        success=True,
        message="파일 업로드 성공",
        data=result
    )


@router.get(
    "/download",
    summary="S3 Key로 이미지 다운로드 링크 조회"
)
async def download_file(
    key: str,
    s3_service: S3Service = Depends(get_s3_service)
):
    download_url = await s3_service.get_download_url(key)

    return RedirectResponse(download_url)

