class Config:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Ensure __init__ is only called once
            self.initialized = True
            # UI
            self.button_color = (24, 115, 119)
            self.button_hover_color = (24, 150, 119)
            self.text_color = (255, 255, 255)
            self.info_text_color = (0, 0, 0)
            self.title_color = (24, 115, 119)
            self.title_text = "Motion Analysis Platform"
            self.obstacle_color = (50, 50, 50)
            self.collision_color = (200, 0, 0)
            self.start_color = (0, 200, 0)
            self.goal_color = (200, 0, 0)
            self.path_color = (0, 0, 255)
            self.explored_color = (200, 200, 200)
            self.start_tree_color = (0, 0, 255)
            self.goal_tree_color = (255, 0, 0)
            self.sensor_range_color = (0, 180, 0, 50)
            # Environment
            self.screen_width = 1000
            self.screen_height = 700
            self.grid_color = (200, 200, 200)
            self.grid_resolution = 20
            self.debug = False


config_instance = Config()
