from datetime import datetime, timezone, timedelta
import secrets

from sqlmodel import Session, select, text

from app.models import Token


def generate_6_digit_code() -> int:
    """Generate a cryptographically secure 6-digit integer code."""
    return secrets.randbelow(900000) + 100000


def create_token(
    session: Session,
    resource_type: str,
    resource_id: str,
    expiry_seconds: int = 300,  # 5 minute
) -> int:

    session.exec(
        statement=text(
            """
        DELETE FROM token
        WHERE resource_type = :type
          AND resource_id = :id
        """
        ),
        params={"type": resource_type, "id": resource_id},
    )

    code = generate_6_digit_code()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(seconds=expiry_seconds)

    token = Token(
        code=code,
        resource_type=resource_type,
        resource_id=resource_id,
        created_at=now,
        expires_at=expires_at,
    )

    session.add(token)

    return code


def verify_token(
    session: Session,
    code: int,
    resource_type: str,
    resource_id: str,
    consume: bool = True,
) -> bool:
    now = datetime.now(timezone.utc)

    statement = select(Token).where(
        Token.code == code,
        Token.resource_type == resource_type,
        Token.resource_id == resource_id,
        Token.expires_at > now,
    )

    token = session.exec(statement).first()

    if not token:
        return False

    if consume:
        session.delete(token)
        session.commit()

    return True
