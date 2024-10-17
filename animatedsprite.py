from pygame import sprite


class AnimatedSprite(sprite.Sprite):
    def __init__(self, idle_frames, hurt_frames, death_frames, attack_frames, x, y):
        super().__init__()
        self.idle_frames = idle_frames
        self.hurt_frames = hurt_frames
        self.death_frames = death_frames
        self.attack_frames = attack_frames

        self.death_animation_started = False
        self.death_animation_complete = False

        self.current_animation = "idle"
        self.current_frames = self.idle_frames
        self.current_frame_index = 0

        self.image = self.current_frames[self.current_frame_index]

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.animation_speed = 0.2
        self.animation_timer = 0

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frames)
            self.image = self.current_frames[self.current_frame_index]

    def set_animation(self, animation_name):
        if animation_name == "idle":
            self.current_frames = self.idle_frames
            self.current_animation = "idle"

        elif animation_name == "hurt":
            self.current_frames = self.hurt_frames
            self.current_animation = "hurt"

        elif animation_name == "death":
            self.current_frames = self.death_frames
            self.current_animation = "death"

        elif animation_name == "attack":
            self.current_frames = self.attack_frames
            self.current_animation = "attack"

        self.current_frame_index = 0
        self.image = self.current_frames[self.current_frame_index]
