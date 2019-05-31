def schedule(card, answer):
    # answer must be an integer from 0 to 5
    # updates @card.due_time based on @answer
    li = card.last_interval
    if li == 1:
        card.last_interval = 6

