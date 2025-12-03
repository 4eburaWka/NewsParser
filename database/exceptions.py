from sqlalchemy import select, delete, insert

from database.database import AsyncSession
from models.db.Exception import UserException


async def get_user_exceptions(session: AsyncSession, user_id: int) -> UserException:
    query = (
        select(UserException)
        .where(UserException.user_id == user_id)
    )
    
    result = (await session.execute(query)).scalars().one_or_none()
    
    return result


async def set_user_exceptions(session: AsyncSession, user_id: int, exceptions: list[str]):
    del_query = (
        delete(UserException)
        .where(UserException.user_id == user_id)
    )
    
    try:
        await session.execute(del_query)
    except Exception:
        pass
    
    user_exceptions = UserException(user_id=user_id, exeptions=','.join(exceptions))
    
    session.add(user_exceptions)
    await session.commit()