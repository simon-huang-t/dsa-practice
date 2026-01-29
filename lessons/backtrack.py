def backtrack(state):
    if goal_reached:
        record_answer
        return
    for choice in all_possible_choices:
        if choice_is_invalid:
            continue
        make_choice(choice)
        backtrack(updated_state)
        undo_choice(choice)
