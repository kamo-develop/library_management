from fastapi import Depends, HTTPException, status

from deps import CurrentUserDep
from models import UserRole


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: CurrentUserDep):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )


AdminOnlyAccess = Depends(RoleChecker([UserRole.ADMIN]))
