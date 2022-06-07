import time

class game_timer(object):
    
    def __init__(self, countdown):
        self.start = time.time()
        self.countdown = countdown
        self.time_elapsed = countdown
        
    def elapsed(self):
        if(self.time_elapsed <= 0):
            self.time_elapsed = self.countdown
            return True
        return False
    
    def tick(self):
        end = time.time()
        self.time_elapsed -= (end - self.start)
        self.start = end
        return self.elapsed()

    