"""
Camera system with screen shake and smooth following
"""
import random
import math


class Camera:
    """Handles camera movement and screen shake effects"""

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0

        # Screen shake
        self.shake_amount = 0
        self.shake_duration = 0
        self.shake_decay = 0.9

    def apply_shake(self, amount, duration=15):
        """Apply screen shake effect"""
        self.shake_amount = max(self.shake_amount, amount)
        self.shake_duration = max(self.shake_duration, duration)

    def update(self):
        """Update camera effects"""
        if self.shake_duration > 0:
            self.shake_duration -= 1

            # Random shake offset
            shake_x = random.uniform(-self.shake_amount, self.shake_amount)
            shake_y = random.uniform(-self.shake_amount, self.shake_amount)

            self.offset_x = shake_x
            self.offset_y = shake_y

            # Decay shake amount
            self.shake_amount *= self.shake_decay
        else:
            # Reset to no shake
            self.offset_x = 0
            self.offset_y = 0
            self.shake_amount = 0

    def get_offset(self):
        """Get current camera offset as integers"""
        return (int(self.offset_x), int(self.offset_y))
