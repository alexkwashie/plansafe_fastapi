from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.auth_token import get_current_user
from routers.schemas import (
    ChecklistTemplateBase, ChecklistTemplateUpdate, ChecklistTemplateDisplay,
    TemplateItemBase, TemplateItemDisplay,
)
from routers.pagination import PaginationParams
from routers.response import paginated_response
from db.db_checklists import db_checklist_template
import uuid
from typing import List


router = APIRouter(
    prefix='/api/v1',
    tags=['checklist-templates']
)


@router.post('/checklist-templates', response_model=ChecklistTemplateDisplay)
async def create(request: ChecklistTemplateBase, user=Depends(get_current_user)):
    return db_checklist_template.create_template(request, user)


@router.get('/checklist-templates')
async def list_templates(pagination: PaginationParams = Depends()):
    data, total = db_checklist_template.get_all_templates(offset=pagination.offset, limit=pagination.limit)
    return paginated_response(data, total, pagination.page, pagination.per_page)


@router.get('/checklist-templates/{template_id}', response_model=ChecklistTemplateDisplay)
async def get_template(template_id: uuid.UUID):
    return db_checklist_template.get_by_id(template_id)


@router.put('/checklist-templates/{template_id}', response_model=ChecklistTemplateDisplay)
async def update(template_id: uuid.UUID, request: ChecklistTemplateUpdate, user=Depends(get_current_user)):
    return db_checklist_template.update_template(template_id, request, user)


@router.delete('/checklist-templates/{template_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete(template_id: uuid.UUID, user=Depends(get_current_user)):
    if not db_checklist_template.delete_template(template_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Template not found")


# Template items
@router.post('/checklist-templates/{template_id}/items', response_model=TemplateItemDisplay)
async def add_item(template_id: uuid.UUID, request: TemplateItemBase, user=Depends(get_current_user)):
    return db_checklist_template.add_item(template_id, request)


@router.get('/checklist-templates/{template_id}/items', response_model=List[TemplateItemDisplay])
async def list_items(template_id: uuid.UUID):
    return db_checklist_template.get_items(template_id)


@router.delete('/checklist-template-items/{item_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: uuid.UUID, user=Depends(get_current_user)):
    if not db_checklist_template.delete_item(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
