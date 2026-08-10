from app.database.models import SessionStatus
from app.database.repositories.result_repo import ResultRepository
from app.database.repositories.session_repo import SessionRepository
from app.database.repositories.user_repo import UserRepository
from app.services.mbti_engine import score_answers


async def _make_user(session, telegram_id=111):
    repo = UserRepository(session)
    user, _created = await repo.get_or_create(telegram_id=telegram_id, username="tester", first_name="Test")
    return user


async def test_incomplete_test_can_be_resumed(db_session):
    user = await _make_user(db_session)
    session_repo = SessionRepository(db_session)

    test_session = await session_repo.create_session(user.id)
    await session_repo.save_answer(test_session.id, 1, 0)
    await session_repo.save_answer(test_session.id, 2, 1)

    active = await session_repo.get_active_session(user.id)
    assert active is not None
    assert active.id == test_session.id
    answers = await session_repo.get_answers(active.id)
    assert len(answers) == 2


async def test_abandoning_a_session_lets_a_new_one_start(db_session):
    user = await _make_user(db_session)
    session_repo = SessionRepository(db_session)

    first = await session_repo.create_session(user.id)
    await session_repo.save_answer(first.id, 1, 0)
    await session_repo.abandon_session(first)

    active = await session_repo.get_active_session(user.id)
    assert active is None  # abandoned sessions are not "active"

    second = await session_repo.create_session(user.id)
    assert second.id != first.id
    active_again = await session_repo.get_active_session(user.id)
    assert active_again.id == second.id


async def test_retaking_the_test_preserves_the_previous_result(db_session):
    user = await _make_user(db_session)
    session_repo = SessionRepository(db_session)
    result_repo = ResultRepository(db_session)

    first_session = await session_repo.create_session(user.id)
    await session_repo.complete_session(first_session)
    first_result = await result_repo.save_result(user.id, first_session.id, score_answers({1: {"E": 2}}))

    second_session = await session_repo.create_session(user.id)
    await session_repo.complete_session(second_session)
    second_result = await result_repo.save_result(user.id, second_session.id, score_answers({1: {"I": 2}}))

    # both results still exist - retaking never deletes history
    assert first_result.id != second_result.id
    latest = await result_repo.get_latest_for_user(user.id)
    assert latest.id == second_result.id

    stored_first = await result_repo.get_by_id_for_user(first_result.id, user.id)
    assert stored_first is not None
    assert stored_first.mbti_type[0] == "E"


async def test_result_ownership_check_blocks_other_users(db_session):
    owner = await _make_user(db_session, telegram_id=111)
    intruder = await _make_user(db_session, telegram_id=222)

    session_repo = SessionRepository(db_session)
    result_repo = ResultRepository(db_session)

    owner_session = await session_repo.create_session(owner.id)
    await session_repo.complete_session(owner_session)
    owner_result = await result_repo.save_result(owner.id, owner_session.id, score_answers({1: {"E": 2}}))

    # the intruder must never be able to fetch someone else's result by id
    stolen = await result_repo.get_by_id_for_user(owner_result.id, intruder.id)
    assert stolen is None

    legit = await result_repo.get_by_id_for_user(owner_result.id, owner.id)
    assert legit is not None


async def test_session_status_transitions(db_session):
    user = await _make_user(db_session)
    session_repo = SessionRepository(db_session)

    session = await session_repo.create_session(user.id)
    assert session.status == SessionStatus.in_progress

    await session_repo.complete_session(session)
    refreshed = await session_repo.get_by_id(session.id)
    assert refreshed.status == SessionStatus.completed
