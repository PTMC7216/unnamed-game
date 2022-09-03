def game_intro(self):
    def timed_dialogue(seq, msg, spd=20):
        if timeframe_start[seq] < intro_time < timeframe_end[seq]:
            if seq > 0:
                resets[seq]()
            self.dialogue.typewriter_center(
                msg, (self.screen_res['x'] // 2, self.screen_res['y'] // 2), spd)

    # create a list of timeframes for use with the timer
    def list_increment(start, stop, step):
        value = start
        for n in range(stop):
            yield value
            value += step

    # modify values in timeframe lists after a specified index
    def change_step_by_index(index, step):
        for i in range(index + 1, len(timeframe_start)):
            timeframe_start[i] += step
        for i in range(index, len(timeframe_end)):
            timeframe_end[i] += step

    dialogues = 6
    duration = 4

    d_amt = dialogues
    timeframe_start = list(list_increment(0, d_amt, duration))
    timeframe_end = list(list_increment(duration, d_amt, duration))

    change_step_by_index(0, 0)
    change_step_by_index(1, -0.25)
    change_step_by_index(2, 0.25)
    change_step_by_index(3, 0.5)
    change_step_by_index(4, 0.5)
    change_step_by_index(5, 1)

    # reset typewriter
    r_count = 1
    resets = {}
    for x in range(dialogues - 1):
        resets[r_count] = utils.run_once(self.dialogue.reset)
        r_count += 1

    # stop current music
    pg.mixer.music.stop()

    # intro music
    pass

    # outer time object
    t0 = time()
    # intro loop
    while self.state == 'Intro':
        # self.game.dt

        t1 = time()

        # elapsed time
        intro_time = t1 - t0

        self.main_menu.check_events()

        self.screen.blit(self.background, (0, 0))

        timed_dialogue(0, "1 2 3", 3)
        timed_dialogue(1, "123.")
        timed_dialogue(2, "1234 123 1234...")
        timed_dialogue(3, "12 123 1234 123 1234567?")
        timed_dialogue(4, "12 12345 123 1234567 123 12345.")
        timed_dialogue(5, "123 123456789 123456 123 123456 12345678.")

        # background fade
        pass

        if intro_time >= 0.1:
            self.state = 'Overworld'

        self.render()
