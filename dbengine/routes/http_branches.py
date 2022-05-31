from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi_sqlalchemy import db
from sqlalchemy.exc import NoResultFound

from dbengine.branch import create_branch, get_branch, ok_branch, request_merge_branch, unrequest_merge_branch
from dbengine.models import Branch


branch_router = APIRouter(prefix="/branch", tags=["Branch"])


@branch_router.get("/{branch_id}")
async def http_get_branch(branch_id: int) -> Branch:
    return get_branch(branch_id, session=db.session)


@branch_router.post("/{branch_name}")
async def http_create_branch_by_name(branch_name: str) -> Branch:
    return create_branch(branch_name, session=db.session)


@branch_router.post("/{branch_id}/merge/request")
async def http_request_merge_branch(branch_id: int) -> Branch:
    branch = get_branch(branch_id, session=db.session)
    return request_merge_branch(branch, session=db.session)


@branch_router.delete("/{branch_id}/merge/unrequest")
async def http_unreguest_merge_branch(branch_id: int) -> Branch:
    branch = get_branch(branch_id, session=db.session)
    return unrequest_merge_branch(branch, session=db.session)


@branch_router.post("/{branch_id}/merge/approve")
async def http_merge_branch(branch_id: int) -> Branch:
    branch = get_branch(branch_id, session=db.session)
    return ok_branch(branch, session=db.session)


@branch_router.get("")
async def http_get_all_branches():
    return db.session.query(Branch).all()


@branch_router.post("")
async def http_create_branch():
    return create_branch(name="default name", session=db.session)


@branch_router.patch("/{branch_id}")
async def patch_branch(branch_id: int, name: str):
    try:
        return db.session.query(Branch).filter(Branch.id == branch_id).update({name: name})
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Not found")