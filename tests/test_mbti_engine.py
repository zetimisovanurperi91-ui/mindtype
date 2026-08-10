from app.services.mbti_engine import score_answers


def _weights_for(question_id: int, option_index: int) -> dict[str, int]:
    from app.data.questions import get_question

    question = get_question(question_id)
    assert question is not None
    return question["options"][option_index]["weights"]


def test_strongly_introverted_thinking_answers_produce_i_and_t():
    answers = {
        1: _weights_for(1, 1),  # I2
        2: _weights_for(2, 1),  # I2
        3: _weights_for(3, 1),  # I2
        4: _weights_for(4, 1),  # I2
        9: _weights_for(9, 0),  # T2
        10: _weights_for(10, 0),  # T2
        11: _weights_for(11, 0),  # T2
        12: _weights_for(12, 0),  # T2
    }
    result = score_answers(answers)
    assert result.mbti_type[0] == "I"
    assert result.mbti_type[2] == "T"


def test_strongly_extraverted_feeling_answers_produce_e_and_f():
    answers = {
        1: _weights_for(1, 0),  # E2
        2: _weights_for(2, 0),  # E2
        3: _weights_for(3, 0),  # E2
        4: _weights_for(4, 0),  # E2
        9: _weights_for(9, 1),  # F2
        10: _weights_for(10, 1),  # F2
        11: _weights_for(11, 1),  # F2
        12: _weights_for(12, 1),  # F2
    }
    result = score_answers(answers)
    assert result.mbti_type[0] == "E"
    assert result.mbti_type[2] == "F"


def test_result_has_four_letters_and_valid_axes():
    answers = {q_id: _weights_for(q_id, 0) for q_id in range(1, 16)}
    result = score_answers(answers)
    assert len(result.mbti_type) == 4
    assert result.mbti_type[0] in "EI"
    assert result.mbti_type[1] in "SN"
    assert result.mbti_type[2] in "TF"
    assert result.mbti_type[3] in "JP"


def test_confidence_is_between_50_and_100_when_there_is_a_signal():
    answers = {
        1: _weights_for(1, 0),
        2: _weights_for(2, 0),
        3: _weights_for(3, 0),
        4: _weights_for(4, 0),
    }
    result = score_answers(answers)
    ei_axis = result.axes["EI"]
    assert 50.0 <= ei_axis.confidence <= 100.0


def test_exact_tie_falls_back_to_deterministic_default():
    # E gets 2, I gets 2 -> exact tie on the EI axis
    answers = {1: {"E": 2}, 2: {"I": 2}}
    result = score_answers(answers)
    assert result.axes["EI"].letter == "I"  # documented tie-break default
    assert result.axes["EI"].confidence == 50.0


def test_no_answers_for_an_axis_still_produces_a_defined_letter():
    result = score_answers({})
    assert result.mbti_type[0] in "EI"
    assert result.axes["EI"].confidence == 50.0


def test_unknown_question_id_is_ignored_without_crashing():
    result = score_answers({9999: {"E": 5}})
    assert result.raw_scores["E"] == 0


def test_raw_scores_are_recoverable_from_result():
    answers = {1: {"E": 2}, 5: {"S": 2}}
    result = score_answers(answers)
    assert result.raw_scores["E"] == 2
    assert result.raw_scores["S"] == 2
