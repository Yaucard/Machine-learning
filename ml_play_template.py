"""
The template of the main script of the machine learning process
"""

class MLPlay:
    def __init__(self):
        """
        Constructor
        """
        self.ball_served = False

    def update(self, scene_info):
      while True:
        platform_center =scene_info["platform"][0]+20
        ball_center = scene_info["ball"][0]+2.5
        ball_height = scene_info["ball"][1]
        
        if (scene_info["status"] == "GAME_OVER" or
            scene_info["status"] == "GAME_PASS"):
            return "RESET"
        
        if not self.ball_served:
            self.ball_served = True
            command = "SERVE_TO_RIGHT"
            return command
        else:
            command = "NONE"
            if ball_height <= 300:
             if ball_center > 100:
                if platform_center < 40	:
                    command = "MOVE_RIGHT"
                elif platform_center > 40	:
                    command = "MOVE_LEFT"
             elif ball_center < 100: 
                if platform_center < 160	:
                    command = "MOVE_RIGHT"
                else:
                    command = "MOVE_LEFT"
            elif ball_height >= 350:
                if platform_center < ball_center:
                    command = "MOVE_RIGHT"
                elif platform_center > ball_center:
                    command = "MOVE_LEFT"
            else:
                command = "NONE"
        return command

    
    def reset(self):
        """
        Reset the status
        """
        self.ball_served = False
