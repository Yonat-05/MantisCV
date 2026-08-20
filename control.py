class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd

        self.prev_error = 0
        self.integral = 0
        
    def update(self, error):
        P = self.kp * error
        self.integral += error
        I = self.ki * self.integral
        D = self.kd * (error - self.prev_error)
        self.prev_error = error
        
        return P+I+D
